import os
import sys
from google import genai

def main():
    api_key = os.getenv(" paste your gemini api key here")
    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set.")
        print("Run: export GEMINI_API_KEY='your_key'")
        sys.exit(1)

    client = genai.Client(api_key="paste your gemini api key here")
    chat = client.chats.create(model="gemini-3.5-flash")

    print("=== TerminalGemini (Chat + File Upload) ===")
    print("• Type your message to chat normally.")
    print("• To upload an image or log file: /file <path> <optional prompt>")
    print("  Example: /file /var/log/secure Analyze these SSH logs")
    print("  Example: /file /home/Downloads/image.jpg Describe this image")
    print("• Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['exit', 'quit']:
                print("\nSession ended.")
                break
            if not user_input:
                continue

            # Command to handle files/images
            if user_input.startswith("/file "):
                parts = user_input.split(" ", 2)
                file_path = parts[1]
                prompt = parts[2] if len(parts) > 2 else "Analyze this file in detail."

                if not os.path.exists(file_path):
                    print(f"\n[Error] File '{file_path}' not found.\n")
                    continue

                print(f"\n[Uploading {file_path} to Gemini...]")
                uploaded_file = client.files.upload(file=file_path,config={"mime_type": "text/plain"})

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[prompt, uploaded_file]
                )
                print(f"\nGemini: {response.text}\n")

            else:
                # Normal text chat
                response = chat.send_message(user_input)
                print(f"\nGemini: {response.text}\n")

        except KeyboardInterrupt:
            print("\nSession interrupted.")
            break
        except Exception as e:
            print(f"\nAPI Error: {e}\n")

if __name__ == "__main__":
    main()