import re
import json

def vtt_to_json(vtt_file):
    """Convert VTT file to JSON format"""
    with open(vtt_file, "r", encoding="utf-8") as f:
        vtt_content = f.read()

    # Split into blocks by blank lines
    blocks = re.split(r'\n\s*\n', vtt_content.strip())
    audio_segments = []

    for i, block in enumerate(blocks):
        lines = block.splitlines()
        if len(lines) >= 3:  # id, time, text
            time_line = lines[1]
            text_lines = lines[2:]
            # Extract start and end times
            match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s-->\s(\d{2}:\d{2}:\d{2}\.\d{3})', time_line)
            if match:
                start_time = match.group(1)
                end_time = match.group(2)
                # Combine text lines into one transcript
                transcript = " ".join(text_lines).replace("\n", " ").strip()
                audio_segments.append({
                    "id": i,
                    "transcript": transcript,
                    "start_time": start_time,
                    "end_time": end_time
                })

    return {"audio_segments": audio_segments}

def save_json(data, filename):
    """Save JSON data to file"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON saved as {filename}")

def load_json(filename):
    """Load JSON data from file"""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)