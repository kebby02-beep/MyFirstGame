import streamlit as st
import time

# 設定網頁標題
st.set_page_config(page_title="我的 AI 遊戲基地", layout="centered")

# Fantasy 主題專屬 CSS
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #0b3d91 0%, #1e5799 50%, #2b8ad5 100%);
        color: #fff;
    }
    .stApp {
        background: rgba(0, 0, 0, 0.25);
        padding: 1rem;
        border-radius: 14px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }
    .click-button {
        font-size: 1.3rem;
        background: linear-gradient(90deg, #f9d423, #ff4e50);
        color: #111;
        border: 2px solid #fff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔥 熱血教官的奇幻點擊冒險！")

# ============================================================================
# 初始化遊戲狀態（使用 st.session_state）
# ============================================================================
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'hp' not in st.session_state:
    st.session_state.hp = 100
if 'scene' not in st.session_state:
    st.session_state.scene = "古老魔法森林"
if 'weather' not in st.session_state:
    st.session_state.weather = "晴天"
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'duration' not in st.session_state:
    st.session_state.duration = 30  # 秒
if 'message' not in st.session_state:
    st.session_state.message = "熱血教官：準備好一決勝負了嗎？每個點擊都能讓你更靠近傳說中的寶藏！"

# 計時器計算
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, st.session_state.duration - elapsed)

def reset_game():
    st.session_state.score = 0
    st.session_state.hp = 100
    st.session_state.scene = "古老魔法森林"
    st.session_state.weather = "晴天"
    st.session_state.start_time = time.time()
    st.session_state.message = "熱血教官：再來一次！你已經更強了！"

# 場景與天氣效果
if remaining > 0 and st.session_state.hp > 0:
    if st.session_state.score < 20:
        st.session_state.scene = "古老魔法森林"
        st.session_state.weather = "晴天"
    elif st.session_state.score < 50:
        st.session_state.scene = "翡翠瀑布"
        st.session_state.weather = "多雲"
    else:
        st.session_state.scene = "火焰守衛之門"
        st.session_state.weather = "雷雨"

# 背景顏色依天氣變化
bg_color = "#0b3d91"
emoji = "☀️"
if st.session_state.weather == "晴天":
    bg_color = "#0b84f2"
    emoji = "☀️"
elif st.session_state.weather == "多雲":
    bg_color = "#758ba3"
    emoji = "⛅"
elif st.session_state.weather == "雷雨":
    bg_color = "#2a2f4a"
    emoji = "⛈️"

st.markdown(f"<div style='background:{bg_color}; padding: 12px; border-radius:10px;'>" \
            f"<strong>場景: {st.session_state.scene} | 天氣: {st.session_state.weather} {emoji}</strong></div>", unsafe_allow_html=True)

# 熱血教官提示
st.info(st.session_state.message)

col1, col2 = st.columns([2, 1])
with col1:
    st.metric(label="分數", value=st.session_state.score)
    st.metric(label="生命值 (HP)", value=f"{st.session_state.hp}%")
    st.metric(label="倒數計時 (秒)", value=remaining)

with col2:
    st.write("### 行動按鈕")
    if remaining > 0 and st.session_state.hp > 0:
        if st.button("🗡️ 熱血點擊", key="click", help="狂點以累積分數", use_container_width=True):
            st.session_state.score += 1
            st.session_state.hp = max(0, st.session_state.hp - 1)
            st.session_state.message = "熱血教官：太棒了！衝刺你的極限！"
    else:
        st.button("🗡️ 熱血點擊", key="click_disabled", disabled=True, use_container_width=True)

# 遊戲結束判斷
if remaining == 0 or st.session_state.hp == 0:
    st.balloons()
    result_text = "勝利" if st.session_state.hp > 0 else "被擊倒"
    st.success(f"遊戲結束！{result_text}！最終分數：{st.session_state.score}")
    if st.button("重新開始"):
        reset_game()

# 顯示視覺回饋（Emoji 動畫）
st.progress(min(100, st.session_state.score * 2))

st.markdown("---")
st.write("🎮 遊戲循環：初始化 -> 互動 -> 狀態更新 -> 渲染")
st.write("💡 請在終端輸入 `streamlit run app.py` 來啟動遊戲。")
