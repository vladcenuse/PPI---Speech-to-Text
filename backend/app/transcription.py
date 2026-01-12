import os
import requests
from pydantic import BaseModel
from dotenv import load_dotenv
from deepgram import DeepgramClient
from huggingface_hub import InferenceClient
import io
import soundfile as sf

class TranscriptionResult(BaseModel):
    text: str

load_dotenv()


DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")

hf_client = InferenceClient(
    provider="hf-inference",
    api_key= HF_TOKEN
)



def transcribe_with_whisper_deepgram(
    audio_content: bytes,
    language: str = "ro"
) -> TranscriptionResult:
    if not DEEPGRAM_API_KEY:
        raise RuntimeError("DEEPGRAM_API_KEY is not set")

    dg = DeepgramClient(api_key=DEEPGRAM_API_KEY)

    response = dg.listen.v1.media.transcribe_file(
        request=audio_content,
        model="whisper",
        language=language,
        smart_format=True,
    )

    text = response.results.channels[0].alternatives[0].transcript.strip()

    if not text:
        raise RuntimeError("Empty transcript from Deepgram")

    return TranscriptionResult(text=text)

def transcribe_with_nova3(
    audio_content: bytes,
    language: str = "ro"
) -> TranscriptionResult:
    if not DEEPGRAM_API_KEY:
        raise RuntimeError("DEEPGRAM_API_KEY is not set")

    dg = DeepgramClient(api_key=DEEPGRAM_API_KEY)

    response = dg.listen.v1.media.transcribe_file(
        request=audio_content,
        model="nova-3",
        language=language,
        smart_format=True,
    )

    text = response.results.channels[0].alternatives[0].transcript.strip()

    if not text:
        raise RuntimeError("Empty transcript from Deepgram")

    return TranscriptionResult(text=text)


def transcribe_with_whisper_hosted_api(
    audio_content: bytes,
    language: str = "ro"
) -> TranscriptionResult:
    WHISPER_HOSTED_API_URL = "https://sebiflorinp-Whisper-Model-Hosting.hf.space/transcribe"

    audio_file = io.BytesIO(audio_content)
    data, samplerate = sf.read(audio_file)

    if samplerate != 16000:
        import resampy
        data = resampy.resample(data.T, samplerate, 16000)
        samplerate = 16000

    wav_io = io.BytesIO()
    sf.write(wav_io, data.T, samplerate, format="WAV")
    wav_io.seek(0)

    files = {"file": ("audio.wav", wav_io.read(), "audio/wav")}
    response = requests.post(
        WHISPER_HOSTED_API_URL,
        files=files,
        timeout=120
    )
    response.raise_for_status()

    data = response.json()
    text = data.get("text", "").strip()
    if not text:
        raise RuntimeError("Empty transcript from Whisper API")

    return TranscriptionResult(text=text)

def transcribe_audio(
    audio_content: bytes,
    provider: str = "deepgram_nova-3",
    language: str = "ro"
) -> TranscriptionResult:

    print(provider)
    provider = provider.lower()
    print(f"provider: {provider}")

    if provider == "deepgram_whisper":
        return transcribe_with_whisper_deepgram(audio_content, language)

    if provider == "deepgram_nova-3":
        return transcribe_with_nova3(audio_content, language)

    if provider == "whisper_hosted_api":
        return transcribe_with_whisper_hosted_api(audio_content, language)

    raise ValueError(f"Unsupported transcription provider: {provider}")
