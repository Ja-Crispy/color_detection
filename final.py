import cv2
import numpy as np
import pandas as pd
import argparse

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

# Reading the image with OpenCV
img = cv2.imread(img_path)

# Declaring global variables (used later on)
clicked = False
r = g = b = xpos = ypos = 0

# Reading CSV file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    distances = {}
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        distances[d] = csv.loc[i, "color_name"]
    min_distance = min(distances.keys())
    return distances[min_distance]

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Create a window and set the mouse callback function
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    cv2.imshow("image", img)
    
    if clicked:
        # Create a region of interest around the clicked pixel
        roi = img[ypos - 10:ypos + 10, xpos - 10:xpos + 10]
        
        # Calculate the mean color within the ROI
        mean_color = np.mean(roi, axis=(0, 1))
        b, g, r = mean_color.astype(int)
        
        # Create a rectangle to display the detected color
        cv2.rectangle(img, (20, 20), (750, 60), (int(b), int(g), int(r)), -1)

        # Get the color name and RGB values
        color_name = getColorName(r, g, b)
        text = f"{color_name} R={r} G={g} B={b}"
        
        # Display the color name and RGB values
        cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        
        # For very light colors, display text in black
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            
        clicked = False

    # Break the loop when the user hits the 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()
