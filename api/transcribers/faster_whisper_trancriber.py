from faster_whisper import WhisperModel
from typing import BinaryIO
from .transcriber import Transcriber


class FasterWhisperTranscriber(Transcriber):
    def __init__(self, model: str, device: str = 'cuda', compute_type: str = 'int8') -> None:
        self.model = WhisperModel(model_size_or_path=model, device=device, compute_type=compute_type, cpu_threads=12)

    def transcribe(self, audio_file: BinaryIO, language: str) -> str:
        segments, _ = self.model.transcribe(audio_file, language, temperature=0.2)
        transcript = next(segments, '')
        return transcript.text
