import os
import random
import shutil

# Set the paths
dataset_dir = 'img_anno_merged'  # Dataset directory
train_dir = 'train'  # Directory for training images and labels
val_dir = 'val'      # Directory for validation images and labels

# Create directories for training and validation if they don't exist
os.makedirs(os.path.join(train_dir), exist_ok=True)
os.makedirs(os.path.join(val_dir), exist_ok=True)

# Loop through each class folder in the dataset
for class_folder in os.listdir(dataset_dir):
    class_path = os.path.join(dataset_dir, class_folder)
    
    if os.path.isdir(class_path):
        # Get all image files in the class folder
        images = [f for f in os.listdir(class_path) if f.endswith('.jpg') or f.endswith('.png')]

        # Shuffle the images randomly
        random.shuffle(images)
        
        # Calculate split index
        split_idx = int(len(images) * 0.8)
        
        # Split images into training and validation
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        # Create class directories in train and val folders
        os.makedirs(os.path.join(train_dir, class_folder), exist_ok=True)
        os.makedirs(os.path.join(val_dir, class_folder), exist_ok=True)
        
        # Move training images and labels to train directory
        for img in train_images:
            img_source_path = os.path.join(class_path, img)
            shutil.copy(img_source_path, os.path.join(train_dir, class_folder, img))  # Copy image
            
            # Copy corresponding label file
            label_file_name = img.replace('.jpg', '.txt').replace('.png', '.txt')
            shutil.copy(os.path.join(class_path, label_file_name), os.path.join(train_dir, class_folder, label_file_name))  # Copy label
            
        # Move validation images and labels to val directory
        for img in val_images:
            img_source_path = os.path.join(class_path, img)
            shutil.copy(img_source_path, os.path.join(val_dir, class_folder, img))  # Copy image
            
            # Copy corresponding label file
            label_file_name = img.replace('.jpg', '.txt').replace('.png', '.txt')
            shutil.copy(os.path.join(class_path, label_file_name), os.path.join(val_dir, class_folder, label_file_name))  # Copy label

print("Dataset split into training and validation sets with labels.")
