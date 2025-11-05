# Agentic AI Solution

An advanced Agentic AI system built with LangGraph, Google Gemini, and Python.

## Features

- Multi-step reasoning and planning
- **Information retrieval from web and documents** ✅ Phase 2
- **Multimedia analysis (audio, video, images)** ✅ Phase 3
- **Data analysis and file processing** ✅ Phase 4
- **Code interpretation** ✅ Phase 4
- **Specialized logic engines** ✅ Phase 4
- **Database queries and SQL** ✅ Phase 5
- **Enhanced error handling and logging** ✅ Phase 6
- **Comprehensive test suite** ✅ Phase 6

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API keys:
```bash
copy .env.example .env
# Edit .env and add your API keys:
# - GOOGLE_API_KEY (required)
# - TAVILY_API_KEY (required for web search)
```

4. Set up databases (Phase 5):
```bash
python setup_databases.py
```

5. Run the agent:
```bash
python main.py
```

6. Verify phases:
```bash
python verify_phase1.py  # Basic setup
python verify_phase2.py  # Information retrieval tools
python verify_phase3.py  # Multimedia analysis tools
python verify_phase4.py  # Code, data, and logic tools
python verify_phase5.py  # Database query tools
python verify_phase6.py  # Refinements and testing
```

7. Run tests (optional):
```bash
python tests/test_all_prompts.py  # Test all 20 challenge prompts
```

## Current Capabilities (Phases 1-6) - COMPLETE!

### 🔍 Information Retrieval
- Web search (Tavily API)
- Wikipedia search
- URL content extraction
- Link extraction
- Document text search

### 🎥 Multimedia Analysis
- **Audio:** Transcription (Whisper), multi-language support
- **Vision:** Image analysis, object counting, OCR, chess position analysis
- **Video:** Frame extraction, audio transcription, comprehensive analysis

### 🐍 Code & Data Processing
- **Code Execution:** Safe Python code execution and expression evaluation
- **Data Analysis:** Excel/CSV reading, filtering, calculations (Pandas)
- **Chess Engine:** Position analysis, best move calculation, move validation
- **Text Logic:** Reverse, antonyms, pattern extraction, categorization

### 🗄️ Database Queries
- **SQL Execution:** Direct query execution on SQLite databases
- **Natural Language to SQL:** Convert questions to SQL automatically
- **Schema Exploration:** Inspect database structure and tables
- **Data Exploration:** Preview tables and discover databases
- **Databases:** Baseball stats, Olympics data, Historical competitions

### ⚙️ Refinement & Testing (Phase 6)
- **Enhanced State Management:** Tool usage tracking, error counting
- **Error Handling:** Graceful error recovery and detailed logging
- **Performance Monitoring:** Track metrics, tool usage, success rates
- **Comprehensive Test Suite:** Automated tests for all 20 prompts
- **Logging Infrastructure:** Structured logging with timestamps

### � Challenge Prompts Solved: 20/20 (100%) ✅
- ✅ All original challenge prompts solved!
- ✅ Comprehensive test suite available
- ✅ Production-ready with error handling and logging

## Project Structure

- `main.py` - Entry point for the application
- `agent/` - Core agent logic and graph definition
- `tools/` - Tool implementations for various capabilities
- `tests/` - Test suite for all 20 prompts
