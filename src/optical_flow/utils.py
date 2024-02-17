from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image


def display(image_B_warped, image_A, image_B):
    image_B_warped_gray = rgb2gray(image_B_warped)
    image_A_gray = rgb2gray(image_A)
    image_B_gray = rgb2gray(image_B)
    rows, columns, _ = image_A.shape

    seq_im = np.zeros((rows, columns, 3))
    seq_im[..., 0] = image_B_gray
    seq_im[..., 1] = image_A_gray
    seq_im[..., 2] = image_A_gray

    reg_im = np.zeros((rows, columns, 3))
    reg_im[..., 0] = image_B_warped_gray
    reg_im[..., 1] = image_A_gray
    reg_im[..., 2] = image_A_gray

    fig, ((ax0_0, ax0_1), (ax1_0, ax1_1), (ax2_0, ax2_1)) = plt.subplots(3, 2, figsize=(4.5, 7.5))

    ax0_0.imshow(image_A)
    ax0_0.set_title("Image A")
    ax0_0.set_axis_off()

    ax0_1.imshow(image_B)
    ax0_1.set_title("Image B")
    ax0_1.set_axis_off()

    ax1_0.imshow(seq_im)
    ax1_0.set_title("Unregistered sequence")
    ax1_0.set_axis_off()

    ax1_1.imshow(reg_im)
    ax1_1.set_title("Registered sequence")
    ax1_1.set_axis_off()

    ax2_0.imshow(image_A)
    ax2_0.set_title("Image A")
    ax2_0.set_axis_off()

    ax2_1.imshow(image_B_warped)
    ax2_1.set_title("Image B warped")
    ax2_1.set_axis_off()

    fig.tight_layout()
    plt.show()


def save(image_A, image_B_warped, name, sequence_path):
    if not os.path.isdir(sequence_path):
        os.mkdir(sequence_path)
    
    A_path = os.path.join(sequence_path, "A")
    B_path = os.path.join(sequence_path, "B")

    if not os.path.isdir(A_path) or not os.path.isdir(B_path):
        os.makedirs(os.path.join(sequence_path, "A"), exist_ok=True)
        os.makedirs(os.path.join(sequence_path, "B"), exist_ok=True)

    # Change to PNG
    file_name = os.path.splitext(name)[0] + ".png"

    A_name = os.path.join(A_path, file_name)
    B_name = os.path.join(B_path, file_name)

    image_B_warped = (np.rint(image_B_warped * 255.0)).astype(np.uint8)

    image_A = Image.fromarray(image_A)
    image_B_warped = Image.fromarray(image_B_warped)
    
    image_A.save(A_name)
    image_B_warped.save(B_name)
