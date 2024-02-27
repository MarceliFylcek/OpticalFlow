from skimage import io
from skimage import registration
from skimage.color import rgb2gray
from skimage.transform import warp
import numpy as np
import matplotlib.pyplot as plt
import os
from progress.bar import Bar

from config import *
from utils import save, display

"""
Image A used as a reference
Image B warped
Images saved in PNG format
"""

if __name__ == "__main__":
    if not os.path.isdir(destination_path):
        os.makedirs(destination_path, exist_ok=True)

    for sequence_name in sequences:
        print(f"Starting sequence {sequence_name}...")
        A_path = os.path.join(dataset_path, sequence_name, "A")
        B_path = os.path.join(dataset_path, sequence_name, "B")

        A_names = os.listdir(A_path)
        B_names = os.listdir(B_path)

        if len(A_names) != len(B_names):
            print(f"Uneven number of images: {len(A_names)} : {len(B_names)}")
            quit()

        sequence_images = []

        for image_A, image_B in zip(os.listdir(A_path), os.listdir(B_path)):
            if image_A != image_B:
                print(f"Image mismatch {image_A: image_B}")
                quit()

            sequence_images.append(image_A)

        with Bar(f"Sequence {sequence_name}", max=len(sequence_images)) as bar:
            for image in sequence_images:
                bar.next()
                image_A = io.imread(os.path.join(A_path, image))
                image_B = io.imread(os.path.join(B_path, image))

                #! Optical flow only supported for gray scale
                # Y = 0.2125 R + 0.7154 G + 0.0721 B
                image_A_gray = rgb2gray(image_A)
                image_B_gray = rgb2gray(image_B)

                # x, y shift for every pixel in the image
                v, u = registration.optical_flow_tvl1(image_A_gray, image_B_gray)

                rows, columns, channels = image_A.shape
                row_coords, col_coords = np.meshgrid(
                    np.arange(rows), np.arange(columns), indexing="ij"
                )

                new_coords = np.array([row_coords + v, col_coords + u])

                # Warp each channel
                rgb_channels = []
                for channel in range(channels):
                    rgb_channels.append(
                        warp(image_B[..., channel], new_coords, mode="edge")
                    )

                # Combine the channels to RGB image
                image_B_warped = np.zeros((rows, columns, channels))
                image_B_warped[..., 0] = rgb_channels[0]
                image_B_warped[..., 1] = rgb_channels[1]
                image_B_warped[..., 2] = rgb_channels[2]

                # display(image_B_warped, image_A, image_B)
                save(image_A, image_B_warped, image, (os.path.join(destination_path, sequence_name)))