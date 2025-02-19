# streamlitを使用して基本的なレイアウトをすべて書いて

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import pytesseract
import re


st.title('Streamlit 超入門')
st.write("Hello from Streamlit!")

left_col, right_col = st.columns(2)
left_col.write("Left column content")
right_col.write("Right column content")

st.sidebar.header("Sidebar")
st.sidebar.write("Sidebar content")
# 画像をアップロードする
uploaded_file = st.file_uploader("Choose an image...", type="jpg, png")
if uploaded_file is not None:
    data = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # imgの幅と高さを取得
    st.write("Image shape:", img.shape)
    hand_crop = img[600:2100, 60:1130]
    st.image(hand_crop, caption="Hand region")
    # extracted_text = pytesseract.image_to_string(hand_crop, lang='eng')
    # name_match = re.search(r'[A-Za-z]+', extracted_text)
    # number_match = re.findall(r'\d+', extracted_text)
    # st.write("Name:", name_match.group(0) if name_match else "N/A")
    # st.write("Numbers:", number_match if number_match else "N/A")
    # st.image(hand_crop, caption="Hand region")
