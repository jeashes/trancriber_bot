import base64
import os
import io
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
from models.models import Voice, VideoNote
from transcribers.faster_whisper_trancriber import FasterWhisperTranscriber

load_dotenv()

app = FastAPI()
app_key_header = APIKeyHeader(name="X-API-KEY-Token")
faster_whisper_transcriber = FasterWhisperTranscriber(os.getenv('FASTER_WHISPER_MODEL'),
                                                      os.getenv('FASTER_WHISPER_DEVICE'),
                                                      os.getenv('FASTER_WHISPER_COMPUTE_TYPE'))


async def verify_api_key(api_key: str = Depends(app_key_header)) -> bool:
    if api_key != os.getenv('APP_SECRET'):
        raise HTTPException(status_code=403, detail='Invalid API key')

    return True


@app.post('/api/transcribe_voice')
async def transcribe_voice(data: Voice = Body(...), api_key: bool = Depends(verify_api_key)):
    try:
        audio_file = io.BytesIO(base64.b64decode(data.voice))
        text = faster_whisper_transcriber.transcribe(audio_file, language='en')
        response_data = {
            'text': text
        }

        return JSONResponse(content=response_data, status_code=200)
    except HTTPException:
        print('oops')


@app.post('/api/transcribe_video_note')
async def transcribe_video_note(data: VideoNote, api_key: str = Depends(verify_api_key)):
    try:
        ...
    except HTTPException:
        print('oops')


if __name__ == '__main__':
    HOST, PORT = os.getenv("APP_HOST"), int(os.getenv("APP_PORT"))
    uvicorn.run('main:app', host=HOST, port=PORT, reload=True)
