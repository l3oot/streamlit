import streamlit as st

# Title and header
st.title("แอปพลิเคชันตัวอย่างด้วย Streamlit")
st.header("ยินดีต้อนรับ!")

# Text input
name = st.text_input("กรุณากรอกชื่อของคุณ:")

# Select box
favorite_color = st.selectbox("เลือกสีที่คุณชอบ:", ["แดง", "เขียว", "น้ำเงิน"])

# Slider
age = st.slider("อายุของคุณ:", 0, 100, 25)

# Button
if st.button("ยืนยัน"):
    st.write(f"สวัสดี {name}!")
    st.write(f"คุณชอบสี {favorite_color} และคุณอายุ {age} ปี!")

# File uploader
uploaded_file = st.file_uploader("อัปโหลดไฟล์ (ถ้ามี):")
if uploaded_file is not None:
    st.write("ไฟล์ที่คุณอัปโหลด:", uploaded_file.name)

# Data visualization example
import pandas as pd
import numpy as np

data = pd.DataFrame(
    np.random.randn(10, 2),
    columns=['X', 'Y']
)

st.line_chart(data)
