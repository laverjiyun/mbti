import streamlit as pd
import streamlit as st
import pandas as pd

st.set_page_config(page_title="세계 MBTI 분석 대시보드", layout="wide")

st.title("🌍 세계 국가별 MBTI 분포 분석 대시보드")
st.markdown("---")

st.markdown("""
이 대시보드는 전 세계 다양한 국가의 MBTI 성격 유형 분포 데이터를 시각화하고 비교 분석하기 위해 제작되었습니다.
왼쪽 사이드바의 메뉴를 이용해 원하는 분석 페이지로 이동할 수 있습니다.
""")

# 데이터 프리뷰
st.subheader("📊 원본 데이터 분석 요약 (`countries_mbti.csv`)")
try:
    df = pd.read_csv("countries_mbti.csv")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("총 대상 국가 수", f"{len(df)}개국")
    col2.metric("분석된 MBTI 유형 수", f"{len(df.columns) - 1}개")
    col3.metric("데이터 행/열 수", f"{df.shape[0]} x {df.shape[1]}")
    
    st.write("### 데이터 미리보기")
    st.dataframe(df.head(10), use_container_width=True)
except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
