import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI별 국가 비교", layout="wide")

st.title("⚖️ MBTI 유형별 국가 비교")
st.markdown("---")

try:
    df = pd.read_csv("countries_mbti.csv")
    
    # MBTI 유형 리스트 선택 (Country 열 제외)
    mbti_types = [col for col in df.columns if col != "Country"]
    selected_mbti = st.selectbox("🧬 비교할 MBTI 유형을 선택하세요:", sorted(mbti_types))
    
    # 선택된 MBTI 기준으로 정렬된 데이터 생성
    compare_df = df[["Country", selected_mbti]].sort_values(by=selected_mbti, ascending=False)
    
    # 상위/하위 몇 개국을 볼지 설정하는 슬라이더
    top_n = st.slider("🗺️ 표시할 국가 수를 선택하세요:", min_value=5, max_value=len(compare_df), value=15)
    
    top_countries = compare_df.head(top_n)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write(f"### 🏆 {selected_mbti} 비율이 높은 국가 (Top {top_n})")
        st.dataframe(top_countries.reset_index(drop=True), use_container_width=True)
        
    with col2:
        st.write(f"### 📊 {selected_mbti} 유형 국가별 비교 차트")
        fig = px.bar(
            top_countries,
            x="Country",
            y=selected_mbti,
            labels={"Country": "국가", selected_mbti: "비율"},
            color=selected_mbti,
            color_continuous_scale="Plasma"
        )
        st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다.")
