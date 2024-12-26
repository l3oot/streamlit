import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# HTML ส่วนหัว
st.markdown("""
    <h1 style="color:blue; text-align:center;">Streamlit + HTML + Matplotlib</h1>
    <p style="text-align:center; font-size:18px;">นี่คือการใช้ HTML ร่วมกับ Streamlit และกราฟจาก Matplotlib</p>
""", unsafe_allow_html=True)

# สร้างข้อมูลสำหรับกราฟ
x = np.linspace(0, 10, 100)
y = np.sin(x)

# สร้างกราฟ Matplotlib
fig, ax = plt.subplots()
ax.plot(x, y, label="Sine Wave", color="blue")
ax.set_title("Sine Wave Example")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.legend()

# แสดงกราฟใน Streamlit
st.pyplot(fig)

# HTML ส่วนท้าย
st.markdown("""
    <hr>
    <p style="text-align:center;">กราฟถูกสร้างด้วย <b>Matplotlib</b> และแสดงผลใน Streamlit</p>
    <p style="text-align:center;"><i>Powered by Streamlit</i></p>
""", unsafe_allow_html=True)
