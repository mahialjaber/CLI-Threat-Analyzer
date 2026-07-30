# CLI-Threat-Analyzer (Log & Security Copilot)

## Overview
A powerful command-line interface (CLI) tool that brings Google's Gemini AI directly into your terminal. Designed for developers, sysadmins, and security professionals to instantly analyze system logs, security reports, code files, and images without ever leaving PowerShell or the command line.

## Features
*   **Log & Report Analysis:** Quickly feed server logs (e.g., Apache/Nginx, SSH logs) to the AI to identify security threats, errors, or anomalous IPs.
*   **Multi-Modal Capabilities:** Upload local files and images directly through the terminal for AI inspection.
*   **Seamless Terminal Integration:** Interactive chat session built purely in Python, optimized for rapid troubleshooting.

## Tech Stack
*   **Language:** Python 3.x
*   **AI Engine:** Google Gemini API
*   **Environment:** Windows PowerShell, Linux Bash, or macOS Terminal

## Installation & Setup ^-^

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mahialjaber/CLI-Threat-Analyzer
    cd gemini-cli-analyzer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables:**
    Create a `.env` file in the root directory and add your API key. 
    **Important:** Do not use Python syntax inside the `.env` file. It should look exactly like this:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

4.  **Run the application:**
    ```bash
    python chat1.py
    ```

## 💻 Usage
*   **Standard Chat:** Type your questions directly.
*   **File Analysis:** Use `/file <path> <prompt>`
    *   *Example:* `/file sample_access.log Analyze these server logs for security breaches.`
