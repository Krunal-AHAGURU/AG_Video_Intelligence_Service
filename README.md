# AG Video Intelligence Service

A comprehensive video intelligence service that provides AI-powered video analysis capabilities, including object detection, scene recognition, and metadata extraction.

## Project Structure

```
video_intelligence_service/
    video_intelligence_service_sdk/
    ├── __init__.py              # Package initialization
    ├── utils/                   # Utility modules
    │   ├── __init__.py         # Utils package initialization
    │   ├── json_processing.py  # JSON data processing utilities
    │   ├── summarization.py    # Text summarization capabilities
    │   └── transcription.py    # Video/audio transcription services
    ├── env/                    # Environment configuration
    ├── config.py               # SDK configuration management
    ├── main.py                 # Main entry point and examples
    └── requirements.txt        # Python dependencies
<!-- Oter files -->
├── index.html                      # Web interface
├── README.md                       # Project documentation
└── Video_Intelligence_Service.ipynb  # Interactive notebook
```

## Quick Start

### Prerequisites

- Python 3.8+
- Required dependencies (see `requirements.txt`)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd video_intelligence_service
```

2. Install dependencies:
```bash
cd video_intelligence_service_sdk
pip install -r requirements.txt
```

3. Configure environment variables in the `env/` directory

4. Run the service:
```bash
python main.py
```

### Interactive Notebook

**You can import the `Video_Intelligence_Service.ipynb` file to Google Colab to get visual step-by-step guidance and interactive examples of the video intelligence capabilities.**

### SDK Access

The main SDK and API implementations are located inside the `video_intelligence_service/` folder, providing programmatic access to all video analysis features.

## Usage
````markdown
### Command Line Mode (🆕 New Feature)

Run the full transcription pipeline automatically by passing the video path as an argument.

```bash
python main.py "D:\ag-demo-video\std11ChemNEETL8Isomerism - ch1\EC1015SS160421V1.mp4"
````

---

### Interactive Mode (💬 Existing)

Start the tool without any arguments to enter interactive mode.

```bash
python main.py
```
---

### 🧩 Key Features Added

#### Command Line Argument Support

Uses `argparse` to handle video path input directly from the terminal.

#### Automatic Pipeline Execution

Runs all 4 processing steps automatically when a video path is provided.

#### Proper Exit Codes

* `0` → Successful completion
* `1` → Error occurred (with detailed logging)

#### Error Handling

Comprehensive `try-except` blocks with full traceback for easy debugging.

#### Dual Mode Compatibility

Maintains backward compatibility with the existing interactive workflow.

#### Clear Success Message

Prints ✅ **“All 4 steps completed successfully!”** upon successful execution.


## Configuration

Edit `config.py` to customize analysis parameters, model settings, and service behavior.

## License

All Rights Recvied  : Ahaguru Analytics team :)

## Support

For issues and questions, please refer to the documentation or create an issue in the project repository or connect krunalrana.ahaguru@gmail.com.