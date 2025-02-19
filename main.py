# streamlitを使用して基本的なレイアウトをすべて書いて

import streamlit as st
import numpy as np
import pandas as pd

st.title('Streamlit 超入門')
st.write("Hello from Streamlit!")

left_col, right_col = st.columns(2)
left_col.write("Left column content")
right_col.write("Right column content")

st.sidebar.header("Sidebar")
st.sidebar.write("Sidebar content")
