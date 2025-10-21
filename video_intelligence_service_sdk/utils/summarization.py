import google.generativeai as genai
import json
import re
from datetime import datetime

def initialize_gemini(api_key):
    """Initialize Gemini model"""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")  # Using flash for faster processing

def generate_summary_prompt(transcript_json):
    """Generate the prompt for summarization"""
    
    prompt = """
You are an expert educational content analyst and summarizer.

Your task is to analyze a transcript JSON (list of time-stamped text segments) and generate a detailed, structured JSON summary suitable for LMS (Learning Management System) display for students of Classes 10–12 preparing for JEE and NEET.

Maintain the following structure and keys exactly:

1. "overall_summary" → an object containing:
    - "summary_title": a short, meaningful title summarizing the entire lecture (e.g., "Understanding Force Resolution and Vector Addition in Physics").
    - "summary_text": a 3–4 paragraph overall summary describing the full lecture or video in a clear, engaging tone.

2. "starting_build_up" → describe how the session begins, what context or motivation is provided, and what students will learn.

3. "timestamp_wise_summary" → an array of objects, each containing:
    - "start_time"
    - "end_time"
    - "summary_title": a short title for that section or subtopic (e.g., "Vector Addition and Resultant Forces").
    - "summary": a concise description of what is discussed in that segment.

4. "end_summary" → a concise wrap-up highlighting final concepts, conclusions, or takeaways.

5. "chapters" → a list of key chapters with:
    - "chapter_title"
    - "start_time"
    - "end_time"
    - "description"

6. "chapter_wise_summary" → a descriptive summary for each chapter, where each item includes:
    - "chapter_title": the same title from the chapters list.
    - "summary_text": a natural paragraph summarizing what the chapter covers, in a student-friendly tone.

7. "tags" → 8–12 short keywords or topic phrases that describe the main concepts.

8. "keyframes" → important timestamps where a key concept, diagram, derivation, or visual explanation is introduced, with:
    - "timestamp"
    - "description"

9. "Q&A" → 6–10 question-answer pairs that test understanding of the topic.
   - Include both conceptual and numerical questions.
   - Include 3–4 relevant **numerical or problem-based questions** suitable for JEE/NEET level.
   - Remaining should be conceptual or theoretical.
   - Ensure questions are realistic, exam-oriented, and derived directly from the lecture concepts.
   - Answers should be concise, clear, and accurate.

Stylistic instructions:
- Write in a smooth, student-friendly, educational tone suitable for LMS summaries.
- Do not mention textbooks, sections, or say "the teacher said".
- Use natural paragraph flow (not bullet points) for summaries.
- Maintain a clear connection between chapters and timestamp summaries.
- Output must be **only valid JSON** (no explanations or extra text outside JSON).

Transcript:
"""
    
    return f"{prompt}\n{json.dumps(transcript_json)}"

def generate_summary(transcript_json, model, api_key):
    """Generate summary using Gemini"""
    prompt = generate_summary_prompt(transcript_json)
    
    try:
        response = model.generate_content(prompt)
        
        # Try parsing output as JSON
        try:
            result_json = json.loads(response.text)
        except Exception:
            # If direct parsing fails, try to extract JSON
            cleaned = re.search(r'\{[\s\S]*\}', response.text)
            if cleaned:
                result_json = json.loads(cleaned.group(0))
            else:
                result_json = {"error": "Could not parse JSON", "raw_output": response.text}
        
        # Add metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        enhanced_json = {
            "generated_timestamp": timestamp,
            "summary_data": result_json
        }
        
        return enhanced_json
        
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}