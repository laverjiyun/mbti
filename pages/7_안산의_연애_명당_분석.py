import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="솔로대첩 명당 분석", layout="wide")

st.title("👫 소개팅 매칭 확률 UP! 안산의 '솔로대첩' 명당 동네는?")
st.markdown("---")

try:
    df = pd.read_csv("population.csv")
    
    st.markdown("""
    💡 **분석 컨셉:** 동네별 남녀 인구 비율을 분석합니다! 
    **남녀 성비(남자÷여자)가 완벽하게 1에 가까워 커플 매칭 확률이 높은 평화로운 동네**를 찾거나, 
    반대로 극단적인 남초/여초 현상으로 '공대' 혹은 '여대' 같은 분위기를 풍기는 액티비티한 동네를 추려봅니다.
    """)
    
    # 최신 2025년 데이터 기준
    df_2025 = df[df['연도'] == 2025].copy()
    
    # 성비 계산 (여성 100명당 남성 수 지표 개념 혹은 단순 비율)
    df_2025['성비(남/여)'] = (df_2025['남자'] / df_2025['여자']).round(3)
    df_2025['성비_균형도'] = (df_2025['성비(남/여)'] - 1).abs() # 0에 가까울수록 황금밸런스
    
    mode = st.radio("확인하고 싶은 솔로대첩 지표를 고르세요:", ["남녀 비율이 황금 밸런스인 동네 (소개팅 명당)", "남초 성향이 가장 강한 동네", "여초 성향이 가장 강한 동네"])
    
    if mode == "남녀 비율이 황금 밸런스인 동네 (소개팅 명당)":
        # 균형도가 0에 가까운 순서
        match_town = df_2025.sort_values(by='성비_균형도', ascending=True).head(10)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("### 🏆 남녀 비율 1:1 황금동네 Top 10")
            st.dataframe(match_town[['구', '행정동', '남자', '여자', '성비(남/여)']].reset_index(drop=True), use_container_width=True)
        with col2:
            st.write("### 📊 황금 밸런스 동네의 남녀 인구 구성")
            fig = px.bar(match_town, x='행정동', y=['남자', '여자'], barmode='group',
                         labels={'value': '인구수 (명)', '행정동': '동 이름', 'variable': '성별'})
            st.plotly_chart(fig, use_container_width=True)
            
    elif mode == "남초 성향이 가장 강한 동네":
        male_town = df_2025.sort_values(by='성비(남/여)', ascending=False).head(10)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("### 🧔 남초 성향 탑 동네 (성비 최고)")
            st.dataframe(male_town[['구', '행정동', '성비(남/여)', '남자', '여자']].reset_index(drop=True), use_container_width=True)
        with col2:
            st.write("### 📊 남성 비율 시각화 차트")
            fig = px.bar(male_town, x='행정동', y='성비(남/여)', color='성비(남/여)', color_continuous_scale='Blues',
                         labels={'성비(남/여)': '성비 (여성 1명당 남성 수)'})
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        female_town = df_2025.sort_values(by='성비(남/여)', ascending=True).head(10)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("### 👩‍🦰 여초 성향 탑 동네 (성비 최저)")
            st.dataframe(female_town[['구', '행정동', '성비(남/여)', '남자', '여자']].reset_index(drop=True), use_container_width=True)
        with col2:
            st.write("### 📊 여성 우세 비율 시각화 차트")
            fig = px.bar(female_town, x='행정동', y='성비(남/여)', color='성비(남/여)', color_continuous_scale='Reds',
                         labels={'성비(남/여)': '성비 (여성 1명당 남성 수)'})
            st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 'population.csv' 파일을 찾을 수 없습니다.")
