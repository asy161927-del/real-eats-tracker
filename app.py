import streamlit as st
import pandas as pd

# ----------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------
st.set_page_config(
    page_title="한집(Han-Jib) - 공공데이터 기반 복수 음식점 인허가 조회",
    page_icon="🏍️",
    layout="centered"
)

# ----------------------------------------------------
# 2. 커스텀 CSS (상단 흑청색 배너 + 중앙 흰색 검색 보드)
# ----------------------------------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 800px !important;
    }
    
    /* 1. 상단 다크 배너 */
    .top-hero-banner {
        background-color: #0f172a;
        color: #ffffff;
        border-radius: 16px 16px 0 0;
        padding: 30px 20px 24px 20px;
        text-align: center;
    }
    .top-title {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 6px;
        letter-spacing: -0.02em;
    }
    .top-subtitle {
        font-size: 0.92rem;
        color: #94a3b8;
        margin-bottom: 22px;
    }

    /* 2. 상단 통계 수치 바 (배너 내부) */
    .hero-stats-row {
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-top: 1px solid #334155;
        padding-top: 18px;
        margin-top: 5px;
    }
    .hero-stat-col {
        flex: 1;
        text-align: center;
        border-right: 1px solid #334155;
    }
    .hero-stat-col:last-child {
        border-right: none;
    }
    .hero-stat-label {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 4px;
        font-weight: 500;
    }
    .hero-stat-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #38bdf8;
        letter-spacing: -0.01em;
    }

    /* 3. 중앙 흰색 검색 보드 카드 */
    .search-card-wrapper {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 16px 16px;
        padding: 24px 24px 18px 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.07);
        margin-bottom: 2rem;
    }

    /* 검색창 힌트 문구 */
    .search-tips-box {
        font-size: 0.83rem;
        color: #64748b;
        margin-top: 10px;
        text-align: left;
    }

    /* 결과 카드 (다크 네이비) */
    .result-alert-box {
        background-color: #0f172a;
        color: #ffffff;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 1.2rem;
        margin-bottom: 1rem;
    }
    .result-addr-title {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    .result-count-val {
        font-size: 1.25rem;
        font-weight: 700;
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. 데이터 로드 및 캐싱
# ----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("delivery_stores.csv")
    df['clean_name'] = df['store_name'].astype(str).str.replace(" ", "")
    df['clean_addr'] = df['address'].astype(str).str.replace(" ", "")
    return df

df = load_data()

# ----------------------------------------------------
# 4. 상단 다크 배너 (타이틀 + 통계 수치만 노출)
# ----------------------------------------------------
st.markdown(f"""
<div class="top-hero-banner">
    <div class="top-title">🏍️ 한집 (Han-Jib)</div>
    <div class="top-subtitle">공공데이터 기반 동일 주소 복수 음식점 인허가 현황 조회</div>
    <div class="hero-stats-row">
        <div class="hero-stat-col">
            <div class="hero-stat-label">분석 대상 공공 인허가</div>
            <div class="hero-stat-value">{len(df):,}</div>
        </div>
        <div class="hero-stat-col">
            <div class="hero-stat-label">복수 등록 주소지</div>
            <div class="hero-stat-value">{df['address'].nunique():,}</div>
        </div>
        <div class="hero-stat-col">
            <div class="hero-stat-label">데이터 기준 지역</div>
            <div class="hero-stat-value">전국 17개 시도</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. 흰색 보드 안의 검색창 영역
# ----------------------------------------------------
with st.container():
    query = st.text_input(
        label="검색창",
        placeholder="배달앱 상호명 또는 동/도로명 주소를 입력하세요 (예: 역삼동, 신림동, 테헤란로, 피자)",
        label_visibility="collapsed"
    ).strip()
    
    st.markdown("""
    <div class="search-tips-box">
        💡 <b>검색 팁:</b> 서울 주요 동/도로명(예: 역삼동, 화양동, 마포대로)이나 상호의 핵심 단어로 검색해 보세요.
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 6. 검색 결과 출력
# ----------------------------------------------------
if query:
    clean_q = query.replace(" ", "")
    matched_stores = df[
        df['clean_name'].str.contains(clean_q, na=False) | 
        df['clean_addr'].str.contains(clean_q, na=False)
    ]
    
    if matched_stores.empty:
        st.warning(f"검색어 **'{query}'**에 대한 등록 정보가 없습니다.")
        st.info("공공데이터 인허가상 법적 상호와 배달앱 표기 상호가 상이할 수 있습니다. 읍·면·동 이름 또는 도로명으로 다시 검색해 보세요.")
    else:
        unique_addrs = matched_stores['address'].unique()
        
        if len(unique_addrs) > 1:
            st.markdown(f"**총 `{len(unique_addrs)}곳`의 연관 소재지가 발견되었습니다.**")
            selected_addr = st.selectbox(
                "확인할 주소지를 선택하세요:",
                options=unique_addrs,
                format_func=lambda x: f"{x} (해당 주소 등록 매장 {len(df[df['address'] == x])}개)"
            )
        else:
            selected_addr = unique_addrs[0]
            
        cluster = df[df['address'] == selected_addr]
        store_count = len(cluster)
        
        # 결과 요약 카드
        st.markdown(f"""
        <div class="result-alert-box">
            <div class="result-addr-title">📍 조회 소재지: {selected_addr}</div>
            <div class="result-count-val">해당 주소지 인허가 매장 총 {store_count}개</div>
        </div>
        """, unsafe_allow_html=True)
            
        display_table = cluster[['store_name', 'category']].copy()
        display_table.columns = ['인허가 상호명', '인허가 업태']
        display_table.reset_index(drop=True, inplace=True)
        display_table.index = display_table.index + 1
        
        st.table(display_table)

# ----------------------------------------------------
# 7. 하단 법적 고지 및 유의사항
# ----------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ℹ️ 정보 해석에 관한 법적 고지 및 유의사항 (필독)"):
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
