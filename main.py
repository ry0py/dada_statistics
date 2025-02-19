# streamlitを使用して基本的なレイアウトをすべて書いて

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import easyocr
import pytesseract
import re

reader = easyocr.Reader(['ja','en'])
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
    img = np.array(Image.open(uploaded_file))
    # imgの幅と高さを取得
    st.write("Image shape:", img.shape)
    hand_crop = img[600:2100, 60:1130]
    st.image(hand_crop, caption="Hand region")
    result = reader.readtext(np.array(hand_crop))
    for (bbox, text, prob) in result:
        st.write(text)
