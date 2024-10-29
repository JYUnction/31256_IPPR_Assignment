import os
import shutil

# Input and output paths
input_file = 'folders_list.txt'
source_dir = '256_ObjectCategories'  # Update to your source dataset path
output_dir = '256_ObjectCategories_renamed'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read folder names and copy them to the new directory
with open(input_file, 'r') as f:
    for i, line in enumerate(f):
        folder_name = line.strip()  # Remove any trailing newline or spaces
        source_folder = os.path.join(source_dir, folder_name)
        
        # Rename and copy each folder with sequential numbering
        new_folder_name = f"{str(i + 1).zfill(3)}_{folder_name}"
        dest_folder = os.path.join(output_dir, new_folder_name)
        
        if os.path.isdir(source_folder):
            shutil.copytree(source_folder, dest_folder)
            print(f"Copied {folder_name} to {new_folder_name}")

print("Folders copied and renamed in sequence.")
