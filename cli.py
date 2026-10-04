import os
import sys
import mimetypes
from google import genai
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set.")
        print("Please set GEMINI_API_KEY in your environment or in a .env file.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model=MODEL_NAME)

    print("=== TerminalGemini (Chat + File Upload) ===")
    print("  - Type your message to chat normally.")
    print("  - To upload an image or log file: /file <path> <optional prompt>")
    print("    Example: /file sample_access.log Analyze these server logs")
    print("    Example: /file image.jpg Describe this image")
    print("  - Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()

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
                prompt = parts[2] if len(parts) > 2 else "Analyze this file in detail."

                if not os.path.exists(file_path):
                    print(f"\n[Error] File '{file_path}' not found.\n")
                    continue

                print(f"\n[Uploading {file_path} to Gemini...]")
                mime_type = mimetypes.guess_type(file_path)[0] or "text/plain"
                uploaded_file = client.files.upload(
                    file=file_path,
                    config={"mime_type": mime_type}
                )

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=[prompt, uploaded_file]
                )
                print(f"\nGemini: {response.text}\n")

            else:
                response = chat.send_message(user_input)
                print(f"\nGemini: {response.text}\n")

        except KeyboardInterrupt:
            print("\nSession interrupted.")
            break
        except Exception as e:
            print(f"\nAPI Error: {e}\n")

if __name__ == "__main__":
    main()