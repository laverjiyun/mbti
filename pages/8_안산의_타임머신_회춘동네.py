import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="타임머신 회춘 동네", layout="wide")

st.title("⏳ 안산에서 타임머신을 타고 과거로 가는 듯한 '회춘형' 동네는?")
st.markdown("---")

try:
    df = pd.read_csv("population.csv")
    
    st.markdown("""
    💡 **분석 컨셉:** 대부분의 기성 도심지역은 시간이 흐를수록 인구가 정체되거나 감소하며 고령화 과정을 겪습니다. 
    하지만 신축 아파트 단지 입주, 신도시 개발 등으로 인해 **오히려 시간이 흐를수록 인구가 폭발적으로 역주행하며 젊어지고 커지는 '성장형 회춘 동네'**를 찾아냅니다!
    """)
    
    # 2016년 데이터와 2025년 데이터 추출 후 비교
    df_2016 = df[df['연도'] == 2016][['행정동', '총인구']].rename(columns={'총인구': '인구_2016'})
    df_2025 = df[df['연도'] == 2025][['구', '행정동', '총인구']].rename(columns={'총인구': '인구_2025'})
    
    merged = pd.merge(df_2025, df_2016, on='행정동')
    merged['인구증가폭(명)'] = merged['인구_2025'] - merged['인구_2016']
    merged['인구증가율(%)'] = ((merged['인구_2025'] - merged['인구_2016']) / merged['인구_2016'] * 100).round(2)
    
    # 인구 증가율이 높은 상위 10개국(동)
    rejuvenated_towns = merged.sort_values(by='인구증가율(%)', ascending=False).head(10)
    
    col1, col2 = st.columns([1.2, 2])
    with col1:
        st.write("### 🚀 인구 대역전! 폭풍 성장한 회춘 동네 Top 10")
        st.dataframe(rejuvenated_towns[['구', '행정동', '인구_2016', '인구_2025', '인구증가율(%)']].reset_index(drop=True), use_container_width=True)
        
    with col2:
        st.write("### 📈 2016년 대비 2025년 인구 증가율(%) 순위")
        fig = px.bar(rejuvenated_towns, x='행정동', y='인구증가율(%)', color='인구증가율(%)', color_continuous_scale='Sunset',
                     labels={'인구증가율(%)': '증가율 (%)', '행정동': '동 이름'})
        st.plotly_chart(fig, use_container_width=True)
        
    # 하단에 선택한 회춘 동네의 전체 시계열 트렌드를 볼 수 있는 보너스 차트 기능
    st.markdown("---")
    st.write("### 🔍 원하는 회춘 동네의 2016~2025년 전체 인구 변화 추이 보기")
    selected_dong = st.selectbox("동네를 선택해 추적해보세요:", rejuvenated_towns['행정동'].unique())
    
    history_df = df[df['행정동'] == selected_dong].sort_values(by='연도')
    
    fig_line = px.line(history_df, x='연도', y=['총인구', '남자', '여자'], markers=True,
                       title=f"📈 {selected_dong}의 연도별 인구 역주행 선그래프",
                       labels={'value': '인구수 (명)', '연도': '조사 연도', 'variable': '지표'})
    st.plotly_chart(fig_line, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ 'population.csv' 파일을 찾을 수 없습니다.")
