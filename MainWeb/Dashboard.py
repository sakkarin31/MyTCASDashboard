import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Thai University Computer Engineering Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .university-highlight {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process the university data"""
    # Read the CSV file
    df = pd.read_csv('MainData.csv')
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Convert fee to numeric, handling any formatting issues
    df['fee/term'] = pd.to_numeric(df['fee/term'], errors='coerce')
    
    # Convert admission rounds to numeric, replacing '-' with 0
    admission_cols = ['r1', 'r2', 'r3', 'r4']
    for col in admission_cols:
        df[col] = df[col].replace('-', 0)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Calculate total admission slots
    df['total_admission'] = df[admission_cols].sum(axis=1)
    
    # Categorize universities by type
    def categorize_university(name):
        if 'จุฬาลงกรณ์' in name or 'เกษตรศาสตร์' in name or 'เชียงใหม่' in name or 'ขอนแก่น' in name or 'สงขลานครินทร์' in name:
            return 'มหาวิทยาลัยชั้นนำ'
        elif 'เทคโนโลยี' in name or 'สถาบัน' in name:
            return 'สถาบันเทคโนโลยี'
        elif 'ราชภัฏ' in name or 'รามคำแหง' in name:
            return 'มหาวิทยาลัยราชภัฏ/เปิด'
        else:
            return 'มหาวิทยาลัยเอกชน'
    
    df['university_type'] = df['university'].apply(categorize_university)
    
    return df

def main():
    st.markdown('<h1 class="main-header">🎓 Thai University Computer Engineering Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">เลือกมหาวิทยาลัยที่เหมาะกับคุณ สำหรับปีการศึกษาถัดไป</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 ตัวกรองข้อมูล")
    
    # Fee range filter
    min_fee, max_fee = st.sidebar.slider(
        "ช่วงค่าเทอม (บาท)",
        min_value=int(df['fee/term'].min()),
        max_value=int(df['fee/term'].max()),
        value=(int(df['fee/term'].min()), int(df['fee/term'].max())),
        step=1000
    )
    
    # University type filter
    university_types = st.sidebar.multiselect(
        "ประเภทมหาวิทยาลัย",
        options=df['university_type'].unique(),
        default=df['university_type'].unique()
    )
    
    # Minimum admission slots filter
    min_admission = st.sidebar.number_input(
        "จำนวนที่รับขั้นต่ำ",
        min_value=0,
        max_value=int(df['total_admission'].max()),
        value=0
    )
    
    # Filter data
    filtered_df = df[
        (df['fee/term'] >= min_fee) & 
        (df['fee/term'] <= max_fee) &
        (df['university_type'].isin(university_types)) &
        (df['total_admission'] >= min_admission)
    ]
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📚 จำนวนหลักสูตร",
            value=len(filtered_df),
            delta=f"{len(filtered_df)}/{len(df)} หลักสูตร"
        )
    
    with col2:
        avg_fee = filtered_df['fee/term'].mean()
        st.metric(
            label="💰 ค่าเทอมเฉลี่ย",
            value=f"฿{avg_fee:,.0f}",
            delta=f"ต่อเทอม"
        )
    
    with col3:
        total_slots = filtered_df['total_admission'].sum()
        st.metric(
            label="🎯 ที่รับทั้งหมด",
            value=f"{total_slots:,}",
            delta="คน"
        )
    
    with col4:
        avg_slots = filtered_df['total_admission'].mean()
        st.metric(
            label="📊 ที่รับเฉลี่ย/หลักสูตร",
            value=f"{avg_slots:.0f}",
            delta="คน"
        )
    
    # Charts section
    st.markdown("---")
    
    # Fee vs Admission Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 การกระจายค่าเทอมตามประเภทมหาวิทยาลัย")
        
        fig_box = px.box(
            filtered_df, 
            x='university_type', 
            y='fee/term',
            color='university_type',
            title="ช่วงค่าเทอมแต่ละประเภทมหาวิทยาลัย"
        )
        fig_box.update_layout(
            xaxis_title="ประเภทมหาวิทยาลัย",
            yaxis_title="ค่าเทอม (บาท)",
            showlegend=False
        )
        fig_box.update_xaxes(tickangle=45)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        st.subheader("🎯 จำนวนที่รับแต่ละรอบ")
        
        # Prepare data for admission rounds
        admission_data = filtered_df[['r1', 'r2', 'r3', 'r4']].sum()
        
        fig_pie = px.pie(
            values=admission_data.values,
            names=['รอบที่ 1', 'รอบที่ 2', 'รอบที่ 3', 'รอบที่ 4'],
            title="สัดส่วนการรับนักศึกษาแต่ละรอบ"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Scatter plot: Fee vs Total Admission
    st.subheader("📈 ความสัมพันธ์ระหว่างค่าเทอมและจำนวนที่รับ")
    
    fig_scatter = px.scatter(
        filtered_df,
        x='fee/term',
        y='total_admission',
        color='university_type',
        size='total_admission',
        hover_data=['university', 'program_name'],
        title="ค่าเทอม vs จำนวนที่รับ (ขนาดจุด = จำนวนที่รับ)"
    )
    fig_scatter.update_layout(
        xaxis_title="ค่าเทอม (บาท)",
        yaxis_title="จำนวนที่รับรวม (คน)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Top universities by different criteria
    st.markdown("---")
    st.subheader("🏆 อันดับมหาวิทยาลัย")
    
    tab1, tab2 = st.tabs(["💰 ค่าเทอมต่ำสุด", "🎯 รับมากที่สุด"])
    
    with tab1:
        cheapest = filtered_df.nsmallest(10, 'fee/term')[['university', 'program_name', 'fee/term', 'total_admission']]
        cheapest['fee/term'] = cheapest['fee/term'].apply(lambda x: f"฿{x:,.0f}")
        st.dataframe(cheapest, use_container_width=True, hide_index=True)
    
    with tab2:
        most_admission = filtered_df.nlargest(10, 'total_admission')[['university', 'program_name', 'fee/term', 'total_admission']]
        most_admission['fee/term'] = most_admission['fee/term'].apply(lambda x: f"฿{x:,.0f}")
        st.dataframe(most_admission, use_container_width=True, hide_index=True)
    
    # Detailed university table
    st.markdown("---")
    st.subheader("📋 ตารางข้อมูลรายละเอียด")
    
    # Prepare display dataframe
    display_df = filtered_df[['university', 'faculty', 'program_name', 'fee/term', 'r1', 'r2', 'r3', 'r4', 'total_admission', 'university_type']].copy()
    display_df['fee/term'] = display_df['fee/term'].apply(lambda x: f"฿{x:,.0f}")
    display_df = display_df.rename(columns={
        'university': 'มหาวิทยาลัย',
        'faculty': 'คณะ',
        'program_name': 'หลักสูตร',
        'fee/term': 'ค่าเทอม',
        'r1': 'รอบ1',
        'r2': 'รอบ2', 
        'r3': 'รอบ3',
        'r4': 'รอบ4',
        'total_admission': 'รวม',
        'university_type': 'ประเภท'
    })
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "มหาวิทยาลัย": st.column_config.TextColumn(width="large"),
            "หลักสูตร": st.column_config.TextColumn(width="large"),
        }
    )
    
    # Summary insights
    st.markdown("---")
    st.subheader("💡 ข้อมูลเชิงลึก")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 สำหรับนักเรียนที่เตรียมสมัคร:")
        # Find round with minimum admission
        round_sums = filtered_df[['r1', 'r2', 'r3', 'r4']].sum()
        min_round_col = round_sums.idxmin()
        round_number = min_round_col[-1]  # Get the number from 'r1', 'r2', etc.
        
        insights = f"""
        - **มหาวิทยาลัยที่มีค่าเทอมต่ำสุด:** {filtered_df.loc[filtered_df['fee/term'].idxmin(), 'university']} (฿{filtered_df['fee/term'].min():,.0f})
        - **มหาวิทยาลัยที่รับมากที่สุด:** {filtered_df.loc[filtered_df['total_admission'].idxmax(), 'university']} ({filtered_df['total_admission'].max()} คน)
        - **รอบที่มีที่รับน้อยที่สุด:** รอบที่ {round_number} ({round_sums.min()} คน)
        - **ช่วงราคาที่พบมาก:** ฿{filtered_df['fee/term'].quantile(0.25):,.0f} - ฿{filtered_df['fee/term'].quantile(0.75):,.0f}
        """
        st.markdown(insights)
    
    with col2:
        st.markdown("### 📊 สถิติที่น่าสนใจ:")
        stats = f"""
        - **จำนวนมหาวิทยาลัยรัฐ:** {len(filtered_df[filtered_df['university_type'].isin(['มหาวิทยาลัยชั้นนำ', 'สถาบันเทคโนโลยี', 'มหาวิทยาลัยราชภัฏ/เปิด'])])} แห่ง
        - **จำนวนมหาวิทยาลัยเอกชน:** {len(filtered_df[filtered_df['university_type'] == 'มหาวิทยาลัยเอกชน'])} แห่ง
        - **ค่าเทอมเฉลี่ยรัฐ:** ฿{filtered_df[filtered_df['university_type'] != 'มหาวิทยาลัยเอกชน']['fee/term'].mean():,.0f}
        - **ค่าเทอมเฉลี่ยเอกชน:** ฿{filtered_df[filtered_df['university_type'] == 'มหาวิทยาลัยเอกชน']['fee/term'].mean():,.0f}
        """
        st.markdown(stats)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>📚 ข้อมูลสำหรับการตัดสินใจเลือกเรียนต่อ | 🎓 ปีการศึกษา 2025</p>
            <p><small>หมายเหตุ: ข้อมูลอาจมีการเปลี่ยนแปลง กรุณาตรวจสอบกับมหาวิทยาลัยโดยตรง</small></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()