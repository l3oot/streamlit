import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ตั้งค่า style ของ matplotlib
plt.style.use('default')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['figure.figsize'] = [10, 6]

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
        'เป้าหมาย': sales * 1.1,
        'ต้นทุน': sales * 0.6
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
    fig, ax = plt.subplots()
    
    # สร้างกราฟเส้นแบบมีพื้นที่ใต้กราฟ
    ax.fill_between(df_sales['วันที่'], df_sales['ยอดขาย'], 
                   df_sales['ต้นทุน'], alpha=0.3, 
                   color='lightblue', label='กำไรขั้นต้น')
    ax.plot(df_sales['วันที่'], df_sales['ยอดขาย'], 
            color='blue', label='ยอดขายจริง', linewidth=2)
    ax.plot(df_sales['วันที่'], df_sales['เป้าหมาย'], 
            '--', color='red', label='เป้าหมาย', linewidth=2)
    ax.plot(df_sales['วันที่'], df_sales['ต้นทุน'], 
            color='gray', label='ต้นทุน', linewidth=1)
    
    ax.set_title('ยอดขายเทียบกับเป้าหมาย')
    ax.set_xlabel('วันที่')
    ax.set_ylabel('ยอดขาย (บาท)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("การวิเคราะห์สินค้าแต่ละหมวดหมู่")
    fig, ax = plt.subplots()
    
    # สร้าง scatter plot
    sizes = products['ยอดขาย'] / 50  # ปรับขนาดจุดตามยอดขาย
    scatter = ax.scatter(products['ยอดขาย'], products['กำไร'], 
                        s=sizes, alpha=0.6, c=range(len(products)),
                        cmap='viridis')
    
    # เพิ่ม label ให้แต่ละจุด
    for idx, row in products.iterrows():
        ax.annotate(row['หมวดหมู่'], 
                   (row['ยอดขาย'], row['กำไร']),
                   xytext=(5, 5), textcoords='offset points')
    
    ax.set_title('ความสัมพันธ์ระหว่างยอดขายและกำไรตามหมวดหมู่')
    ax.set_xlabel('ยอดขาย (บาท)')
    ax.set_ylabel('กำไร (บาท)')
    plt.tight_layout()
    st.pyplot(fig)

# สร้างกราฟวงกลม
st.subheader("สัดส่วนยอดขายตามหมวดหมู่")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Pie chart
wedges, texts, autotexts = ax1.pie(products['ยอดขาย'], 
                                  labels=products['หมวดหมู่'],
                                  autopct='%1.1f%%',
                                  textprops={'size': 'smaller'},
                                  colors=plt.cm.Pastel1(np.linspace(0, 1, len(products))))
ax1.set_title('สัดส่วนยอดขาย')

# Bar chart
bars = ax2.bar(products['หมวดหมู่'], products['ยอดขาย'],
               color=plt.cm.Pastel1(np.linspace(0, 1, len(products))))
ax2.set_title('ยอดขายตามหมวดหมู่')
ax2.tick_params(axis='x', rotation=45)
ax2.set_ylabel('ยอดขาย (บาท)')

# เพิ่มค่าตัวเลขบน bar
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom')

plt.tight_layout()
st.pyplot(fig)

# สร้างกราฟการกระจายตัว
st.subheader("การกระจายตัวของยอดขาย")
fig, ax = plt.subplots()

# สร้าง histogram
n, bins, patches = ax.hist(df_sales['ยอดขาย'], bins=20, 
                          density=True, alpha=0.7,
                          color='skyblue', edgecolor='black')

# คำนวณและพล็อต normal distribution
mu = df_sales['ยอดขาย'].mean()
sigma = df_sales['ยอดขาย'].std()
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
y = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu)**2 / (2 * sigma**2))
ax.plot(x, y, 'r-', lw=2, label='Normal Distribution')

ax.set_title('การกระจายตัวของยอดขาย')
ax.set_xlabel('ยอดขาย (บาท)')
ax.set_ylabel('ความถี่')
ax.legend()
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
st.sidebar.metric("ส่วนเบี่ยงเบนมาตรฐาน", f"{df_sales['ยอดขาย'].std():,.0f} บาท")

# แสดงข้อมูลดิบ
if st.checkbox("แสดงข้อมูลดิบ"):
    st.subheader("ข้อมูลยอดขายรายวัน")
    st.dataframe(df_sales)
    
    st.subheader("ข้อมูลสินค้าตามหมวดหมู่")
    st.dataframe(products)