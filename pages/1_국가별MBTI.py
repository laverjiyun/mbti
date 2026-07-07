import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 MBTI 현황", layout="wide")

st.title("🔍 국가별 MBTI 분포 현황")
st.markdown("---")

try:
    df = pd.read_csv("countries_mbti.csv")
    
    # 국가 선택 박스
    countries = df["Country"].unique()
    selected_country = st.selectbox("🌐 분석할 국가를 선택하세요:", countries)
    
    # 선택된 국가 데이터 추출
    country_data = df[df["Country"] == selected_country].drop(columns=["Country"]).T
    country_data.columns = ["Ratio"]
    country_data = country_data.sort_values(by="Ratio", ascending=False)
    
    # 시각화 레이아웃 분할
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write(f"### 📊 {selected_country}의 MBTI 순위")
        st.dataframe(country_data, use_container_width=True)
        
    with col2:
        st.write(f"### 📈 {selected_country}의 MBTI 분포 차트")
        # 막대 그래프 그리기
        fig = px.bar(
            country_data, 
            x=country_data.index, 
            y="Ratio", 
            labels={"index": "MBTI 유형", "Ratio": "비율"},
            color="Ratio",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다.")
