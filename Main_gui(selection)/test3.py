import cv2
from ultralytics import YOLO

# Function to load model paths from a text file
def load_model_paths(file_path):
    with open(file_path, 'r') as f:
        paths = f.readlines()
    return [path.strip() for path in paths]

# Load model paths from the text file
model_paths = load_model_paths('model_path.txt')

# Load the models
models = [YOLO(path) for path in model_paths]

# Function to perform object detection on a frame using the models
def detect_objects(frame):
    results = []
    for model in models:
        results.append(model(frame))
    return results

def process_frame(frame):
    # Detect objects in the frame using both models
    detection_results = detect_objects(frame)

    class_counts = {}
    confidence_threshold = 0.6

    # Draw results from both models on the frame
    for i, result in enumerate(detection_results):
        for r in result:
            boxes = r.boxes.xyxy.cpu().numpy()  # Get boxes coordinates
            confs = r.boxes.conf.cpu().numpy()  # Get confidence scores
            clss = r.boxes.cls.cpu().numpy()  # Get class IDs

            for box, conf, cls in zip(boxes, confs, clss):
                if conf >= confidence_threshold:
                    label = f"{models[i].names[int(cls)]} {conf:.2f}"  # Use models[i] instead of model
                    color = (0, 255, 0) if i == 0 else (255, 0, 0)  # Green for first model, Blue for second
                    cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)
                    cv2.putText(frame, label, (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    # Update class counts
                    class_name = models[i].names[int(cls)]
                    if class_name in class_counts:
                        class_counts[class_name] += 1
                    else:
                        class_counts[class_name] = 1

    return frame, class_counts
