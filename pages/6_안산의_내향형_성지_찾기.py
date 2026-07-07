import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="내향형(I)의 성지", layout="wide")

st.title("🤫 안산에서 MBTI 'I'들이 살기 가장 좋은 동네는?")
st.markdown("---")

try:
    df = pd.read_csv("population.csv")
    
    st.markdown("""
    💡 **분석 컨셉:** 인구가 너무 많거나 북적거리는 핫플레이스는 외향형(E)들의 무대일 확률이 높습니다! 
    반대로 **가장 최근(2025년 기준) 인구수가 적어 한적하거나, 지난 10년간 인구가 꾸준히 감소하여 조용한 혼자만의 여유를 즐길 수 있는 'I들의 힐링 성지'**를 찾아냅니다.
    """)
    
    # 2025년 최신 데이터 필터링
    df_2025 = df[df['연도'] == 2025].copy()
    
    # 분석 기준 선택
    mode = st.radio("I들의 성지를 판정할 기준을 고르세요:", ["현재 인구가 가장 적고 조용한 동네", "지난 10년간 인구가 가장 많이 감소한 동네"])
    
    if mode == "현재 인구가 가장 적고 조용한 동네":
        top10_i = df_2025.sort_values(by='총인구', ascending=True).head(10)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("### 🏆 가장 한적한 동네 Top 10")
            st.dataframe(top10_i[['구', '행정동', '총인구']].reset_index(drop=True), use_container_width=True)
        with col2:
            st.write("### 📊 동네별 인구 규모 비교")
            fig = px.bar(top10_i, x='행정동', y='총인구', color='총인구', color_continuous_scale='Purples',
                         labels={'총인구': '총 인구수 (명)', '행정동': '동 이름'})
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        # 2016년과 2025년 인구 비교하여 감소율 계산
        df_2016 = df[df['연度' if '연度' in df.columns else '연도'] == 2016][['행정동', '총인구']].rename(columns={'총인구': '인구_2016'})
        df_2025_sub = df_2025[['행정동', '총인구']].rename(columns={'총인구': '인구_2025'})
        
        merged = pd.merge(df_2016, df_2025_sub, on='행정동')
        merged['인구감소율(%)'] = ((merged['인구_2016'] - merged['인구_2025']) / merged['인구_2016'] * 100).round(2)
        
        # 감소율이 높은 순으로 정렬
        top10_decrease = merged.sort_values(by='인구감소율(%)', ascending=False).head(10)
        
        col1, col2 = st.columns([1.2, 2])
        with col1:
            st.write("### 🏆 인구 감소 속도가 빠른(점점 조용해지는) 동네")
            st.dataframe(top10_decrease[['행정동', '인구_2016', '인구_2025', '인구감소율(%)']].reset_index(drop=True), use_container_width=True)
        with col2:
            st.write("### 📊 지난 10년간 인구 감소율(%)")
            fig = px.bar(top10_decrease, x='행정동', y='인구감소율(%)', color='인구감소율(%)', color_continuous_scale='Mint',
                         labels={'인구감소율(%)': '감소율 (%)', '행정동': '동 이름'})
            st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 'population.csv' 파일을 찾을 수 없습니다. 전처리를 먼저 진행해 주세요.")
