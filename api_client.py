from google.cloud import speech, translate_v2 as translate
from google.oauth2 import service_account

class GoogleCloudClient:
    def __init__(self, credential_path):
        self.credentials = service_account.Credentials.from_service_account_file(
            credential_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.speech_client = speech.SpeechClient(credentials=self.credentials)
        self.translate_client = translate.Client(credentials=self.credentials)

def transcribe_speech(audio_path: str, language_code: str = "en-US") -> str:
    """語音轉文字核心邏輯"""
    client = GoogleCloudClient("path/to/service-account.json").speech_client
    
    try:
        with open(audio_path, "rb") as f:
            audio = speech.RecognitionAudio(content=f.read())
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=48000,
            language_code=language_code,
            enable_automatic_punctuation=True
        )
        
        response = client.recognize(config=config, audio=audio)
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        return transcript
    
    except Exception as e:
        print(f"語音轉文字失敗: {str(e)}")
        return ""

def translate_text(text: str, target_lang: str) -> str:
    """文字翻譯核心邏輯"""
    client = GoogleCloudClient("path/to/service-account.json").translate_client
    try:
        return client.translate(text, target_language=target_lang)['translatedText']
    except Exception as e:
        print(f"翻譯失敗: {str(e)}")
        return ""
