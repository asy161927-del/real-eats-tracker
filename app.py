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
# 2. 커스텀 CSS (신뢰감을 주는 흑청색/다크 네이비 테마)
# ----------------------------------------------------
st.markdown("""
<style>
    /* 전체 여백 및 폰트 */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 780px;
    }
    
    /* 헤더 텍스트 스타일링 */
    .brand-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
        text-align: center;
        letter-spacing: -0.03em;
    }
    .brand-subtitle {
        font-size: 1.05rem;
        color: #334155;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.4rem;
    }
    .brand-caption {
        font-size: 0.88rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 1.8rem;
    }
    
    /* 상단 미니 현황 바 */
    .stat-pill {
        display: flex;
        justify-content: center;
        gap: 16px;
        background-color: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 9999px;
        padding: 6px 18px;
        font-size: 0.82rem;
        color: #475569;
        margin: 0 auto 1.8rem auto;
        width: fit-content;
    }
    .stat-pill strong {
        color: #0f172a;
    }

    /* 검색창 힌트 스타일링 */
    .search-hint {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: -10px;
        margin-bottom: 1.5rem;
        text-align: left;
    }

    /* 결과 요약 카드 (다크 네이비 테두리 & 배경) */
    .result-summary-card {
        background-color: #0f172a;
        color: #ffffff;
        border-radius: 12px;
        padding: 16px 20px;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.1);
    }
    .result-summary-card .addr-text {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    .result-summary-card .count-text {
        font-size: 1.25rem;
        font-weight: 700;
        color: #38bdf8;
    }

    /* 인라인 뱃지 */
    .category-badge {
        background-color: #e2e8f0;
        color: #1e293b;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
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
# 4. 헤더 및 통합 검색창 UI
# ----------------------------------------------------
st.markdown('<div class="brand-title">🏍️ 한집 (Han-Jib)</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">공공데이터 기반 복수 음식점 인허가 간이 조회기</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-caption">행정안전부 일반음식점 인허가 데이터 기반 동일 소재지 등록 현황 검색</div>', unsafe_allow_html=True)

# 간이 현황 뱃지 (더치트 스타일)
st.markdown(f'''
<div class="stat-pill">
    <span>등록 매장 <strong>{len(df):,}개</strong></span>
    <span>•</span>
    <span>밀집 주소 <strong>{df["address"].nunique():,}곳</strong></span>
</div>
''', unsafe_allow_html=True)

# 단일 통합 검색창 (더치트/홈택스 방식)
query = st.text_input(
    label="검색창",
    placeholder="배달앱 상호명 또는 동/도로명 주소를 입력하세요",
    label_visibility="collapsed"
).strip()

st.markdown('<div class="search-hint">💡 <b>검색 예시:</b> 불당동, 두정동, 원성동, 와촌동, 피자, 버거, 탕수육 등</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# 5. 검색 결과 렌더링
# ----------------------------------------------------
if query:
    clean_q = query.replace(" ", "")
    
    # 상호명 또는 주소지 동시 매칭
    matched_stores = df[
        df['clean_name'].str.contains(clean_q, na=False) | 
        df['clean_addr'].str.contains(clean_q, na=False)
    ]
    
    if matched_stores.empty:
        st.warning(f"검색어 **'{query}'**에 대한 등록 정보가 없습니다.")
        st.info("공공데이터 인허가상 법적 상호와 배달앱 표기 상호가 상이할 수 있습니다. 읍·면·동 이름 또는 도로명으로 다시 검색해 보세요.")
    else:
        unique_addrs = matched_stores['address'].unique()
        
        # 일치하는 주소지가 여러 개인 경우 직관적인 선택 드롭다운 제공
        if len(unique_addrs) > 1:
            st.markdown(f"**총 `{len(unique_addrs)}곳`의 연관 소재지가 발견되었습니다.**")
            selected_addr = st.selectbox(
                "확인할 주소지를 선택하세요:",
                options=unique_addrs,
                format_func=lambda x: f"{x} (등록 매장 {len(df[df['address'] == x])}개)"
            )
        else:
            selected_addr = unique_addrs[0]
            
        cluster = df[df['address'] == selected_addr]
        store_count = len(cluster)
        
        # 더치트 스타일의 다크 네이비 요약 카드
        st.markdown(f'''
        <div class="result-summary-card">
            <div class="addr-text">📍 조회 소재지: {selected_addr}</div>
            <div class="count-text">해당 주소지 등록 매장 총 {store_count}개</div>
        </div>
        ''', unsafe_allow_html=True)
            
        # 상세 매장 목록
        display_table = cluster[['store_name', 'category']].copy()
        display_table.columns = ['인허가 상호명', '인허가 업태']
        display_table.reset_index(drop=True, inplace=True)
        display_table.index = display_table.index + 1
        
        st.table(display_table)

# ----------------------------------------------------
# 6. 법적 안전장치 및 유의사항 (접이식 기본 닫힘 구조로 깔끔함 유지)
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
