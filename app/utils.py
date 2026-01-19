def format_message(prompt: str, role: str) -> str:
    return {"role": role, "content": prompt}