import pytube
import os

def download_youtube_audio(url: str) -> str:
    """下載YouTube音頻並返回本地路徑"""
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        download_path = stream.download(output_path="temp_audio")
        
        # 重命名文件為.mp3
        base = os.path.splitext(download_path)[0]
        os.rename(download_path, base + '.mp3')
        return base + '.mp3'
        
    except Exception as e:
        raise RuntimeError(f"下載失敗: {str(e)}")
