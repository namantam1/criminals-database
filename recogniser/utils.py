import dlib
from django.conf import settings
import numpy as np
from PIL import Image


BASE_DIR = settings.BASE_DIR
# BASE_DIR = ""

predictor_path = (
    str(BASE_DIR) + "/recogniser/trained_models/shape_predictor_5_face_landmarks.dat"
)
face_rec_model_path = (
    str(BASE_DIR)
    + "/recogniser/trained_models/dlib_face_recognition_resnet_model_v1.dat"
)

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face, and finally the
# face recognition model.
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(predictor_path)
face_recogniser = dlib.face_recognition_model_v1(face_rec_model_path)


def encode(img):
    img = np.array(Image.open(img).convert("RGB"))
    detected_faces = face_detector(img, 1)
    faces_shape = map(lambda loc: shape_predictor(img, loc), detected_faces)
    embeddings = map(
        lambda shape: face_recogniser.compute_face_descriptor(img, shape), faces_shape
    )
    embeddings = list(embeddings)

    assert len(embeddings) > 0, f"No face detected in {img}"
    return embeddings
