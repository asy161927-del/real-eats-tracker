import streamlit as st
import pandas as pd

st.set_page_config(page_title="배달 식당 한지붕(샵인샵) 조회기", layout="wide")

st.title(" 배달 식당 한지붕(샵인샵) 통합 조회기")
st.caption("공공데이터 기반으로 동일 주소지에 3개 이상 등록된 샵인샵/공유주방 사업장을 탐색합니다.")

@st.cache_data
def load_data():
    df = pd.read_csv("delivery_stores.csv")
    # 검색 편의를 위해 띄어쓰기 제거된 검색용 컬럼 미리 생성
    df['clean_name'] = df['store_name'].astype(str).str.replace(" ", "")
    df['clean_addr'] = df['address'].astype(str).str.replace(" ", "")
    return df

df = load_data()

# 상단 안내 및 통계 지표
col_stat1, col_stat2 = st.columns(2)
with col_stat1:
    st.metric("총 등록된 샵인샵 의심 매장 수", f"{len(df):,}개")
with col_stat2:
    st.metric("의심 밀집 주소지(사업장) 수", f"{df['address'].nunique():,}곳")

st.markdown("---")

# 검색 방식 선택 라디오 버튼
search_type = st.radio(
    "검색 기준을 선택하세요:",
    ("식당/상호명으로 검색", "지역/동/도로명 주소로 검색"),
    horizontal=True
)

search_placeholder = "예: 김치찌개, 푸드, 치킨, 피자 등" if search_type == "식당/상호명으로 검색" else "예: 두정동, 불당동, 강남대로, 서초중앙로 등"
query = st.text_input("검색어를 입력하세요:", placeholder=search_placeholder).strip()

if query:
    clean_q = query.replace(" ", "")
    
    if search_type == "식당/상호명으로 검색":
        matched_stores = df[df['clean_name'].str.contains(clean_q, na=False)]
    else:
        matched_stores = df[df['clean_addr'].str.contains(clean_q, na=False)]
        
    if matched_stores.empty:
        st.warning(f"⚠️ '{query}'에 대한 검색 결과가 없습니다.")
        st.info("💡 팁: 배달앱 상호와 구청 등록 법적 상호(예: ~푸드, ~키친)가 다를 수 있습니다. 주변 동 이름이나 도로명으로 검색해보세요.")
    else:
        # 매칭된 주소 목록 추출
        unique_addrs = matched_stores['address'].unique()
        st.success(f"🔍 총 {len(unique_addrs)}곳의 주소지에서 일치하는 매장을 찾았습니다.")
        
        # 주소가 여러 개일 경우 선택할 수 있는 셀렉트박스 제공
        if len(unique_addrs) > 1:
            selected_addr = st.selectbox(
                "확인하고 싶은 주소지를 선택하세요:",
                options=unique_addrs,
                format_func=lambda x: f"{x} (해당 주소 등록 매장 {len(df[df['address'] == x])}개)"
            )
        else:
            selected_addr = unique_addrs[0]
            
        # 선택된 주소지의 모든 매장 정보 추출
        cluster =
