import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="한집 - 공공데이터 기반 복수 음식점 인허가 조회 서비스",
    page_icon="🏠",
    layout="wide"
)

# 1. 메인 타이틀 및 슬로건 (중립적 행정정보 조회 성격 명시)
st.title("🏠 한집 (Han-Jib)")
st.subheader("공공데이터 기반 복수 음식점 인허가 조회 서비스")
st.caption("행정안전부 일반음식점 인허가 공공데이터를 바탕으로 동일 소재지에 등록된 복수 음식점 현황을 객관적으로 조회합니다.")

@st.cache_data
def load_data():
    df = pd.read_csv("delivery_stores.csv")
    df['clean_name'] = df['store_name'].astype(str).str.replace(" ", "")
    df['clean_addr'] = df['address'].astype(str).str.replace(" ", "")
    return df

df = load_data()

# 2. 통계 명칭 개선 ('의심' 단어 전면 제거 및 객관적 통계치 표현)
col_stat1, col_stat2 = st.columns(2)
with col_stat1:
    st.metric("동일 주소 복수 등록 매장 수", f"{len(df):,}개")
with col_stat2:
    st.metric("복수 매장 등록 주소 수", f"{df['address'].nunique():,}곳")

st.markdown("---")

# 검색 기준 라디오 버튼
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
        st.warning(f"'{query}'에 대한 등록 정보가 없습니다.")
        st.info("💡 공공데이터 인허가 법적 상호와 배달앱 표기 상호가 상이할 수 있습니다. 읍·면·동 이름 또는 도로명으로 검색해 보세요.")
    else:
        unique_addrs = matched_stores['address'].unique()
        st.success(f"총 {len(unique_addrs)}곳의 주소지에서 일치하는 인허가 정보를 확인했습니다.")
        
        if len(unique_addrs) > 1:
            selected_addr = st.selectbox(
                "확인할 주소지를 선택하세요:",
                options=unique_addrs,
                format_func=lambda x: f"{x} (해당 주소 등록 매장 {len(df[df['address'] == x])}개)"
            )
        else:
            selected_addr = unique_addrs[0]
            
        cluster = df[df['address'] == selected_addr]
        store_count = len(cluster)
        
        st.markdown("---")
        st.subheader("소재지 인허가 상세 현황")
        st.markdown(f"**조회 주소지:** `{selected_addr}`")
        
        # 부정적 낙인 효과가 있는 경고창 대신 객관적 현황 안내로 변경
        st.info(f"ℹ️ 해당 주소지에 행정 인허가 기준 **총 {store_count}개 음식점**이 등록되어 있습니다.")
            
        display_table = cluster[['store_name', 'category']].copy()
        display_table.columns = ['인허가 상호명', '인허가 업태']
        display_table.reset_index(drop=True, inplace=True)
        display_table.index = display_table.index + 1
        
        st.table(display_table)

# ----------------------------------------------------
# 3 & 4. 법적 안전장치, 정보 해석 원칙 및 정정 요청 창구
# ----------------------------------------------------
st.markdown("---")
with st.expander("ℹ️ 정보 해석에 관한 유의사항 및 법적 고지 (필독)", expanded=True):
    st.markdown("""
    **1. 정보 해석에 관한 유의사항**
    * 본 서비스는 행정안전부 및 지방자치단체의 공공데이터(지방행정인허가 일반음식점 데이터)에 등록된 정보를 바탕으로 동일하거나 유사한 소재지에 복수의 음식점이 등록된 현황을 검색하는 서비스입니다.
    * 동일 주소에 여러 음식점이 등록되어 있다는 사실만으로 동일 사업자의 운영, 샵인샵 형태의 영업, 불법 영업 또는 소비자 기만 행위를 의미하지 않습니다.
    * 실제 영업 형태 및 사업자 간 관계는 해당 데이터만으로 확인할 수 없으며, 이용자는 검색 결과를 특정 업체에 대한 부정적인 판단의 근거로 단정해서는 안 됩니다.
    * 시설 기준을 충족한 공유주방 입점, 복합 상가 건물 입점, 또는 적법한 다중 영업신고 등은 관계 법령에 따른 정상적인 영업 형태입니다.

    **2. 데이터의 최신성 및 출처**
    * **출처**: 공공데이터포털(data.go.kr) 지방행정인허가데이터(일반음식점)
    * 데이터의 정확성과 최신성은 원천 공공데이터의 갱신 시점 및 행정기관의 정보 반영 시점에 따라 달라질 수 있으며, 현재 폐업 또는 이전된 매장 정보가 일부 포함되어 있을 수 있습니다.

    **3. 데이터 오류 및 정보 정정 요청**
    * 공공데이터 원천 정보의 변경(폐업, 이전, 상호 변경 등)에 따른 정보 수정이나 삭제 요청이 있으실 경우, 하단 저장소(Issue) 또는 관리자 문의를 통해 접수해 주시면 검토 후 즉시 반영하겠습니다.
    """)
