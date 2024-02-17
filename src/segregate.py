import os
import shutil


root_folder = "dataset/pylon"
camera_A = "40316885"
camera_B = "40334462"


for sequence in os.listdir(root_folder):
    sequence_path = os.path.join(root_folder, sequence)

    destination_dir_A = os.path.join(sequence_path, "A")
    if not os.path.exists(destination_dir_A):
        os.mkdir(destination_dir_A)

    destination_dir_B = os.path.join(sequence_path, "B",)
    if not os.path.exists(destination_dir_B):
        os.mkdir(destination_dir_B)

    for image in os.listdir(sequence_path):
        image_path = os.path.join(sequence_path, image)
        
        if not os.path.isdir(image_path):
            if camera_A in image:
                shutil.move(image_path, os.path.join(destination_dir_A, image))

            elif camera_B in image:
                shutil.move(image_path, os.path.join(destination_dir_B, image))