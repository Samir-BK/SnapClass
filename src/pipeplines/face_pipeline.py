


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

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerocg.compute_face_descriptor(image_np, shape, 1) # 128 embeddings

        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embeding = student.get("face_embedding")
        if embeding:
            X.append(np.array(embeding))
            y.append(student.get("student_id"))
    if len(X) == 0:
        return 0

    clf = SVC(kernel="linear", probability=True, class_weight="balanced")

    try:
        clf.fit(X, y)
    except ValueError:
        pass
