import os
import sys
import argparse
from config import *
from utils.transcription import transcribe_video_to_vtt
from utils.json_processing import vtt_to_json, save_json, load_json
from utils.summarization import initialize_gemini, generate_summary

def main():
    # Check for command line arguments
    if len(sys.argv) > 1:
        run_from_command_line()
    else:
        run_interactive_mode()

def run_from_command_line():
    """Run the full pipeline from command line arguments"""
    parser = argparse.ArgumentParser(description='AG Video Intelligence Service')
    parser.add_argument('video_path', help='Path to the video file')
    
    args = parser.parse_args()
    video_file = args.video_path
    
    print("🎥 AG Video Intelligence Service - Command Line Mode")
    print("=" * 50)
    
    # Check for Gemini API key
    if not GEMINI_API_KEY:
        print("❌ Please set GOOGLE_API_KEY_1 in your .env file")
        sys.exit(1)
    
    if not os.path.exists(video_file):
        print(f"❌ File not found: {video_file}")
        sys.exit(1)
    
    try:
        # Step 1: Transcribe
        print("🔄 Step 1/4: Transcribing MP4 to VTT...")
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        vtt_file = os.path.join(OUTPUT_FOLDER, base_name + ".vtt")
        transcribe_video_to_vtt(video_file, vtt_file, WHISPER_MODEL_SIZE)
        print(f"✅ Transcription complete: {vtt_file}")
        
        # Step 2: Convert to JSON
        print("🔄 Step 2/4: Converting VTT to JSON...")
        json_file = os.path.join(OUTPUT_FOLDER, base_name + ".json")
        json_data = vtt_to_json(vtt_file)
        save_json(json_data, json_file)
        print(f"✅ Conversion complete: {json_file}")
        
        # Step 3: Generate Summary
        print("🔄 Step 3/4: Generating summary...")
        model = initialize_gemini(GEMINI_API_KEY)
        summary = generate_summary(json_data, model, GEMINI_API_KEY)
        
        # Step 4: Save final summary
        print("🔄 Step 4/4: Saving results...")
        summary_file = os.path.join(OUTPUT_FOLDER, f"summary_{base_name}.json")
        save_json(summary, summary_file)
        
        print(f"\n🎉 All 4 steps completed successfully!")
        print(f"📁 Output files:")
        print(f"   • VTT: {vtt_file}")
        print(f"   • Transcript JSON: {json_file}")
        print(f"   • Summary JSON: {summary_file}")
        
        sys.exit(0)  # Success exit
        
    except Exception as e:
        print(f"❌ Pipeline failed at step: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)  # Error exit

def run_interactive_mode():
    """Run the interactive menu mode"""
    print("🎥 AG Video Intelligence Service - Interactive Mode")
    print("=" * 50)
    
    # Check for Gemini API key
    if not GEMINI_API_KEY:
        print("❌ Please set GOOGLE_API_KEY_1 in your .env file")
        return
    
    while True:
        print("\nChoose an option:")
        print("1. Transcribe MP4 to VTT")
        print("2. Convert VTT to JSON")
        print("3. Generate Summary from JSON")
        print("4. Full Pipeline (MP4 → Summary)")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            transcribe_mp4()
        elif choice == "2":
            convert_vtt_to_json()
        elif choice == "3":
            generate_summary_from_json()
        elif choice == "4":
            full_pipeline()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def transcribe_mp4():
    """Transcribe MP4 file to VTT"""
    video_file = input("Enter MP4 file path: ").strip()
    
    if not os.path.exists(video_file):
        print(f"❌ File not found: {video_file}")
        return
    
    output_vtt = os.path.join(OUTPUT_FOLDER, os.path.splitext(os.path.basename(video_file))[0] + ".vtt")
    
    try:
        transcribe_video_to_vtt(video_file, output_vtt, WHISPER_MODEL_SIZE)
        print(f"✅ Transcription complete: {output_vtt}")
    except Exception as e:
        print(f"❌ Transcription failed: {e}")

def convert_vtt_to_json():
    """Convert VTT file to JSON"""
    vtt_file = input("Enter VTT file path: ").strip()
    
    if not os.path.exists(vtt_file):
        print(f"❌ File not found: {vtt_file}")
        return
    
    try:
        json_data = vtt_to_json(vtt_file)
        output_json = os.path.join(OUTPUT_FOLDER, os.path.splitext(os.path.basename(vtt_file))[0] + ".json")
        save_json(json_data, output_json)
        print(f"✅ Conversion complete: {output_json}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")

def generate_summary_from_json():
    """Generate summary from JSON transcript"""
    json_file = input("Enter JSON transcript file path: ").strip()
    
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        return
    
    try:
        # Initialize Gemini
        model = initialize_gemini(GEMINI_API_KEY)
        
        # Load transcript
        transcript_json = load_json(json_file)
        
        # Generate summary
        print("🔄 Generating summary... This may take a few minutes.")
        summary = generate_summary(transcript_json, model, GEMINI_API_KEY)
        
        # Save summary
        output_file = os.path.join(OUTPUT_FOLDER, f"summary_{os.path.splitext(os.path.basename(json_file))[0]}.json")
        save_json(summary, output_file)
        print(f"✅ Summary generated: {output_file}")
        
    except Exception as e:
        print(f"❌ Summary generation failed: {e}")

def full_pipeline():
    """Complete pipeline: MP4 → VTT → JSON → Summary"""
    video_file = input("Enter MP4 file path: ").strip()
    
    if not os.path.exists(video_file):
        print(f"❌ File not found: {video_file}")
        return
    
    try:
        # Step 1: Transcribe
        print("🔄 Step 1/3: Transcribing MP4 to VTT...")
        base_name = os.path.splitext(os.path.basename(video_file))[0]
        vtt_file = os.path.join(OUTPUT_FOLDER, base_name + ".vtt")
        transcribe_video_to_vtt(video_file, vtt_file, WHISPER_MODEL_SIZE)
        
        # Step 2: Convert to JSON
        print("🔄 Step 2/3: Converting VTT to JSON...")
        json_file = os.path.join(OUTPUT_FOLDER, base_name + ".json")
        json_data = vtt_to_json(vtt_file)
        save_json(json_data, json_file)
        
        # Step 3: Generate Summary
        print("🔄 Step 3/3: Generating summary...")
        model = initialize_gemini(GEMINI_API_KEY)
        summary = generate_summary(json_data, model, GEMINI_API_KEY)
        
        # Save final summary
        summary_file = os.path.join(OUTPUT_FOLDER, f"summary_{base_name}.json")
        save_json(summary, summary_file)
        
        print(f"✅ Full pipeline complete!")
        print(f"   VTT: {vtt_file}")
        print(f"   Transcript JSON: {json_file}")
        print(f"   Summary JSON: {summary_file}")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")

if __name__ == "__main__":
    main()