from ollama import get_tags, pull_model

from settings import MODEL_NAME

def ensure_model_exists():
    data = get_tags()
    print(data)
    if f"{MODEL_NAME}:latest" not in [tag['name'] for tag in data['models']]:
        print(f"Model {MODEL_NAME} not found locally. Pulling from Ollama server...")
        print(pull_model(MODEL_NAME))
        print(f"Model {MODEL_NAME} has been pulled successfully.")
    print(f"Model {MODEL_NAME} is available locally.")