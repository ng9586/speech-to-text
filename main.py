import streamlit as st
from video_processor import download_youtube_audio
from api_client import transcribe_speech, translate_text

# 設定頁面標題和佈局
st.set_page_config(page_title="YouTube Translator", layout="wide")
st.title("🎥 YouTube影片即時翻譯工具")

# 創建輸入欄和選擇器
video_url = st.text_input("輸入YouTube影片URL", placeholder="https://youtu.be/...")
target_language = st.selectbox("選擇翻譯語言", ["中文", "英文", "日文", "西班牙文"])

# 語言代碼映射
LANGUAGE_MAP = {
    "中文": "zh-CN",
    "英文": "en",
    "日文": "ja",
    "西班牙文": "es"
}

if st.button("開始翻譯"):
    if not video_url:
        st.error("請輸入有效的YouTube URL！")
    else:
        try:
            with st.spinner("⏳ 正在處理影片..."):
                # 後端處理流程
                audio_path = download_youtube_audio(video_url)
                transcript = transcribe_speech(audio_path)
                translated = translate_text(transcript, LANGUAGE_MAP[target_language])
                
            # 顯示結果
            st.subheader("翻譯結果")
            st.code(translated, language="text")
            
            # 顯示原始文本對比
            with st.expander("查看原始文本"):
                st.write(transcript)
                
        except Exception as e:
            st.error(f"處理失敗: {str(e)}")
