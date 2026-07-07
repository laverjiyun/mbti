import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="P 성향 많은 나라", layout="wide")

st.title("🏃‍♂️ P(인식형)가 가장 많은 나라 Top 10")
st.markdown("---")

try:
    df = pd.read_csv("countries_mbti.csv")
    mbti_cols = [col for col in df.columns if col != "Country"]
    
    st.caption("💡 MBTI 16가지 유형 중 네 번째 자리가 'P'인 유형(INFP, INTP, ENFP, ENTP, ISFP, ISTP, ESFP, ESTP)의 비율을 합산했습니다.")
    
    # P가 포함된 열만 선택하여 합산
    p_types = [col for col in mbti_cols if 'P' in col]
    df_p = df.copy()
    df_p['P_Total'] = df_p[p_types].sum(axis=1)
    
    top10_p = df_p[['Country', 'P_Total']].sort_values(by='P_Total', ascending=False).head(10)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("### 📊 순위 테이블")
        st.dataframe(top10_p.reset_index(drop=True), use_container_width=True)
    with col2:
        st.write("### 📈 시각화 차트")
        fig_p = px.bar(top10_p, x='Country', y='P_Total', color='P_Total',
                       labels={'P_Total': 'P 성향 총합 비율', 'Country': '국가'},
                       color_continuous_scale='Greens')
        st.plotly_chart(fig_p, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다.")
