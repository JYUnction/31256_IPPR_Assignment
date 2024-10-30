import os

# Set paths
train_images_path = 'dataset/train'
val_images_path = 'dataset/val'

# Get the list of class directories (subdirectories in training path)
class_dirs = [d for d in os.listdir(train_images_path) if os.path.isdir(os.path.join(train_images_path, d))]
num_classes = len(class_dirs)  # Number of classes

# Create a list of class names
class_names = [class_name for class_name in class_dirs]  # Use directory names as class names

# Create the YAML content
yaml_file_path = 'dataset.yaml'  # Name of the YAML file
yaml_content = f"""
train: {train_images_path}
val: {val_images_path}

nc: {num_classes}  # Number of classes
names: {class_names}  # List of class names
"""

# Write the YAML content to a file
with open(yaml_file_path, 'w') as yaml_file:
    yaml_file.write(yaml_content.strip())

print(f"Generated {yaml_file_path} with {num_classes} classes: {class_names}.")
