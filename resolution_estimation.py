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
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    edges = cv2.Canny(gray, 20, 300, L2gradient=True)
    return gray, adaptive_thresh, edges

def display_image(image, title="Image"):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.show()

def find_and_draw_hough_lines(edges, image):
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    if lines is not None:
        for rho, theta in lines.squeeze(axis=1):
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (130, 0, 255), 2)
    return image

def analyze_lines(lines):
    if lines is None:
        return 0, 0
    vertical_lines = [line for line in lines if line[0][1] == 0]
    horizontal_lines = [line for line in lines if line[0][1] != 0]
    if not vertical_lines or not horizontal_lines:
        return 0, 0
    vertical_diffs = sorted([abs(vertical_lines[i][0][0] - vertical_lines[i+1][0][0]) for i in range(len(vertical_lines)-1)])
    horizontal_diffs = sorted([abs(horizontal_lines[i][0][0] - horizontal_lines[i+1][0][0]) for i in range(len(horizontal_lines)-1)])
    mode_vertical = statistics.mode(vertical_diffs) if vertical_diffs else 0
    mode_horizontal = statistics.mode(horizontal_diffs) if horizontal_diffs else 0
    return abs(mode_vertical), abs(mode_horizontal)

def estimate_resolution(image, mode_vertical, mode_horizontal):
    height, width = image.shape[:2]
    resolution_y = width / mode_vertical if mode_vertical else 0
    resolution_x = height / mode_horizontal if mode_horizontal else 0
    return round(resolution_x), round(resolution_y)

def main():
    image_path = "img01.png"
    image = load_and_display_image(image_path)
    gray, adaptive_thresh, edges = preprocess_image(image)
    display_image(adaptive_thresh, "Adaptive Threshold")
    display_image(edges, "Edges")
    lines_image = find_and_draw_hough_lines(edges, image.copy())
    display_image(lines_image, "Lines Detected")
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    mode_vertical, mode_horizontal = analyze_lines(lines)
    resolution_x, resolution_y = estimate_resolution(image, mode_vertical, mode_horizontal)
    print(f"Estimated Horizontal Resolution: {resolution_y} pixels")
    print(f"Estimated Vertical Resolution: {resolution_x} pixels")

if __name__ == "__main__":
    main()
