import streamlit as st
import pandas as pd

# ----------------------------------------------------
# 1. 페이지 기본 설정 및 브랜딩 (라이더 이모티콘 🏍️ 적용)
# ----------------------------------------------------
st.set_page_config(
    page_title="한집(Han-Jib) - 공공데이터 기반 복수 음식점 인허가 조회 서비스",
    page_icon="🏍️",
    layout="wide"
)

st.title("🏍️ 한집 (Han-Jib)")
st.subheader("공공데이터 기반 복수 음식점 인허가 조회 서비스")
st.caption("행정안전부 일반음식점 인허가 공공데이터를 바탕으로 동일 소재지에 등록된 복수 음식점 인허가 현황을 객관적으로 조회합니다.")

# ----------------------------------------------------
# 2. 데이터 로드 및 전처리 캐싱
# ----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("delivery_stores.csv")
    df['clean_name'] = df['store_name'].astype(str).str.replace(" ", "")
    df['clean_addr'] = df['address'].astype(str).str.replace(" ", "")
    return df

df = load_data()

# ----------------------------------------------------
# 3. 핵심 현황 지표 (중립적 통계 명칭 적용)
# ----------------------------------------------------
col_stat1, col_stat2 = st.columns(2)
with col_stat1:
    st.metric("동일 주소 복수 등록 매장 수", f"{len(df):,}개")
with col_stat2:
    st.metric("복수 매장 등록 주소 수", f"{df['address'].nunique():,}곳")

st.markdown("---")

# ----------------------------------------------------
# 4. 검색 인터페이스
# ----------------------------------------------------
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
        
        # 복수 주소지 선택 드롭다운
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
        st.info(f"ℹ️ 해당 주소지에 행정 인허가 기준 **총 {store_count}개 음식점**이 등록되어 있습니다.")
            
        # 대표자 및 개인정보를 배제하고 상호명과 인허가 업태만 출력
        display_table = cluster[['store_name', 'category']].copy()
        display_table.columns = ['인허가 상호명', '인허가 업태']
        display_table.reset_index(drop=True, inplace=True)
        display_table.index = display_table.index + 1
        
        st.table(display_table)

# ----------------------------------------------------
# 5. 법적 안전장치 및 정보 해석 유의사항 (필독 고지)
# ----------------------------------------------------
st.markdown("---")
with st.expander("ℹ️ 정보 해석에 관한 유의사항 및 법적 고지 (필독)", expanded=True):
    st.markdown("""
    **1. 동일 주소 등록과 운영 주체의 명확한 구분**
    * **동일 주소 등록이 동일 사업자를 의미하지 않습니다.** 본 서비스는 행정 인허가상 소재지(주소)가 같거나 유사한 매장을 기계적으로 집계한 것일 뿐이며, **각 매장의 실제 운영자나 대표자가 동일인임을 나타내는 것이 결코 아닙니다.**
    * 복합 상가 건물 입점, 정식 시설 기준을 갖춘 공유주방 내 각기 다른 개별 창업자 입점, 독립된 복수 사업자 운영 등은 관련 법령에 따른 정상적이고 합법적인 영업 형태입니다.

    **2. 객관적 행정정보 제공 및 비방 금지 원칙**
    * 본 서비스는 공공데이터포털(data.go.kr)의 지방행정인허가(일반음식점) 공공데이터에 근거한 사실 정보만을 제공하며, 특정 업체를 비방·평가하거나 샵인샵 영업 여부를 단정하지 않습니다.
    * 이용자는 본 조회 결과를 특정 업체에 대한 불필요한 오해나 부정적인 평가의 근거로 단정해서는 안 되며, 대표자 신상이나 개인정보는 일체 수집·제공하지 않습니다.

    **3. 데이터의 최신성 및 정정 요청 안내**
    * 공공데이터 갱신 주기 및 지자체 행정 반영 시점에 따라 현재 폐업·이전·상호 변경된 정보가 일부 포함되어 있을 수 있습니다.
    * 데이터의 정정, 갱신, 삭제 요청이 있으신 업주 및 관계자분께서는 프로젝트 저장소(Issue) 또는 관리자 문의를 통해 접수해 주시면 확인 즉시 조치하겠습니다.
    """)
