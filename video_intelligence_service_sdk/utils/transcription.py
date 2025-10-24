# from faster_whisper import WhisperModel
# import os

# def format_timestamp(seconds: float) -> str:
#     hours = int(seconds // 3600)
#     minutes = int((seconds % 3600) // 60)
#     secs = int(seconds % 60)
#     millis = int((seconds - int(seconds)) * 1000)
#     return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

# def transcribe_video_to_vtt(video_path, output_vtt, model_size="small"):
#     if not os.path.exists(video_path):
#         raise FileNotFoundError(f"Video file not found: {video_path}")

#     print(f"Loading model '{model_size}'...")
#     # Use GPU if available, fallback to CPU
#     device = "cuda" if model_size != "tiny" else "cpu"
#     model = WhisperModel(model_size, device=device)

#     print(f"Transcribing video: {video_path}")
#     segments, info = model.transcribe(video_path)

#     print(f"Detected language: {info.language}, Probability: {info.language_probability:.2f}")

#     with open(output_vtt, "w", encoding="utf-8") as vtt:
#         vtt.write("WEBVTT\n\n")
#         for i, segment in enumerate(segments, start=1):
#             start = format_timestamp(segment.start)
#             end = format_timestamp(segment.end)
#             vtt.write(f"{i}\n{start} --> {end}\n{segment.text.strip()}\n\n")

#     print(f"✅ Subtitles saved as {output_vtt}")
#     return output_vtt

from faster_whisper import WhisperModel
import os
import psutil  # For system memory info
import traceback

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

def estimate_model_memory(model_size: str) -> float:
    """Rough estimate of model RAM usage in GB"""
    estimates = {
        "tiny": 0.3,
        "base": 0.5,
        "small": 1.2,
        "medium": 2.6,
        "large-v2": 5.5
    }
    return estimates.get(model_size, 1.0)

def log_memory_status(model_size: str):
    mem = psutil.virtual_memory()
    total_gb = mem.total / (1024 ** 3)
    available_gb = mem.available / (1024 ** 3)
    est_needed = estimate_model_memory(model_size)

    print(f"💾 System Memory: {available_gb:.2f} GB available / {total_gb:.2f} GB total")
    print(f"🧠 Estimated required for model '{model_size}': ~{est_needed:.2f} GB")

    if available_gb < est_needed * 1.2:  # add safety buffer
        print("⚠️ Warning: You may not have enough RAM to load this model efficiently!")
    else:
        print("✅ Memory seems sufficient for this model.")

def transcribe_video_to_vtt(video_path, output_vtt, model_size="small"):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    print(f"\n📂 Input video: {video_path}")
    print(f"🎯 Output subtitle: {output_vtt}")
    print(f"🧩 Model size: {model_size}")
    
    log_memory_status(model_size)

    try:
        print(f"\n🚀 Loading model '{model_size}' on CPU (int8 precision)...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

        print(f"🎧 Transcribing video: {video_path}")
        segments, info = model.transcribe(video_path)

        print(f"🌐 Detected language: {info.language}, Probability: {info.language_probability:.2f}")

        with open(output_vtt, "w", encoding="utf-8") as vtt:
            vtt.write("WEBVTT\n\n")
            for i, segment in enumerate(segments, start=1):
                start = format_timestamp(segment.start)
                end = format_timestamp(segment.end)
                vtt.write(f"{i}\n{start} --> {end}\n{segment.text.strip()}\n\n")

        print(f"\n✅ Subtitles saved as {output_vtt}")
        return output_vtt

    except Exception as e:
        print("\n❌ Transcription failed due to an error:")
        print(traceback.format_exc())
        print("💡 Tip: Try using a smaller model like 'base' or 'tiny' if memory is low.")
        return None
