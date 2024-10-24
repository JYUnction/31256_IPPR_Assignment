import cv2
import os
import numpy as np

# Load YOLO model
net = cv2.dnn.readNet('yolov4-csp-swish.weights', 'yolov4-csp-swish.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Directory containing Caltech 256 dataset images
image_dir = '256_ObjectCategories'
output_dir = 'annotations'  # Directory to save annotations
os.makedirs(output_dir, exist_ok=True)

# Loop over each class folder in Caltech 256
for class_folder in os.listdir(image_dir):
    class_path = os.path.join(image_dir, class_folder)
    
    # Ensure we are only working with directories (class folders)
    if os.path.isdir(class_path):
        print(f"Processing class: {class_folder}")
        
        # Loop over each image in the class folder
        for filename in os.listdir(class_path):
            if filename.endswith('.jpg'):
                img_path = os.path.join(class_path, filename)
                img = cv2.imread(img_path)
                
                if img is None:
                    print(f"Could not read image: {img_path}")
                    continue
                
                height, width = img.shape[:2]

                # Prepare the image for YOLO
                blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(output_layers)

                # Initialize lists to hold predictions
                class_ids = []
                confidences = []
                boxes = []

                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        pred_class_id = np.argmax(scores)
                        confidence = scores[pred_class_id]
                        if confidence > 0.5:  # Confidence threshold
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)

                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(pred_class_id)

                # Apply Non-Maximum Suppression (NMS)
                indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

                # Check if indices is not empty
                if len(indices) > 0:
                    for i in indices:
                        # Access the scalar index
                        i = i[0] if isinstance(i, (list, np.ndarray)) else i

                        box = boxes[i]
                        x, y, w, h = box

                        # Normalize the bounding box coordinates
                        x_center = (x + w / 2) / width
                        y_center = (y + h / 2) / height
                        w_norm = w / width
                        h_norm = h / height

                        # Save in YOLO format: class_id x_center y_center width height
                        annotation_path = os.path.join(output_dir, filename.replace('.jpg', '.txt'))
                        with open(annotation_path, 'w') as f:
                            f.write(f"{class_ids[i]} {x_center} {y_center} {w_norm} {h_norm}\n")
                else:
                    print(f"No valid boxes after NMS for {filename}")
