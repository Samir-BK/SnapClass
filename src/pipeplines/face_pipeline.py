


import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

st.cache_resource # makes load only one time
def load_dib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerocg = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerocg


def get_face_embeddings(image_np):
    detector, sp, facerocg = load_dib_models()
    faces = detector(image_np,2)

    encoding = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerocg.compute_face_descriptor(image_np, shape, 1) # 128 embeddings

        encoding.append(np.array(face_descriptor))