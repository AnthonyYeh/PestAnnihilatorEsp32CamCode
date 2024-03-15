from inference.models.utils import get_roboflow_model
import cv2
from collections import namedtuple

model = get_roboflow_model(
    model_id="insects-detector/3",
    api_key="ToumOw2ArLdsofKlQMYQ"
)

def infer(image):
    infered=model.infer(image)[0].predictions
    ret_type=namedtuple("ret_type", "insect_type, confidence, x, y, width, height")
    return [ret_type(i.class_name, i.confidence, i.x, i.y, i.width, i.height) for i in infered]

#print(infer(cv2.imread(r"eco-pest-mgmt_0.jpg")))