from faster_whisper import WhisperModel
import os

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

def transcribe_video_to_vtt(video_path, output_vtt, model_size="small"):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    print(f"Loading model '{model_size}'...")
    # Use GPU if available, fallback to CPU
    device = "cuda" if model_size != "tiny" else "cpu"
    model = WhisperModel(model_size, device=device)

    print(f"Transcribing video: {video_path}")
    segments, info = model.transcribe(video_path)

    print(f"Detected language: {info.language}, Probability: {info.language_probability:.2f}")

    with open(output_vtt, "w", encoding="utf-8") as vtt:
        vtt.write("WEBVTT\n\n")
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment.start)
            end = format_timestamp(segment.end)
            vtt.write(f"{i}\n{start} --> {end}\n{segment.text.strip()}\n\n")

    print(f"✅ Subtitles saved as {output_vtt}")
    return output_vtt