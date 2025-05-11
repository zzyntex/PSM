import cv2
import pyautogui
import numpy as np
import tensorflow as tf
import csv
import mediapipe as mp
from collections import deque
from app import KeyPointClassifier  # Assuming this is the trained model class
from utils import CvFpsCalc
from google.protobuf.json_format import MessageToDict
from model import KeyPointClassifier
from model import PointHistoryClassifier

# Load the trained model
model_path = 'model/keypoint_classifier/keypoint_classifier.keras'  # Adjust this path if needed
model = tf.keras.models.load_model(model_path)

# Load gesture labels (the same labels used during model training)
gesture_labels_path = 'model/keypoint_classifier/keypoint_classifier_label.csv'  # Adjust the path if needed
gesture_labels = []
with open(gesture_labels_path, 'r') as f:
    reader = csv.reader(f)
    gesture_labels = [row[0] for row in reader]

# Gesture-action mapping (you can modify these actions as per your needs)
gesture_actions = {
    "Open": pyautogui.hotkey('ctrl', 'o'),  # Example: Open a file
    "Close": pyautogui.hotkey('alt', 'f4'),  # Example: Close the active window
    "Pointer": pyautogui.click(),  # Example: Click
    "OK": pyautogui.press('enter'),  # Example: Press Enter key
    "Peace Sign": pyautogui.hotkey('ctrl', 'w'),  # Example: Close browser tab
    "Rock": pyautogui.hotkey('ctrl', 't'),  # Example: Open a new tab in browser
}

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Preprocess the keypoints from the camera feed for classification
def preprocess_keypoints(landmark_list):
    temp_landmark_list = np.array(landmark_list)
    base_x, base_y = temp_landmark_list[0][0], temp_landmark_list[0][1]
    temp_landmark_list -= [base_x, base_y]
    
    # Normalize the landmarks
    max_value = np.max(np.abs(temp_landmark_list))
    normalized_landmarks = temp_landmark_list / max_value
    
    return normalized_landmarks.flatten()  # Flatten to a 1D array

# Gesture control part to replace the existing logic
class GestureController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def classify_gesture(self, landmarks):
        # Preprocess the landmarks
        processed_landmarks = preprocess_keypoints(landmarks)

        # Predict gesture using the trained model
        gesture_id = np.argmax(model.predict(np.array([processed_landmarks])))

        # Map the gesture ID to the corresponding gesture name
        gesture_name = gesture_labels[gesture_id]
        print(f"Detected gesture: {gesture_name}")

        # Trigger action based on the gesture name
        if gesture_name in gesture_actions:
            print(f"Triggering action for gesture: {gesture_name}")
            gesture_actions[gesture_name]  # Perform the action

    def start(self):
        with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
            while self.cap.isOpened():
                success, image = self.cap.read()

                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                        
                        # Classify gesture
                        self.classify_gesture(landmarks)

                        # Draw landmarks
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                cv2.imshow('Gesture Controller', image)
                if cv2.waitKey(5) & 0xFF == 13:
                    break

        self.cap.release()
        cv2.destroyAllWindows()

# Entry point for Gesture Controller
gc = GestureController()
gc.start()
