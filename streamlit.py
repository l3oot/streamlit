import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# ตั้งค่า style ของ seaborn
sns.set_style("whitegrid")
plt.style.use("ggplot")

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Advanced Graphs Demo", layout="wide")
st.title("การแสดงผลกราฟขั้นสูงด้วย Streamlit และ Matplotlib")

# สร้างข้อมูลตัวอย่าง
@st.cache_data
def generate_sample_data():
    # ข้อมูลยอดขายรายวัน
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    sales = np.random.normal(1000, 200, 90).cumsum()
    df_sales = pd.DataFrame({
        'วันที่': dates,
        'ยอดขาย': sales,
        'เป้าหมาย': sales * 1.1
    })
    
    # ข้อมูลสินค้าตามหมวดหมู่
    categories = ['อาหาร', 'เครื่องดื่ม', 'ขนม', 'ของใช้', 'เครื่องสำอาง']
    products = pd.DataFrame({
        'หมวดหมู่': categories,
        'ยอดขาย': np.random.randint(1000, 5000, len(categories)),
        'กำไร': np.random.randint(100, 1000, len(categories))
    })
    
    return df_sales, products

df_sales, products = generate_sample_data()

# สร้าง 2 คอลัมน์
col1, col2 = st.columns(2)

with col1:
    st.subheader("กราฟแนวโน้มยอดขาย")
    # สร้างกราฟเส้นแบบมีพื้นที่ใต้กราฟ
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.fill_between(df_sales['วันที่'], df_sales['ยอดขาย'], 
                   alpha=0.3, color='royalblue', label='พื้นที่ยอดขาย')
    ax.plot(df_sales['วันที่'], df_sales['ยอดขาย'], 
            color='royalblue', label='ยอดขายจริง')
    ax.plot(df_sales['วันที่'], df_sales['เป้าหมาย'], 
            '--', color='coral', label='เป้าหมาย')
    
    ax.set_title('ยอดขายเทียบกับเป้าหมาย')
    ax.set_xlabel('วันที่')
    ax.set_ylabel('ยอดขาย (บาท)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("การวิเคราะห์สินค้าแต่ละหมวดหมู่")
    # สร้าง scatter plot ด้วย seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=products, x='ยอดขาย', y='กำไร', 
                    size='ยอดขาย', sizes=(100, 1000),
                    hue='หมวดหมู่', ax=ax)
    
    # เพิ่ม label ให้แต่ละจุด
    for idx, row in products.iterrows():
        ax.annotate(row['หมวดหมู่'], 
                   (row['ยอดขาย'], row['กำไร']),
                   xytext=(5, 5), textcoords='offset points')
    
    ax.set_title('ความสัมพันธ์ระหว่างยอดขายและกำไรตามหมวดหมู่')
    plt.tight_layout()
    st.pyplot(fig)

# สร้างกราฟวงกลม
st.subheader("สัดส่วนยอดขายตามหมวดหมู่")
fig, ax = plt.subplots(figsize=(10, 6))
wedges, texts, autotexts = ax.pie(products['ยอดขาย'], 
                                 labels=products['หมวดหมู่'],
                                 autopct='%1.1f%%',
                                 textprops={'size': 'smaller'},
                                 wedgeprops={'width': 0.7})
ax.set_title('สัดส่วนยอดขายแต่ละหมวดหมู่')
plt.tight_layout()
st.pyplot(fig)

# สร้างกราฟ Distribution ด้วย Seaborn
st.subheader("การกระจายตัวของยอดขาย")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df_sales, x='ยอดขาย', bins=20, kde=True)
ax.set_title('การกระจายตัวของยอดขาย')
plt.tight_layout()
st.pyplot(fig)

# เพิ่มตัวกรองข้อมูล
st.sidebar.header("ตัวกรองข้อมูล")
date_range = st.sidebar.date_input(
    "เลือกช่วงวันที่",
    value=(df_sales['วันที่'].min(), df_sales['วันที่'].max())
)

# สถิติพื้นฐาน
st.sidebar.subheader("สถิติพื้นฐาน")
st.sidebar.metric("ยอดขายเฉลี่ย", f"{df_sales['ยอดขาย'].mean():,.0f} บาท")
st.sidebar.metric("ยอดขายสูงสุด", f"{df_sales['ยอดขาย'].max():,.0f} บาท")
st.sidebar.metric("ยอดขายต่ำสุด", f"{df_sales['ยอดขาย'].min():,.0f} บาท")

# แสดงข้อมูลดิบ
if st.checkbox("แสดงข้อมูลดิบ"):
    st.subheader("ข้อมูลยอดขายรายวัน")
    st.dataframe(df_sales)
    
    st.subheader("ข้อมูลสินค้าตามหมวดหมู่")
    st.dataframe(products)