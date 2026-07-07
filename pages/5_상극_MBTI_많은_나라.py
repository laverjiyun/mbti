import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="상극 MBTI 많은 나라", layout="wide")

st.title("⚡ 상극 성향 조합 국가별 분포 분석")
st.markdown("---")

try:
    df = pd.read_csv("countries_mbti.csv")
    mbti_cols = [col for col in df.columns if col != "Country"]
    
    st.markdown("""
    💡 **상극 MBTI 조합이란?** 4가지 선호 지표(E/I, N/S, T/F, J/P)가 모두 정반대되어 성향 차이가 가장 크다고 알려진 대표적인 조합들입니다. 
    두 유형의 비율 합이 높은 국가일수록, 서로 다른 가치관을 가진 두 집단이 팽팽하게 공존하고 있음을 의미합니다.
    """)
    
    # 1. 대표적인 상극 조합 프리셋 정의
    opposite_pairs = {
        "ENFP 🤝 ISTJ (스파크형 vs 소금형)": ("ENFP", "ISTJ"),
        "INFP 🤝 ESTJ (잔다르크형 vs 사업가형)": ("INFP", "ESTJ"),
        "INFJ 🤝 ESTP (예언자형 vs 활동가형)": ("INFJ", "ESTP"),
        "INTJ 🤝 ESFP (과학자형 vs 연예인형)": ("INTJ", "ESFP"),
        "INTP 🤝 ESFJ (아이디어형 vs 친선도모형)": ("INTP", "ESFJ"),
        "ENTP 🤝 ISFJ (발명가형 vs 권력형)": ("ENTP", "ISFJ"),
        "ENTJ 🤝 ISFP (지도자형 vs 성인군자형)": ("ENTJ", "ISFP"),
        "ENFJ 🤝 ISTP (언변능숙형 vs 백과사전형)": ("ENFJ", "ISTP"),
    }
    
    # 2. 사용자 입력 방식 선택 (프리셋 vs 직접 선택)
    analysis_mode = st.radio("분석할 조합 선택 방식:", ["추천 상극 조합 목록에서 선택", "내가 직접 2개 유형 지정하기"], horizontal=True)
    
    type1, type2 = "", ""
    
    if analysis_mode == "추천 상극 조합 목록에서 선택":
        selected_pair_name = st.selectbox("☯️ 상극 조합을 선택하세요:", list(opposite_pairs.keys()))
        type1, type2 = opposite_pairs[selected_pair_name]
    else:
        col_select1, col_select2 = st.columns(2)
        with col_select1:
            type1 = st.selectbox("🧬 첫 번째 MBTI 유형 선택:", sorted(mbti_cols), index=0)
        with col_select2:
            # 첫 번째 선택과 중복되지 않도록 리스트 제공
            remaining_cols = [c for c in sorted(mbti_cols) if c != type1]
            type2 = st.selectbox("🧬 두 번째 MBTI 유형 선택 (상극 등):", remaining_cols, index=len(remaining_cols)-1)

    # 3. 데이터 계산 및 시각화
    if type1 in df.columns and type2 in df.columns:
        df_vs = df.copy()
        df_vs['Combined_Total'] = df_vs[type1] + df_vs[type2]
        
        # 상위 10개국 추출
        top10_vs = df_vs[['Country', type1, type2, 'Combined_Total']].sort_values(by='Combined_Total', ascending=False).head(10)
        
        st.markdown(f"### 📊 **{type1}**와(과) **{type2}** 성향이 가장 많이 공존하는 나라 Top 10")
        
        col1, col2 = st.columns([1.2, 2])
        with col1:
            st.write("#### 📋 순위 및 데이터 테이블")
            # 보기 편하게 백분율(%) 표기법 등으로 정돈하여 출력 가능
            st.dataframe(top10_vs.reset_index(drop=True), use_container_width=True)
            
        with col2:
            st.write("#### 📈 두 유형의 국가별 구성 비율 차트")
            # 두 유형을 누적 막대로 쌓아서 국가별 비율을 시각화
            fig_vs = px.bar(
                top10_vs, 
                x='Country', 
                y=[type1, type2],
                labels={'value': '인구 비율', 'Country': '국가', 'variable': 'MBTI 유형'},
                barmode='stack',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_vs, use_container_width=True)
    else:
        st.error("⚠️ 데이터 세트에 선택하신 MBTI 유형이 존재하지 않습니다.")

except FileNotFoundError:
    st.error("⚠️ 'countries_mbti.csv' 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
