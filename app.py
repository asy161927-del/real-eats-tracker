import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="배달 식당 한지붕(샵인샵) 조회기", layout="centered")

st.title("배달 식당 한지붕(샵인샵) 조회기")
st.caption("공공데이터 기반으로 동일 사업장 주소지에 3개 이상 등록된 배달 전문 매장을 탐색합니다.")

# 정제된 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv("delivery_stores.csv")

df = load_data()

# 검색창 UI
search_query = st.text_input("식당 이름을 입력하세요 (예: 김치찌개, 초밥, 할매 등)", placeholder="매장명 또는 상호 입력...")

if search_query:
    matched = df[df['store_name'].str.contains(search_query, na=False)]

    if not matched.empty:
        selected_store = matched.iloc[0]
        target_addr = selected_store['address']

        family_stores = df[df['address'] == target_addr]
        store_count = len(family_stores)

        st.divider()
        st.subheader(f"📌 '{selected_store['store_name']}' 조회 결과")
        st.write(f"**소재지 주소:** {target_addr}")

        if store_count >= 3:
            st.warning(f"⚠️ 이 주소지에는 현재 **총 {store_count}개의 매장**이 한 주방/사업장으로 등록되어 있습니다.")
        else:
            st.info(f"등록 매장 수: {store_count}개")

        st.markdown("#### 함께 등록된 식당 상호 목록")
        for idx, row in family_stores.iterrows():
            cat_name = str(row['category']) if pd.notna(row['category']) else "기타"
            st.write(f"- **{row['store_name']}** (`{cat_name}`)")
    else:
        st.error(f"'{search_query}' 검색 결과가 없습니다. (3개 이상 다중 등록된 매장 목록에 없음)")
