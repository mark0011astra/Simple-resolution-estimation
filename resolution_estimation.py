import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import statistics

def load_and_display_image(image_path):
    image = cv2.imread(image_path)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.show()
    return image

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    return edges

def display_image(image, title="Image"):
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.show()

def filter_hough_lines(lines):
    vertical_lines = []
    horizontal_lines = []
    for line in lines:
        for rho, theta in line:
            if abs(theta - 0) < np.pi / 36 or abs(theta - np.pi) < np.pi / 36:  # 垂直線
                vertical_lines.append((rho, theta))
            elif abs(theta - np.pi/2) < np.pi / 36 or abs(theta - 3*np.pi/2) < np.pi / 36:  # 水平線
                horizontal_lines.append((rho, theta))
    return vertical_lines, horizontal_lines

def find_and_draw_hough_lines(edges, image):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)
    vertical_lines, horizontal_lines = filter_hough_lines(lines)
    for line in vertical_lines + horizontal_lines:
        rho, theta = line
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y2 = int(y0 + 1000 * (a))
        cv2.line(image, (x1, int(y0)), (int(x0), y2), (0, 0, 255), 2)
    return image

def estimate_resolution(image, vertical_lines, horizontal_lines):
    height, width = image.shape[:2]
    if vertical_lines:
        vertical_distances = [line[0] for line in vertical_lines]
        vertical_distances.sort()
        vertical_diffs = [vertical_distances[i+1] - vertical_distances[i] for i in range(len(vertical_distances)-1)]
        mode_vertical = statistics.median(vertical_diffs) if vertical_diffs else 0
        resolution_y = width / mode_vertical if mode_vertical else 0
    else:
        resolution_y = 0

    if horizontal_lines:
        horizontal_distances = [line[0] for line in horizontal_lines]
        horizontal_distances.sort()
        horizontal_diffs = [horizontal_distances[i+1] - horizontal_distances[i] for i in range(len(horizontal_distances)-1)]
        mode_horizontal = statistics.median(horizontal_diffs) if horizontal_diffs else 0
        resolution_x = height / mode_horizontal if mode_horizontal else 0
    else:
        resolution_x = 0

    return round(resolution_x), round(resolution_y)

def main():
    image_path = "img01.png"
    image = load_and_display_image(image_path)
    edges = preprocess_image(image)
    display_image(edges, "Edges")
    lines_image = find_and_draw_hough_lines(edges, image.copy())
    display_image(lines_image, "Lines Detected")
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)
    vertical_lines, horizontal_lines = filter_hough_lines(lines)
    resolution_x, resolution_y = estimate_resolution(image, vertical_lines, horizontal_lines)
    print(f"Estimated Horizontal Resolution: {resolution_y} pixels")
    print(f"Estimated Vertical Resolution: {resolution_x} pixels")

if __name__ == "__main__":
    main()
