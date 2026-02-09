# Assistly: Voice Assistant with LLM-Driven Intent Routing

**Assistly** is a comprehensive, modular Python-based voice assistant that enables users to interact with their system through natural voice commands. It combines advanced intent classification, speech recognition and synthesis, and LLM integration (Google Gemini) to provide an extensible set of capabilities and skills.

---

## 📖 Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites & Installation](#prerequisites--installation)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Built-in Modules](#built-in-modules)

---

## ✨ Features

- **Voice Input/Output**: Continuous speech recognition and natural text-to-speech responses using Google Cloud Speech API and pyttsx3
- **AI-Powered Intent Classification**: Uses Google Gemini LLM to intelligently parse natural language commands with entity extraction and confidence scoring
- **Entity Extraction**: Automatically identifies and extracts relevant parameters (locations, search terms, durations, etc.) from user commands for precise action execution
- **Modular Architecture**: Designed with a plugin-like skill system where each module is independent and can be easily extended or replaced
- **LLM Integration**: Deep integration with Google Gemini API for intelligent command classification, response generation, and context awareness
- **13+ Pre-built Skills**: Includes weather, news, timer, YouTube player, system utilities, web search, app launcher, and more
- **Confidence Threshold**: Built-in safety mechanism that prevents execution of low-confidence intent classifications, reducing false activations
- **Comprehensive Logging**: Debug-ready logging with dual output (console for INFO+ events, files for DEBUG+ events) for troubleshooting and monitoring
- **Graceful Error Handling**: Fallback responses and exception handling ensure the assistant remains responsive even when external APIs are unavailable
- **Event-Driven Pipeline**: Speech is captured, processed through a multi-stage pipeline, and results are routed to appropriate modules
- **Extensible Design**: Add new skills by creating simple Python modules without modifying core application code
- **API-First Approach**: Integrates with third-party services (WeatherAPI, NewsAPI, YouTube, Google Search) while maintaining modularity
- **Configurable via Environment**: All API keys and settings managed through `.env` files for easy deployment across environments
- **Cross-Platform**: Works on Windows, macOS, and Linux with the same codebase

---

## 🏗️ Architecture Overview

Assistly follows a modular pipeline architecture where user voice is converted to text, analyzed via Google Gemini LLM to classify intent and extract entities, routed to the appropriate module, and responded with text-to-speech:

```
User Voice Input
        ↓
[Recognizer] - Speech Recognition (Google API)
        ↓
Command (text)
        ↓
[Intent Engine] - AI Classification (Google Gemini)
        ↓
(Intent, Entities, Confidence)
        ↓
[Router] - Route to appropriate module
        ↓
[Module] - Execute skill (weather, jokes, news, etc.)
        ↓
Response (text)
        ↓
[Speech] - Text-to-Speech (pyttsx3)
        ↓
User Audio Output
```

---

## 📋 Prerequisites & Installation

### System Requirements
- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Microphone**: Required for speech input
- **Speakers**: Required for audio output

### 1. Clone the Repository
```bash
git clone https://github.com/AdityaKarun/assistly.git
cd assistly
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pyttsx3` | 2.99 | Text-to-speech engine |
| `pyjokes` | 0.8.3 | Programming jokes API |
| `requests` | 2.32.5 | HTTP requests for APIs |
| `python-dotenv` | 1.2.1 | Environment variable management |
| `newsapi-python` | 0.2.7 | News headlines API |
| `SpeechRecognition` | 3.14.3 | Speech-to-text recognition |
| `PyAudio` | 0.2.14 | Microphone audio input |
| `pywhatkit` | 5.4 | YouTube and web automation |
| `psutil` | 7.2.1 | System information queries |

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root with the following keys:

```env
# Required - Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Optional APIs (required for specific features)
WEATHER_API_KEY=your_weatherapi_key_here
NEWS_API_KEY=your_newsapi_key_here
```

### How to Get API Keys

1. **Google Gemini API**
   - Visit: https://aistudio.google.com/apikey
   - Create new API key
   - Set it in `.env`

2. **Weather API**
   - Visit: https://www.weatherapi.com
   - Sign up and get free API key
   - Set it in `.env`

3. **News API**
   - Visit: https://newsapi.org
   - Register and get free API key
   - Set it in `.env`

---

## 🚀 Usage

### Basic Startup
```bash
python main.py
```

The assistant will greet you, listen for voice commands, classify the intent using Google Gemini, execute the appropriate module, and respond via text-to-speech. Say "goodbye" or use Ctrl+C to exit.

---

## 📂 Project Structure

```
assistly/
├── core/                        # Core application components
│   ├── intent_classifier.py
│   ├── llm_client.py
│   ├── logger_config.py
│   ├── recognizer.py
│   ├── router.py
│   └── speech.py
├── logs/                        # Application logs directory
├── modules/                     # Individual skill modules
│   ├── courtesy_handler.py
│   ├── date_and_time.py
│   ├── greet.py
│   ├── joke.py
│   ├── location.py
│   ├── news.py
│   ├── open_app_or_url.py
│   ├── search_google.py
│   ├── system_info.py
│   ├── timer.py
│   ├── weather.py
│   └── youtube_player.py
├── .gitignore                   # Git ignore rules
├── LICENSE                      # Project license
├── README.md                    # Project documentation
├── main.py                      # Application entry point and main loop
└── requirements.txt             # Python dependencies and packages
```

---

## 🔧 Core Components

- **Intent Classification Engine** (`core/intent_classifier.py`) - Classifies voice commands using Google Gemini LLM with entity extraction and confidence scoring
- **Speech Recognizer** (`core/recognizer.py`) - Captures microphone input and converts speech to text using Google Cloud Speech API
- **Text-to-Speech** (`core/speech.py`) - Converts text responses to natural speech at 170 WPM using pyttsx3 with Microsoft Zira voice
- **LLM Client** (`core/llm_client.py`) - Google Gemini API integration for intelligent command classification and processing
- **Router** (`core/router.py`) - Dispatches classified intents to appropriate skill modules with confidence threshold validation

---

## 📦 Built-in Modules

| Module | File | Description | Example Commands |
|--------|------|-------------|-------------------|
| **Greeter** | `greet.py` | Time-based greeting (Good Morning/Afternoon/Evening) | - |
| **Date/Time** | `date_and_time.py` | Current date, time, and day information | "What time is it?", "Tell me the date", "What's today?" |
| **Weather** | `weather.py` | Real-time weather using WeatherAPI.com | "What's the weather in London?", "How is the weather?", "How is the sky in Paris" |
| **News** | `news.py` | Latest headlines from BBC News | "What's happening in news?", "Tell me today's headlines", "Any news updates?" |
| **Jokes** | `joke.py` | Random programming jokes via PyJokes | "Tell me a joke", "Make me laugh", "Say something funny" |
| **Location** | `location.py` | IP-based geolocation detection | "Where am I?", "What's my location?" |
| **Google Search** | `search_google.py` | Internet search capability | "Search for Python tutorials", "Google machine learning", "Look up quantum physics" |
| **YouTube Player** | `youtube_player.py` | YouTube video search and playback | "Play despacito on YouTube", "Play the odyssey trailer" |
| **App/URL Launcher** | `open_app_or_url.py` | Open applications and websites | "Open notepad", "Launch Chrome", "Visit google.com" |
| **System Info** | `system_info.py` | CPU, memory, and disk usage information | "How much space do i have left?", "CPU usage", "Show memory details" |
| **Timer** | `timer.py` | Countdown timer with audio alerts | "Set a timer for 5 minutes", "Timer 30 seconds", "Countdown 2 minutes" |
| **Courtesy Handler** | `courtesy_handler.py` | Polite responses for thank you, appreciation, etc. | "Thank you", "Thanks for your help", "Appreciate it" |

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">Made with ❤️ by Aditya Karun</div>
