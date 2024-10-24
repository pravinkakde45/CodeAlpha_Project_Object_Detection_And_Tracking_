import cv2
import numpy as np

# Load YOLO
net = cv2.dnn.readNet('yolov3-tiny.weights', 'yolov3-tiny.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load COCO class names
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Load image
img = cv2.imread('your_image.jpg')  # Change this to your image file path
height, width, channels = img.shape

# Prepare the image for YOLO
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)

# Showing information on the screen
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:  # Confidence threshold
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Draw rectangle
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label = str(classes[class_id])
            cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

# Display image with detections
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
