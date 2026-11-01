import streamlit as st
import pandas as pd

st.set_page_config(page_title="배달 식당 한지붕(샵인샵) 조회기", layout="wide")

st.title(" 배달 식당 한지붕(샵인샵) 통합 조회기")
st.caption("공공데이터 기반으로 동일 주소지에 복수 등록된 샵인샵/공유주방 사업장을 탐색합니다.")

@st.cache_data
def load_data():
    df = pd.read_csv("delivery_stores.csv")
    df['clean_name'] = df['store_name'].astype(str).str.replace(" ", "")
    df['clean_addr'] = df['address'].astype(str).str.replace(" ", "")
    return df

df = load_data()

# 상단 지표
col_stat1, col_stat2 = st.columns(2)
with col_stat1:
    st.metric("총 등록된 샵인샵 의심 매장 수", f"{len(df):,}개")
with col_stat2:
    st.metric("의심 밀집 주소지(사업장) 수", f"{df['address'].nunique():,}곳")

st.markdown("---")

# 검색 방식 선택
search_type = st.radio(
    "검색 기준을 선택하세요:",
    ("식당/상호명으로 검색", "지역/동/도로명 주소로 검색"),
    horizontal=True
)

search_placeholder = "예: 김치찌개, 푸드, 치킨, 피자 등" if search_type == "식당/상호명으로 검색" else "예: 두정동, 불당동, 원성동, 강남대로 등"
query = st.text_input("검색어를 입력하세요:", placeholder=search_placeholder).strip()

if query:
    clean_q = query.replace(" ", "")
    
    if search_type == "식당/상호명으로 검색":
        matched_stores = df[df['clean_name'].str.contains(clean_q, na=False)]
    else:
        matched_stores = df[df['clean_addr'].str.contains(clean_q, na=False)]
        
    if matched_stores.empty:
        st.warning(f"⚠️ '{query}'에 대한 검색 결과가 없습니다.")
        st.info("💡 배달앱 상호와 구청 등록 법적 상호(예: ~푸드, ~키친)가 다를 수 있습니다. 주변 동 이름이나 도로명으로 검색해보세요.")
    else:
        unique_addrs = matched_stores['address'].unique()
        st.success(f"🔍 총 {len(unique_addrs)}곳의 주소지에서 일치하는 매장을 찾았습니다.")
        
        if len(unique_addrs) > 1:
            selected_addr = st.selectbox(
                "확인하고 싶은 주소지를 선택하세요:",
                options=unique_addrs,
                format_func=lambda x: f"{x} (해당 주소 등록 매장 {len(df[df['address'] == x])}개)"
            )
        else:
            selected_addr = unique_addrs[0]
            
        cluster = df[df['address'] == selected_addr]
        store_count = len(cluster)
        
        st.markdown("---")
        st.subheader("📍 주소지 상세 분석 결과")
        st.markdown(f"**소재지 주소:** `{selected_addr}`")
        
        if store_count >= 5:
            st.error(f"🚨 초밀집 공유주방/샵인샵 의심: 한 주소지에 **총 {store_count}개 매장**이 등록되어 있습니다!")
        else:
            st.warning(f"⚠️ 샵인샵 의심: 한 주소지에 **총 {store_count}개 매장**이 등록되어 있습니다.")
            
        display_table = cluster[['store_name', 'category']].copy()
        display_table.columns = ['등록 상호명', '인허가 업태']
        display_table.reset_index(drop=True, inplace=True)
        display_table.index = display_table.index + 1
        
        st.table(display_table)

# ----------------------------------------------------
# 하단 면책 조항 및 유의사항 (법적 보호 장치)
# ----------------------------------------------------
st.markdown("---")
with st.expander("ℹ️ 서비스 안내 및 법적 유의사항 (필독)", expanded=True):
    st.markdown("""
    - **공공데이터 출처**: 본 서비스는 행정안전부 및 지방자치단체가 공개한 공공데이터(지방행정인허가 일반음식점 데이터)를 기반으로 단순히 동일 인허가 주소지에 등록된 복수 사업장을 기계적으로 집계한 통계 정보입니다.
    - **합법적 영업 형태 안내**: 동일 주소에 여러 매장이 등록된 것은 시설 기준을 갖춘 공유주방 입점, 복합 상가 건물 입점, 또는 적법한 다중 영업신고 등 **합법적인 영업 형태**일 수 있으며, 특정 업장의 위생이나 서비스 품질과는 무관합니다.
    - **데이터 최신성 한계**: 공공데이터 갱신 주기 및 지자체 반영 시점에 따라 현재 폐업 또는 이전된 매장 정보가 일부 포함되어 있을 수 있습니다.
    """)
