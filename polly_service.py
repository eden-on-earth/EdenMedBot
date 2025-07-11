import boto3

polly = boto3.client("polly")

def synthesize_speech(text, output_path="output.mp3"):
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Joanna"
    )
    with open(output_path, "wb") as f:
        f.write(response["AudioStream"].read())
    return output_path
