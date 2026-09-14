import json
import re
from pathlib import Path

# Automatically locate project root directory (multi_source_rag/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def clean_pii(text: str) -> str:
    """Strips personal emails and phone numbers from raw text."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_HIDDEN]', text)
    text = re.sub(r'\+?\d{10,12}', '[PHONE_HIDDEN]', text)
    return text


def extract_qa_threads(json_file_path: Path):
    if not json_file_path.exists():
        raise FileNotFoundError(f"File not found: {json_file_path}")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    messages = data.get("messages", [])
    message_dict = {msg["id"]: msg for msg in messages}
    processed_threads = []

    for msg in messages:
        reply_id = msg.get("reply_to_message_id")
        if reply_id and reply_id in message_dict:
            parent_msg = message_dict[reply_id]

            cleaned_question = clean_pii(parent_msg.get("text", ""))
            cleaned_answer = clean_pii(msg.get("text", ""))

            context_text = f"Question: {cleaned_question}\nAnswer: {cleaned_answer}"

            processed_threads.append({
                "id": str(msg["id"]),
                "text": context_text,
                "metadata": {
                    "question_id": parent_msg["id"],
                    "answer_id": msg["id"],
                    "date": msg.get("date", ""),
                    "platform": "Telegram"
                }
            })

    return processed_threads


if __name__ == "__main__":
    sample_data_path = PROJECT_ROOT / "data" / "raw" / "sample_telegram_data.json"

    threads = extract_qa_threads(sample_data_path)
    print(f"Extracted {len(threads)} clean thread pairs.\n")
    for t in threads:
        print(t["text"])
        print("-" * 40)