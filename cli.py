import os
import sys
import re
import ipaddress
import mimetypes
from google import genai

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Regex patterns for local IOC extraction
IPV4_REGEX = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
SHA256_REGEX = re.compile(r'\b[a-fA-F0-9]{64}\b')
MD5_REGEX = re.compile(r'\b[a-fA-F0-9]{32}\b')
DOMAIN_REGEX = re.compile(r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b')

def extract_iocs(content: str) -> dict:
    """Extract and categorize indicators of compromise (IOCs) from text."""
    iocs = {
        "public_ips": set(),
        "internal_ips": set(),
        "sha256": set(),
        "md5": set(),
        "domains": set()
    }

    # Extract IPs and classify
    for match in IPV4_REGEX.finditer(content):
        ip_str = match.group(0)
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_private or ip_obj.is_loopback:
                iocs["internal_ips"].add(ip_str)
            elif not ip_obj.is_multicast and not ip_obj.is_reserved:
                iocs["public_ips"].add(ip_str)
        except ValueError:
            continue

    # Extract hashes
    iocs["sha256"] = set(SHA256_REGEX.findall(content))
    iocs["md5"] = set(MD5_REGEX.findall(content))

    # Extract domains (filter common false positives)
    common_false_positives = {"microsoft.com", "google.com", "github.com", "schema.org", "w3.org"}
    for domain in DOMAIN_REGEX.findall(content):
        domain_lower = domain.lower()
        if domain_lower not in common_false_positives and not domain_lower.endswith(".exe"):
            iocs["domains"].add(domain_lower)

    return iocs

def print_ioc_summary(iocs: dict):
    """Print extracted IOCs to console."""
    has_iocs = any(len(v) > 0 for v in iocs.values())
    if not has_iocs:
        return

    print("\n" + "=" * 50)
    print("🔍 [Local Heuristic] Discovered Indicators of Compromise (IOCs):")
    if iocs["public_ips"]:
        print(f"  • External IPv4 ({len(iocs['public_ips'])}): {', '.join(sorted(list(iocs['public_ips'])[:5]))}")
    if iocs["internal_ips"]:
        print(f"  • Internal IPv4 ({len(iocs['internal_ips'])}): {', '.join(sorted(list(iocs['internal_ips'])[:5]))}")
    if iocs["sha256"]:
        print(f"  • SHA-256 Hashes ({len(iocs['sha256'])}): {', '.join(sorted(list(iocs['sha256'])[:3]))}")
    if iocs["md5"]:
        print(f"  • MD5 Hashes ({len(iocs['md5'])}): {', '.join(sorted(list(iocs['md5'])[:3]))}")
    if iocs["domains"]:
        print(f"  • Discovered Domains ({len(iocs['domains'])}): {', '.join(sorted(list(iocs['domains'])[:5]))}")
    print("=" * 50 + "\n")

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set.")
        print("Please set GEMINI_API_KEY in your environment or in a .env file.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model=MODEL_NAME)

    print("=== CLI Threat Analyzer (Log Triage & IOC Extraction) ===")
    print("  - Type an alert description or log snippet to analyze.")
    print("  - To triage a local file or log: /file <path> <optional prompt>")
    print("    Example: /file sample_access.log Extract anomalies and triage risk")
    print("  - Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("Analyst: ").strip()

            if user_input.lower() in ['exit', 'quit']:
                print("\nSession ended.")
                break
            if not user_input:
                continue

            if user_input.startswith("/file"):
                parts = user_input.split(" ", 2)
                if len(parts) < 2 or not parts[1].strip():
                    print("\n[Usage] /file <path> <optional prompt>\n")
                    continue

                file_path = parts[1].strip('"\'')
                prompt = parts[2] if len(parts) > 2 else "Perform a SOC Tier-1 triage on this file. Identify suspected MITRE ATT&CK techniques, high-risk IOCs, and recommended containment steps."

                if not os.path.exists(file_path):
                    print(f"\n[Error] File '{file_path}' not found.\n")
                    continue

                # Read local text for immediate local IOC extraction
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        file_text = f.read(100000) # Read first 100KB for heuristic IOC parsing
                        local_iocs = extract_iocs(file_text)
                        print_ioc_summary(local_iocs)
                except Exception:
                    pass

                print(f"[Uploading {file_path} to Gemini for security reasoning...]")
                mime_type = mimetypes.guess_type(file_path)[0] or "text/plain"
                uploaded_file = client.files.upload(
                    file=file_path,
                    config={"mime_type": mime_type}
                )

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[prompt, uploaded_file]
                )
                print(f"\nThreat Analyzer Report:\n{response.text}\n")

            else:
                # Check for IOCs directly in the user input
                iocs = extract_iocs(user_input)
                print_ioc_summary(iocs)

                response = chat.send_message(user_input)
                print(f"\nThreat Analyzer:\n{response.text}\n")

        except KeyboardInterrupt:
            print("\nSession interrupted.")
            break
        except Exception as e:
            print(f"\nAPI Error: {e}\n")

if __name__ == "__main__":
    main()
