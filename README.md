# CLI-Threat-Analyzer

A Python command-line utility for rapid security log triage and threat analysis. Combines local heuristic IOC extraction (IPv4 classification, SHA-256/MD5 hashes, and domains) with Google Gemini API reasoning to analyze log dumps and alert contexts directly from the terminal.

---

## Features

* **Heuristic IOC Extraction:** Automatically parses input logs and file uploads using regular expressions to extract and classify public vs. internal IPv4 addresses, cryptographic hashes, and external domains before API processing.
* **Log & File Triage (`/file`):** Ingests system logs, event dumps, or incident screenshots for security reasoning, MITRE ATT&CK technique mapping, and containment suggestions.
* **Interactive Terminal Workflow:** Lightweight CLI loop built for rapid investigations without requiring a heavy browser interface.

---

## Tech Stack

* **Language:** Python 3.10+
* **LLM Engine:** Google Gemini API (`google-genai` SDK)
* **Regex Engine:** Built-in Python `re` & `ipaddress` modules

---

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

3. **Configure API Key:**
   Copy `.env.example` to `.env` and set your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

4. **Launch the CLI:**
   ```bash
   python cli.py
   ```

---

## Usage Examples

* **Ad-hoc Log Triage:** Paste raw log lines directly into the terminal prompt to extract IOCs and ask questions:
  ```text
  Analyst: Failed password for invalid user admin from 192.168.1.50 port 54321 ssh2, followed by connection from 45.33.32.156
  ```
* **Local File Inspection:** Use `/file <path> <optional prompt>`:
  ```text
  Analyst: /file /var/log/auth.log Triage high-severity authentication failures and summarize attacker IPs
  ```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
