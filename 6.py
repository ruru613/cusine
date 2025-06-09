import streamlit as st
from fastai.vision.all import *
import pathlib

@st.cache_resource
def load_model():
    model_path = pathlib.Path(__file__).parent / "doraemon_walle_model.pkl"
    return load_learner(model_path)

model = load_model()

st.title("Doraemon 与 Walle 分类器")
st.write("上传一张图片，看看它是 Doraemon 还是 Walle！")
uploaded_file = st.file_uploader("选择一张图片", type=["jpg", "jpeg", "png"])