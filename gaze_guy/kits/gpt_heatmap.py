import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

def draw_gaze_heatmap(gaze_positions, sigma=15):
    # Determine the maximum and minimum gaze    
    max_x, max_y = np.max(gaze_positions, axis=0)
    min_x, min_y = np.min(gaze_positions, axis=0)
    # Compute the heatmap shape based on the gaze position range
    width = int(max_x - min_x + 1)
    height = int(max_y - min_y + 1)
    heatmap_shape = (height, width, 1)
    # Create a blank image with the desired shape
    heatmap = np.zeros(heatmap_shape, dtype=np.float32)
    # Resize the heatmap to a
    # heatmap = cv2.resize(heatmap, (960, 540), interpolation=cv2.INTER_AREA)
    # Draw a Gaussian blur at each gaze position
    for x, y in gaze_positions:
        x, y = int(x - min_x), int(y - min_y)
        heatmap[y][x] += 1
    heatmap = cv2.GaussianBlur(heatmap, (0, sigma), sigmaX=10)
    # Normalize the heatmap values to a range between 0 and 255
    heatmap = cv2.normalize(heatmap, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    # Apply a color map to the heatmap
    cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    # Add a colorbar to the right of the heatmap
    fig, ax = plt.subplots()
    ax.axis('off')
    # Draw the axis in the center of the image
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    # Set the limit for the axis
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    
    # Use the ScalarMappable object to create the colorbar with the same color map as the heatmap
    sm = ScalarMappable(cmap='jet')
    sm.set_array([])
    fig.colorbar(sm, ax=ax)
    
    plt.imshow(heatmap[::-1], cmap='jet', vmin=0, vmax=255)
    
    # Set the x and y labels to the gaze position range
    ax.set_xticks(np.arange(width))
    ax.set_yticks(np.arange(height))
    ax.set_xticklabels(np.arange(min_x, max_x+1))
    ax.set_yticklabels(np.arange(min_y, max_y+1)[::-1])
    # Rotate the x labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.show()
    return heatmap

def main():
    # Generate 1000 random gaze positions between (-500, -500) and (500, 500)
    gaze_positions = np.random.randint(-50, 50, size=(1000000, 2))
    # Draw the gaze heatmap
    heatmap = draw_gaze_heatmap(gaze_positions, 15)

if __name__ == '__main__':
    main()
