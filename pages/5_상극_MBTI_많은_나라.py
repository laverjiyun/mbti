import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="상극 MBTI 많은 나라", layout="wide")

st.title("⚡ 상극 유형(ENFP + ISTJ)이 가장 많은 나라 Top 10")
st.markdown("---")

try:
    df = pd.read_csv("countries_mbti.csv")
    
    st.caption("💡 모든 지표가 정반대인 스파크형(ENFP)과 소금형(ISTJ) 두 유형의 인구 비율을 합산하여, 두 성향이 공존하는 비율이 가장 높은 국가를 분석합니다.")
    
    df_vs = df.copy()
    if 'ENFP' in df_vs.columns and 'ISTJ' in df_vs.columns:
        df_vs['VS_Total'] = df_vs['ENFP'] + df_vs['ISTJ']
        top10_vs = df_vs[['Country', 'ENFP', 'ISTJ', 'VS_Total']].sort_values(by='VS_Total', ascending=False).head(10)
        
        col1, col2 = st.columns([1.2, 2])
        with col1:
            st.write("### 📊 순위 테이블 (상세 비율)")
            st.dataframe(top10_vs.reset_index(drop=True), use_container_width=True)
        with col2:
            st.write("### 📈 국가별 ENFP vs ISTJ 비율 구성")
            # 누적 막대그래프로 두 상극 성향의 내부 지분을 시각화
            fig_vs = px.bar(top10_vs, x='Country', y=['ENFP', 'ISTJ'],
                           labels={'value': '비율', 'Country': '국가', 'variable': 'MBTI 유형'},
                           barmode='stack',
                           color_discrete_map={'ENFP': '#FF9999', 'ISTJ': '#9999FF'})
            st.plotly_chart(fig_vs, use_container_width=True)
    else:
        st.error("⚠️ 데이터에 'ENFP' 또는 'ISTJ' 열이 존재하지 않습니다.")

except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다.")
