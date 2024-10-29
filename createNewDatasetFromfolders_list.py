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

            # Rename the image files inside the new folder
            for img_file in os.listdir(dest_folder):
                if img_file.endswith('.jpg'):  # Assuming images are .jpg
                    # Extract the old category name from the image filename
                    old_category = img_file.split('_')[0]  # This assumes the format is like 001_xxxx.jpg
                    
                    # Create the new filename based on the new folder name
                    new_img_file = img_file.replace(old_category, str(i + 1).zfill(3))  # Update old category with new number
                    old_img_path = os.path.join(dest_folder, img_file)
                    new_img_path = os.path.join(dest_folder, new_img_file)

                    # Rename the image file
                    os.rename(old_img_path, new_img_path)
                    print(f"Renamed {img_file} to {new_img_file} in {new_folder_name}")

print("Folders copied and renamed, along with updated image filenames.")
