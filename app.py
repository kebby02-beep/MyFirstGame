import streamlit as st
import time
import random

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
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        '治療藥水': 0,
        '攻擊寶石': 0,
        '時間沙漏': 0,
    }
if 'enemy' not in st.session_state:
    st.session_state.enemy = {
        'name': '魔靈守衛',
        'hp': 40,
        'max_hp': 40,
        'damage': 8,
        'alive': True,
    }
if 'sound_enabled' not in st.session_state:
    st.session_state.sound_enabled = True

# 計時器計算
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, st.session_state.duration - elapsed)

def spawn_enemy():
    mob = random.choice([
        {'name': '幽光妖狼', 'hp': 35, 'max_hp': 35, 'damage': 6},
        {'name': '黑暗樹精', 'hp': 50, 'max_hp': 50, 'damage': 10},
        {'name': '炙焰火龍', 'hp': 70, 'max_hp': 70, 'damage': 14},
    ])
    mob['alive'] = True
    return mob


def use_item(item_name):
    if st.session_state.inventory[item_name] <= 0:
        st.session_state.message = f"你沒有 {item_name} 了！"
        return

    st.session_state.inventory[item_name] -= 1
    if item_name == '治療藥水':
        st.session_state.hp = min(100, st.session_state.hp + 20)
        st.session_state.message = '你喝下治療藥水，恢復 20 HP！'
    elif item_name == '攻擊寶石':
        st.session_state.score += 10
        st.session_state.message = '攻擊寶石閃耀，直接額外 +10 分！'
    elif item_name == '時間沙漏':
        st.session_state.duration += 10
        st.session_state.message = '時間流動，倒數計時延長 10 秒！'


def reset_game():
    st.session_state.score = 0
    st.session_state.hp = 100
    st.session_state.scene = "古老魔法森林"
    st.session_state.weather = "晴天"
    st.session_state.start_time = time.time()
    st.session_state.duration = 30
    st.session_state.message = "熱血教官：再來一次！你已經更強了！"
    st.session_state.inventory = {'治療藥水': 0, '攻擊寶石': 0, '時間沙漏': 0}
    st.session_state.enemy = spawn_enemy()

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

            # 敵人戰鬥機制
            enemy = st.session_state.enemy
            if enemy['alive']:
                if random.random() < 0.7:  # 命中敵人
                    damage = random.randint(8, 16)
                    enemy['hp'] = max(0, enemy['hp'] - damage)
                    st.session_state.score += 5
                    st.session_state.message = f"成功攻擊 {enemy['name']}，造成 {damage} 傷害！"
                    if enemy['hp'] == 0:
                        enemy['alive'] = False
                        st.session_state.score += 15
                        st.session_state.message = f"你擊敗了 {enemy['name']}，獲得 15 分獎勵！"
                        st.session_state.enemy = spawn_enemy()
                else:
                    st.session_state.message = f"攻擊未命中 {enemy['name']}，它準備反擊！"

                # 敵人反擊
                if enemy['alive'] and random.random() < 0.6:
                    st.session_state.hp = max(0, st.session_state.hp - enemy['damage'])
                    st.session_state.message += f" {enemy['name']} 反擊並造成 {enemy['damage']} 傷害！"

            if st.session_state.sound_enabled:
                st.audio("https://www.soundjay.com/button/sounds/button-4.mp3", format='audio/mp3')

    else:
        st.button("🗡️ 熱血點擊", key="click_disabled", disabled=True, use_container_width=True)

    # 道具欄位
    st.write("### 道具商店")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🧪 找到治療藥水" , key='item_hp'):
            st.session_state.inventory['治療藥水'] += 1
            st.session_state.message = '你拾得治療藥水！'
    with c2:
        if st.button("💎 找到攻擊寶石", key='item_atk'):
            st.session_state.inventory['攻擊寶石'] += 1
            st.session_state.message = '你拾得攻擊寶石！'
    with c3:
        if st.button("⏳ 找到時間沙漏", key='item_time'):
            st.session_state.inventory['時間沙漏'] += 1
            st.session_state.message = '你拾得時間沙漏！'

    st.write("### 使用道具")
    use1, use2, use3 = st.columns([1,1,1])
    with use1:
        if st.button("使用治療藥水", key='use_hp'):
            use_item('治療藥水')
    with use2:
        if st.button("使用攻擊寶石", key='use_atk'):
            use_item('攻擊寶石')
    with use3:
        if st.button("使用時間沙漏", key='use_time'):
            use_item('時間沙漏')

    st.write(f"**擁有道具**: 🧪 {st.session_state.inventory['治療藥水']} / 💎 {st.session_state.inventory['攻擊寶石']} / ⏳ {st.session_state.inventory['時間沙漏']}")
    st.write(f"**當前敵人**: {st.session_state.enemy['name']} ({st.session_state.enemy['hp']}/{st.session_state.enemy['max_hp']} HP)")
    st.write(f"**音效**: {'開啟' if st.session_state.sound_enabled else '關閉'}")
    if st.button('🔊 切換音效', key='toggle_sound'):
        st.session_state.sound_enabled = not st.session_state.sound_enabled

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
