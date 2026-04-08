import streamlit as st
import time
import streamlit.components.v1 as components

# --- 1. 定義播放聲音的函數 ---
def play_sound():
    # 這是一段 JavaScript，會播放一個簡單的系統提示音（嗶聲）
    sound_html = """
    <audio autoplay>
      <source src="https:// character-assets.s3.amazonaws.com/beep.mp3" type="audio/mp3">
      <source src="https://www.soundjay.com/buttons/beep-07a.mp3" type="audio/mp3">
    </audio>
    """
    # 也可以使用瀏覽器內建的合成聲音 (語音提示)
    # sound_html = "<script>speechSynthesis.speak(new SpeechSynthesisUtterance('Next'));</script>"
    components.html(sound_html, height=0)

# ... (中間的選單與邏輯與之前相同) ...

# --- 2. 在計時迴圈中加入聲音 ---
if st.button("🚀 開始今日訓練", type="primary"):
    progress_bar = st.progress(0)
    status = st.empty()
    timer = st.empty()
    
    for r in range(1, rounds + 1):
        for ex in selected_exercises:
            # --- 動作開始 ---
            status.error(f"💪 正在進行：{ex['name']}")
            play_sound()  # 動作開始響一聲
            for i in range(work_sec, 0, -1):
                timer.metric("剩餘時間", f"{i} 秒")
                progress_bar.progress(int((work_sec - i + 1) / work_sec * 100))
                time.sleep(1)
            
            # --- 休息開始 ---
            status.success("☕ 休息時間")
            play_sound()  # 休息開始響一聲
            for i in range(rest_sec, 0, -1):
                timer.metric("休息倒數", f"{i} 秒")
                progress_bar.progress(int((rest_sec - i + 1) / rest_sec * 100))
                time.sleep(1)

    st.balloons()
    play_sound() # 全部結束響一聲
    st.success("🎉 太棒了！您完成了今天的目標！")
