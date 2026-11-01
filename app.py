import streamlit as st
import pandas as pd

# ----------------------------------------------------
# 1. 페이지 설정
# ----------------------------------------------------
st.set_page_config(
    page_title="한집 (Han-Jib) - 복수 음식점 인허가 검색",
    page_icon="🏍️",
    layout="wide"
)

# ----------------------------------------------------
# 2. 더치트 스타일 전용 커스텀 CSS
# ----------------------------------------------------
st.markdown("""
<style>
    /* 기본 여백 초기화 */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 3rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* 1. 상단 글로벌 네비게이션 바 */
    .thecheat-navbar {
        background-color: #174b85;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 10%;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    }
    .thecheat-logo {
        font-size: 1.35rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .thecheat-nav-menus {
        display: flex;
        gap: 20px;
        color: #dbeafe;
        font-size: 0.88rem;
        font-weight: 500;
    }

    /* 2. 메인 블루 히어로 섹션 */
    .thecheat-hero {
        background: linear-gradient(180deg, #1f5e9e 0%, #174b85 100%);
        padding: 60px 15% 45px 15%;
        text-align: center;
        color: white;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #bfdbfe;
        margin-bottom: 30px;
    }

    /* 검색창 래퍼 중앙 정렬 */
    .search-container {
        max-width: 680px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Streamlit 기본 text_input 커스텀 (더치트 검색창처럼 굵고 시원하게) */
    div[data-testid="stTextInput"] input {
        height: 52px !important;
        font-size: 1.05rem !important;
        border-radius: 6px !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        padding-left: 16px !important;
    }
    
    .hero-footer-text {
        font-size: 0.82rem;
        color: #93c5fd;
        margin-top: 14px;
        margin-bottom: 15px;
    }

    /* 3. 하단 화이트 통계 섹션 (더치트 하단 지표 완벽 재현) */
    .thecheat-stats-section {
        background-color: #ffffff;
        padding: 40px 10%;
        border-bottom: 1px solid #e2e8f0;
    }
    .stats-grid {
        display: flex;
        justify-content: space-around;
        text-align: center;
        max-width: 1000px;
        margin: 0 auto;
    }
    .stat-item {
        flex: 1;
        border-right: 1px solid #e2e8f0;
    }
    .stat-item:last-child {
        border-right: none;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 6px;
    }
    .stat-num {
        font-size: 1.9rem;
        font-weight: 800;
        color: #174b85;
        letter-spacing: -0.02em;
    }

    /* 4. 본문 결과 영역 콘테이너 */
    .content-container {
        max-width: 900px;
        margin: 30px auto;
        padding: 0 20px;
    }
    
    /* 결과 요약 카드 (더치트 결과 카드) */
    .result-alert-box {
        background-color: #eff6ff;
        border-left: 5px solid #174b85;
        border-radius: 6px;
        padding: 16px 20px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
# 4. 상단 네비게이션 바 & 블루 히어로 영역
# ----------------------------------------------------
st.markdown("""
<div class="thecheat-navbar">
    <div class="thecheat-logo">🏍️ 한집 (Han-Jib)</div>
    <div class="thecheat-nav-menus">
        <span>🔍 인허가 조회</span>
        <span>📋 공공데이터 출처</span>
        <span>ℹ️ 법적 안내</span>
    </div>
</div>

<div class="thecheat-hero">
    <div class="hero-title">동일 주소 인허가 현황 검색</div>
    <div class="hero-subtitle">배달앱에 등록된 매장의 실제 인허가 소재지와 복수 등록 매장을 확인해보세요.</div>
</div>
""", unsafe_allow_html=True)

# 검색창 (히어로 영역 중앙에 배치)
_, col_search, _ = st.columns([1, 4, 1])
with col_search:
    query = st.text_input(
        label="search_box",
        placeholder="상호명 또는 동/도로명 주소를 입력해 보세요. (예: 두정동, 피자)",
        label_visibility="collapsed"
    ).strip()

st.markdown("""
<div class="thecheat-hero" style="padding-top: 0; padding-bottom: 25px;">
    <div class="hero-footer-text">한집은 투명한 행정정보 공유와 소비자 알 권리를 위해 공공데이터를 기반으로 운영됩니다.</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. 하단 화이트 통계 영역 (더치트 스타일 4개 지표)
# ----------------------------------------------------
st.markdown(f"""
<div class="thecheat-stats-section">
    <div class="stats-grid">
        <div class="stat-item">
            <div class="stat-label">분석 대상 공공 인허가</div>
            <div class="stat-num">{len(df):,}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">복수 등록 주소지</div>
            <div class="stat-num">{df['address'].nunique():,}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">데이터 기준 지역</div>
            <div class="stat-num">전국 17개 시도</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">실시간 연계 공공데이터</div>
            <div class="stat-num">지방행정인허가</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 6. 검색 결과 출력 영역
# ----------------------------------------------------
_, col_result, _ = st.columns([1, 4, 1])

with col_result:
    if query:
        clean_q = query.replace(" ", "")
        matched_stores = df[
            df['clean_name'].str.contains(clean_q, na=False) | 
            df['clean_addr'].str.contains(clean_q, na=False)
        ]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if matched_stores.empty:
            st.warning(f"검색어 **'{query}'**에 대한 등록 정보가 없습니다.")
            st.info("💡 공공데이터 인허가 법적 상호와 배달앱 표기 상호가 상이할 수 있습니다. 읍·면·동 이름 또는 도로명으로 다시 검색해 보세요.")
        else:
            unique_addrs = matched_stores['address'].unique()
            
            if len(unique_addrs) > 1:
                st.markdown(f"**총 `{len(unique_addrs)}곳`의 연관 소재지가 검색되었습니다.**")
                selected_addr = st.selectbox(
                    "확인할 주소지를 선택하세요:",
                    options=unique_addrs,
                    format_func=lambda x: f"{x} (해당 주소 등록 매장 {len(df[df['address'] == x])}개)"
                )
            else:
                selected_addr = unique_addrs[0]
                
            cluster = df[df['address'] == selected_addr]
            store_count = len(cluster)
            
            # 더치트 스타일 결과 박스
            st.markdown(f"""
            <div class="result-alert-box">
                <div style="font-size: 0.9rem; color: #475569; margin-bottom: 4px;">📍 조회 소재지: <b>{selected_addr}</b></div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #174b85;">해당 주소지에 총 {store_count}개 음식점이 인허가 등록되어 있습니다.</div>
            </div>
            """, unsafe_allow_html=True)
                
            display_table = cluster[['store_name', 'category']].copy()
            display_table.columns = ['인허가 상호명', '인허가 업태']
            display_table.reset_index(drop=True, inplace=True)
            display_table.index = display_table.index + 1
            
            st.table(display_table)

    # ----------------------------------------------------
    # 7. 하단 법적 고지 및 안내 (더치트식 푸터)
    # ----------------------------------------------------
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("ℹ️ 정보 해석에 관한 유의사항 및 법적 고지 (필독)"):
        st.markdown("""
        **1. 동일 주소 등록과 운영 주체의 명확한 구분**
        * **동일 주소 등록이 동일 사업자를 의미하지 않습니다.** 본 서비스는 행정 인허가상 소재지(주소)가 같거나 유사한 매장을 기계적으로 집계한 것일 뿐이며, **각 매장의 실제 운영자나 대표자가 동일인임을 나타내는 것이 결코 아닙니다.**
        * 복합 상가 건물 입점, 정식 시설 기준을 갖춘 공유주방 내 각기 다른 개별 창업자 입점, 독립된 복수 사업자 운영 등은 관련 법령에 따른 정상적이고 합법적인 영업 형태입니다.

        **2. 객관적 행정정보 제공 및 비방 금지 원칙**
        * 본 서비스는 공공데이터포털(data.go.kr)의 지방행정인허가(일반음식점) 공공데이터에 근거한 사실 정보만을 제공하며, 특정 업체를 비방·평가하거나 샵인샵 영업 여부를 단정하지 않습니다.
        * 이용자는 본 조회 결과를 특정 업체에 대한 불필요한 오해나 부정적인 판단의 근거로 단정해서는 안 되며, 대표자 신상이나 개인정보는 일체 수집·제공하지 않습니다.

        **3. 데이터의 최신성 및 정정 요청 안내**
        * 공공데이터 갱신 주기 및 지자체 행정 반영 시점에 따라 현재 폐업·이전·상호 변경된 정보가 일부 포함되어 있을 수 있습니다.
        * 데이터의 정정, 갱신, 삭제 요청이 있으신 업주 및 관계자분께서는 프로젝트 저장소(Issue) 또는 관리자 문의를 통해 접수해 주시면 확인 즉시 조치하겠습니다.
        """)
