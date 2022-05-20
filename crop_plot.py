import numpy as np
from PIL import Image
import pandas as pd
import sys

def main(img_path, txt_path):

    # Log start
    print('Loading image.')

    # Load the image and convert it to the proper color space
    png_image = Image.open(img_path)
    png_image = png_image.convert("RGBA")

    # Load the coordinates and calculate image dimensions
    coords = pd.read_csv(txt_path, sep=" ", header=0, index_col=0)
    extent = ((coords.iloc[1, 0] - coords.iloc[0, 0]) * coords.iloc[2, 0], (coords.iloc[0, 1] - coords.iloc[1, 1]) * coords.iloc[2, 0])

    # Crop the image to the proper size
    img_array_cropped = np.array(png_image.crop((0, png_image.height - extent[1], extent[0], png_image.height)))

    # Convert all full white pixels to transparent
    img_array_cropped[:, :, 3] = (255 * (img_array_cropped[:, :, :3] != 255).any(axis=2)).astype(np.uint8)

    # Create a new image and save it to overwrite the unmodified one
    png_image_cropped = Image.fromarray(img_array_cropped)

    print('Saving image.')
    png_image_cropped.save(img_path)

    # Drop the resolution row in the coordinates txt
    coords.drop(index=coords.index[-1], axis=0, inplace=True)

    # Save the modified txt to overwrite the temporary one
    coords.to_csv(txt_path, sep=" ")

    print('Done.')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])