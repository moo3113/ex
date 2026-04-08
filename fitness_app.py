import streamlit as st
import time
import streamlit.components.v1 as components

# 設定頁面
st.set_page_config(page_title="燃脂小教練", page_icon="🔥")

# --- 1. 定義語音播報函數 (使用瀏覽器內建 TTS) ---
def speak(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'zh-TW';
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

st.title("🔥 我的專屬燃脂 App")

# --- 2. 側邊欄：選擇與設定 ---
st.sidebar.header("📋 計畫設定")

workout_type = st.sidebar.selectbox(
    "選擇運動方式",
    ["初學者入門", "核心強化", "全身燃脂"]
)

intensity = st.sidebar.selectbox(
    "選擇訓練強度",
    ["輕鬆 (Easy)", "中等 (Moderate)", "挑戰 (Hard)"]
)

# 確保變數在外面先定義，避免 NameError
work_sec, rest_sec, rounds = 30, 20, 4 # 這是預設值

if intensity == "輕鬆 (Easy)":
    work_sec, rest_sec, rounds = 20, 30, 3
elif intensity == "中等 (Moderate)":
    work_sec, rest_sec, rounds = 30, 20, 4
elif intensity == "挑戰 (Hard)":
    work_sec, rest_sec, rounds = 45, 15, 5

# --- 3. 動作資料庫 ---
workout_data = {
    "初學者入門": [
        {"name": "原地踏步", "note": "抬高膝蓋，擺動手臂"},
        {"name": "靠牆深蹲", "note": "背貼牆，大腿平行地面"},
        {"name": "走步波比", "note": "不跳躍，用走的後退再站起"},
        {"name": "側步跨移", "note": "左右移動，保持重心穩健"}
    ],
    "核心強化": [
        {"name": "靜態平板", "note": "身體成一直線，不憋氣"},
        {"name": "登山者", "note": "快節奏收膝，核心收緊"},
        {"name": "俄羅斯轉體", "note": "轉動軀幹，坐姿保持平衡"},
        {"name": "仰臥起坐", "note": "用腹部力量帶起身體"}
    ],
    "全身燃脂": [
        {"name": "開合跳", "note": "全力衝刺速度"},
        {"name": "標準波比跳", "note": "包含俯臥撐與垂直跳躍"},
        {"name": "深蹲跳", "note": "落地要輕，緩衝關節"},
        {"name": "高抬膝跑", "note": "原地快速跑，膝蓋碰手掌"}
    ]
}

selected_exercises = workout_data[workout_type]

# --- 4. 顯示行程表 ---
st.header(f"📅 行程：{workout_type}")
st.info(f"強度：{intensity} | 動作：{work_sec}秒 | 休息：{rest_sec}秒 | 總共：{rounds} 輪")

for i, ex in enumerate(selected_exercises):
    with st.expander(f"動作 {i+1}: {ex['name']}"):
        st.write(f"💡 要點：{ex['note']}")

# --- 5. 開始計時邏輯 ---
if st.button("🚀 開始今日訓練", type="primary"):
    # 先測試語音是否運作
    speak("訓練開始，加油！")
    
    progress_bar = st.progress(0)
    status = st.empty()
    timer = st.empty()
    
    for r in range(1, rounds + 1):
        st.subheader(f"第 {r} 輪開始")
        for ex in selected_exercises:
            # 動作開始語音
            speak(f"開始 {ex['name']}")
            status.error(f"💪 正在進行：{ex['name']}")
            
            for i in range(work_sec, 0, -1):
                timer.metric("剩餘時間", f"{i} 秒")
                progress_bar.progress(int((work_sec - i + 1) / work_sec * 100))
                time.sleep(1)
            
            # 休息開始語音
            speak("休息時間")
            status.success("☕ 休息時間")
            for i in range(rest_sec, 0, -1):
                timer.metric("休息倒數", f"{i} 秒")
                progress_bar.progress(int((rest_sec - i + 1) / rest_sec * 100))
                time.sleep(1)

    speak("恭喜完成所有訓練")
    st.balloons()
    st.success("🎉 太棒了！今天的目標達成了！")
