# CLI-Threat-Analyzer (Log & Security Triage Utility)

## Overview
A Python command-line utility for rapid security triage directly in your terminal. Designed for SOC analysts, sysadmins, and security engineers to parse system logs, extract IOCs, inspect suspicious files, and analyze threat reports without leaving PowerShell or the command line.

## Features
* **Log & Report Analysis:** Feed server logs (Apache/Nginx, auth logs, Windows events) to identify security threats, anomalous IPs, or error spikes.
* **Multi-Modal Inspection:** Inspect local log dumps, intelligence reports, and security screenshots directly through the terminal.
* **Terminal Integration:** Interactive terminal session built in Python for fast troubleshooting.

## Tech Stack
* **Language:** Python 3.x
* **Core Engine:** Threat Intelligence & Log Parsing Engine (`google-genai` / REST API)
* **Environment:** Windows PowerShell, Linux Bash, or macOS Terminal

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mahialjaber/CLI-Threat-Analyzer.git
   cd CLI-Threat-Analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Key:**
   Copy `.env.example` to `.env` in the root directory (`cp .env.example .env`) and set your key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   Or export it in your environment:
   - **Linux / macOS:** `export GEMINI_API_KEY="your_api_key"`
   - **PowerShell:** `$env:GEMINI_API_KEY="your_api_key"`

4. **Run the application:**
   ```bash
   python cli.py
   ```

## Usage
* **Chat:** Type your message directly into the prompt.
* **File Analysis:** Use `/file <path> <optional prompt>`
  * *Example:* `/file sample_access.log Analyze these server logs for security breaches.`
  * *Example:* `/file image.png Inspect this screenshot for errors.`
* **Exit:** Type `exit` or `quit`.

## License
MIT

## Troubleshooting
- **Missing API Key Error:** Ensure .env exists in the project root (copied from .env.example) and contains a valid GEMINI_API_KEY.
- **Python Version:** Python 3.10 or newer is recommended.
