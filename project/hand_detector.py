import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request

class HandDetector:
    def __init__(self, model_path="hand_landmarker.task"):
        self.model_path = model_path
        self._ensure_model_exists()
        
        # Initialize the Hand Landmarker
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            running_mode=vision.RunningMode.IMAGE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.latest_result = None

    def _ensure_model_exists(self):
        if not os.path.exists(self.model_path):
            print(f"Baixando modelo MediaPipe: {self.model_path}...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            urllib.request.urlretrieve(url, self.model_path)
            print("Download concluído.")

    def find_hands(self, img, draw=True):
        # Convert BGR to RGB (MediaPipe requirement)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        # Process the image
        self.latest_result = self.detector.detect(mp_image)
        
        if draw and self.latest_result.hand_landmarks:
            self._draw_landmarks(img)
            
        return img

    def _draw_landmarks(self, img):
        # MediaPipe Tasks doesn't have a direct drawing util like solutions, 
        # so we implement a simple one or use the legacy one if available via solutions (unlikely in 3.14)
        # However, for simplicity and compatibility, we'll draw manual circles/lines
        h, w, _ = img.shape
        for hand_landmarks in self.latest_result.hand_landmarks:
            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
            
            # Simple line connections for presentation
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4), # thumb
                (0, 5), (5, 6), (6, 7), (7, 8), # index
                (5, 9), (9, 10), (10, 11), (11, 12), # middle
                (9, 13), (13, 14), (14, 15), (15, 16), # ring
                (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # pinky
            ]
            for start_idx, end_idx in connections:
                start = hand_landmarks[start_idx]
                end = hand_landmarks[end_idx]
                cv2.line(img, (int(start.x * w), int(start.y * h)), 
                         (int(end.x * w), int(end.y * h)), (0, 255, 0), 2)

    def get_landmarks(self, img):
        lm_list = []
        if self.latest_result and self.latest_result.hand_landmarks:
            h, w, _ = img.shape
            # Get the first hand detected
            first_hand = self.latest_result.hand_landmarks[0]
            for id, landmark in enumerate(first_hand):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                lm_list.append([id, cx, cy, landmark.z])
        return lm_list
