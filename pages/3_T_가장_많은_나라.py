import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="T 성향 많은 나라", layout="wide")

st.title("🧠 T(사고형) 성향이 가장 많은 나라 Top 10")
st.markdown("---")

try:
    df = pd.read_csv("countries_mbti.csv")
    mbti_cols = [col for col in df.columns if col != "Country"]
    
    st.caption("💡 MBTI 16가지 유형 중 세 번째 자리가 'T'인 유형(INTJ, INTP, ENTJ, ENTP, ISTJ, ISTP, ESTJ, ESTP)의 비율을 합산했습니다.")
    
    # T가 포함된 열만 선택하여 합산
    t_types = [col for col in mbti_cols if 'T' in col]
    df_t = df.copy()
    df_t['T_Total'] = df_t[t_types].sum(axis=1)
    
    top10_t = df_t[['Country', 'T_Total']].sort_values(by='T_Total', ascending=False).head(10)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("### 📊 순위 테이블")
        st.dataframe(top10_t.reset_index(drop=True), use_container_width=True)
    with col2:
        st.write("### 📈 시각화 차트")
        fig_t = px.bar(top10_t, x='Country', y='T_Total', color='T_Total',
                       labels={'T_Total': 'T 성향 총합 비율', 'Country': '국가'},
                       color_continuous_scale='Blues')
        st.plotly_chart(fig_t, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다.")
