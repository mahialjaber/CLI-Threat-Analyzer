# CLI-Threat-Analyzer (Log & Security Copilot)

## Overview
A command-line tool that integrates Google's Gemini AI directly into your terminal. Designed for developers, sysadmins, and security analysts to analyze system logs, security reports, code files, and images without leaving PowerShell or the command line.

## Features
* **Log & Report Analysis:** Feed server logs (Apache/Nginx, auth logs, Windows events) to the AI to identify security threats, errors, or suspicious IP addresses.
* **Multi-Modal Capabilities:** Inspect local files and images directly through the terminal.
* **Terminal Integration:** Interactive terminal session built in Python for fast troubleshooting.

## Tech Stack
* **Language:** Python 3.x
* **AI Engine:** Google Gemini API (`google-genai`)
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
   Create a `.env` file in the root directory:
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
