import os
import shutil

def pull_files_from_subfolders(input_directory, output_directory, file_extension=".jpg"):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Walk through the input directory
    for root, _, files in os.walk(input_directory):
        for file in files:
            # Check for the specified file extension
            if file.endswith(file_extension):
                # Construct full file path
                file_path = os.path.join(root, file)
                
                # Copy the file to the output directory
                shutil.copy(file_path, output_directory)
                print(f"Copied: {file_path} to {output_directory}")

if __name__ == "__main__":
    # Specify your input and output directories
    input_directory = "256_ObjectCategories"  # Change to your input directory
    output_directory = "pulled_images"  # Change to your desired output directory
    
    # Call the function to pull files
    pull_files_from_subfolders(input_directory, output_directory)
