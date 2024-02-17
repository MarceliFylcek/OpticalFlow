import os

folder_path = 'dataset/pylon/1/A'

files = os.listdir(folder_path)
print(files)
files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))
#files.sort()

for index, file_name in enumerate(files):
    old_path = os.path.join(folder_path, file_name)
    new_name = f"{index}{os.path.splitext(file_name)[1]}"
    new_path = os.path.join(folder_path, new_name)
    
    os.rename(old_path, new_path)