from ultralytics import YOLO
import os

# Load the pre-trained YOLOv8 model (replace with your model path if custom)
model = YOLO('yolov8n.pt')  # or 'path/to/your/custom_model.pt'

# Paths
images_dir = '256_ObjectCategories_renamed'  # Main dataset directory
output_dir = 'annotations'  # Directory to save YOLO annotations
os.makedirs(output_dir, exist_ok=True)

# Loop through each category folder
for category_folder in os.listdir(images_dir):
    category_path = os.path.join(images_dir, category_folder)

    # Ensure we are only working with directories
    if os.path.isdir(category_path):
        # Create a corresponding output directory for each category
        category_output_dir = os.path.join(output_dir, category_folder)
        os.makedirs(category_output_dir, exist_ok=True)

        # Loop through each image in the category folder
        for image_name in os.listdir(category_path):
            image_path = os.path.join(category_path, image_name)
            if image_path.endswith(('.jpg', '.png', '.jpeg')):  # Filter image files
                results = model(image_path)  # Perform object detection

                # Get file name without extension
                base_name = os.path.splitext(image_name)[0]
                txt_file_path = os.path.join(category_output_dir, f"{base_name}.txt")

                # Write predictions to a YOLO-format text file
                with open(txt_file_path, 'w') as f:
                    for result in results:
                        boxes = result.boxes.xywhn.cpu().numpy()  # Get normalized bbox (x_center, y_center, width, height)
                        class_ids = result.boxes.cls.cpu().numpy()  # Get class IDs

                        for box, class_id in zip(boxes, class_ids):
                            x_center, y_center, width, height = box
                            f.write(f"{int(class_id)} {x_center} {y_center} {width} {height}\n")

                print(f"Annotation saved for {image_name} in {category_output_dir}")
