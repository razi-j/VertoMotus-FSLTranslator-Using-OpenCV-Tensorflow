import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import os

class VM: 
    mp_holistic = mp.solutions.holistic
    mp_draw = mp.solutions.drawing_utils
    DATA_PATH = os.path.join("Model_Data")

    fsl = np.array(["hello"]) #things to put here: asl words, phrases
    seq = 30 # number of videos to be used for data collection
    seq_lenght = 30 # number of frames to be used per video

    def build_folder():
        for a in VM.fsl:
            for sequences in range(VM.seq):
                try:
                    os.makedirs(os.path.join(VM.DATA_PATH, a, str(sequences)))
                except:
                    pass


    def point_detection(image, model): #image from cv; holistic model from mp
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB) #process color and flip
        image.flags.writeable = False
        results = model.process(image)
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        return image, results

    def draw_points(image, results):
        VM.mp_draw.draw_landmarks(image, results.right_hand_landmarks, VM.mp_holistic.HAND_CONNECTIONS)
        VM.mp_draw.draw_landmarks(image, results.left_hand_landmarks, VM.mp_holistic.HAND_CONNECTIONS)
        VM.mp_draw.draw_landmarks(image, results.face_landmarks, VM.mp_holistic.FACEMESH_TESSELATION)
        VM.mp_draw.draw_landmarks(image, results.pose_landmarks, VM.mp_holistic.POSE_CONNECTIONS)

    def draw_styled_points(image, results):
        VM.mp_draw.draw_landmarks(image, results.right_hand_landmarks, VM.mp_holistic.HAND_CONNECTIONS,
                                VM.mp_draw.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=3),#landmark color
                                VM.mp_draw.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=1))#connection color

        VM.mp_draw.draw_landmarks(image, results.left_hand_landmarks, VM.mp_holistic.HAND_CONNECTIONS,
                                VM.mp_draw.DrawingSpec(color=(84, 44, 44), thickness=2, circle_radius=3),
                                VM.mp_draw.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=1))
        
        VM.mp_draw.draw_landmarks(image, results.face_landmarks, VM.mp_holistic.FACEMESH_TESSELATION,
                                VM.mp_draw.DrawingSpec(color=(255,170,170), thickness=1, circle_radius=1),
                                VM.mp_draw.DrawingSpec(color=(255,255,255), thickness=1, circle_radius=1))
        
        VM.mp_draw.draw_landmarks(image, results.pose_landmarks, VM.mp_holistic.POSE_CONNECTIONS,
                            VM.mp_draw.DrawingSpec(color=(42,43,42), thickness=2, circle_radius=3),
                            VM.mp_draw.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=1))
        
    def extract_keypoints(results):
        # list comprehension to loop over results and get needed data, then arranged to np.array. flattened to turn it into one array. else is to make a placeholder
        pose = np.array([[res.x,res.y,res.z,res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        lh = np.array([[res.x,res.y,res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x,res.y,res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        face = np.array([[res.x,res.y,res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
        
        # puts all data into one array
        a = np.concatenate([lh, rh, pose, face])
        return a

