import boto3
import time

transcribe = boto3.client("transcribe")

def transcribe_audio(audio_uri, job_name):
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(2)

    transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    return transcript_uri  # You can download and parse this JSON
