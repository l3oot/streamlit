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

# Custom CSS and HTML
st.markdown("""
<style>
    .dashboard-container {
        padding: 20px;
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .graph-container {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .title-text {
        color: #2c3e50;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .subtitle-text {
        color: #34495e;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .stat-box {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .sidebar {
        padding: 20px;
        background: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# สร้างข้อมูลตัวอย่าง (ใช้ฟังก์ชันเดิม)
@st.cache_data
def generate_sample_data():
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    sales = np.random.normal(1000, 200, 90).cumsum()
    df_sales = pd.DataFrame({
        'วันที่': dates,
        'ยอดขาย': sales,
        'เป้าหมาย': sales * 1.1
    })
    
    categories = ['อาหาร', 'เครื่องดื่ม', 'ขนม', 'ของใช้', 'เครื่องสำอาง']
    products = pd.DataFrame({
        'หมวดหมู่': categories,
        'ยอดขาย': np.random.randint(1000, 5000, len(categories)),
        'กำไร': np.random.randint(100, 1000, len(categories))
    })
    
    return df_sales, products

df_sales, products = generate_sample_data()

# สร้าง HTML Layout
st.markdown("""
<div class="dashboard-container">
    <div class="title-text">แดชบอร์ดวิเคราะห์ยอดขาย</div>
</div>
""", unsafe_allow_html=True)

# สร้างคอลัมน์สำหรับกราฟ
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">กราฟแนวโน้มยอดขาย</div>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">การวิเคราะห์สินค้าแต่ละหมวดหมู่</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=products, x='ยอดขาย', y='กำไร', 
                    size='ยอดขาย', sizes=(100, 1000),
                    hue='หมวดหมู่', ax=ax)
    for idx, row in products.iterrows():
        ax.annotate(row['หมวดหมู่'], 
                   (row['ยอดขาย'], row['กำไร']),
                   xytext=(5, 5), textcoords='offset points')
    ax.set_title('ความสัมพันธ์ระหว่างยอดขายและกำไรตามหมวดหมู่')
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# สร้างแถวใหม่สำหรับกราฟล่าง
st.markdown('<div class="graph-container">', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">สัดส่วนยอดขายตามหมวดหมู่</div>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10, 6))
wedges, texts, autotexts = ax.pie(products['ยอดขาย'], 
                                 labels=products['หมวดหมู่'],
                                 autopct='%1.1f%%',
                                 textprops={'size': 'smaller'},
                                 wedgeprops={'width': 0.7})
ax.set_title('สัดส่วนยอดขายแต่ละหมวดหมู่')
plt.tight_layout()
st.pyplot(fig)
st.markdown('</div>', unsafe_allow_html=True)

# สถิติพื้นฐานในรูปแบบ card
st.markdown("""
<div class="stats-container">
    <div class="stat-box">
        <h3>ยอดขายเฉลี่ย</h3>
        <p>{:,.0f} บาท</p>
    </div>
    <div class="stat-box">
        <h3>ยอดขายสูงสุด</h3>
        <p>{:,.0f} บาท</p>
    </div>
    <div class="stat-box">
        <h3>ยอดขายต่ำสุด</h3>
        <p>{:,.0f} บาท</p>
    </div>
</div>
""".format(
    df_sales['ยอดขาย'].mean(),
    df_sales['ยอดขาย'].max(),
    df_sales['ยอดขาย'].min()
), unsafe_allow_html=True)

# Sidebar with filters
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.header("ตัวกรองข้อมูล")
    date_range = st.date_input(
        "เลือกช่วงวันที่",
        value=(df_sales['วันที่'].min(), df_sales['วันที่'].max())
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Toggle for raw data
if st.checkbox("แสดงข้อมูลดิบ"):
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">ข้อมูลยอดขายรายวัน</div>', unsafe_allow_html=True)
    st.dataframe(df_sales)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">ข้อมูลสินค้าตามหมวดหมู่</div>', unsafe_allow_html=True)
    st.dataframe(products)
    st.markdown('</div>', unsafe_allow_html=True)