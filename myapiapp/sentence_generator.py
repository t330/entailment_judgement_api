from django.http import JsonResponse
import ollama
import json
from pydantic import BaseModel

class SentenceList(BaseModel):
    sentences: list[dict[str, str]]

def generate_sentences_with_llm(isBulkySentences: bool = False) -> JsonResponse:
    """Generates a sentence by prompting a local LLM via the Ollama client."""
    
    # The prompt instructs the AI model to generate the sentence

    if isBulkySentences: # Generate up to 100 pairs of sentence generation
        prompt = """
            Generate 5 pairs of Japanese sentences whose two sentences are semantically similar or semantically dissimilar randomly.
            Here is the examples of an expected JSON array output:
            [{"sentence1": "私は猫が大好きだ。", "sentence2": "猫が好きです。"}, {"sentence1": "天気が良いですね。", "sentence2": "あの人は美しいです。"}, ...]
            In this case, the first pair of sentences is semantically similar, while the second pair is not.
            You must return the JSON array including 5 objects.
            """
    else: # Generate a single pair of sentences
        prompt = """
            Generate a single pair of Japanese sentences whose two sentences are semantically similar or semantically dissimilar randomly.
            Here are the two examples of an expected JSON array output:
            Example 1: [{"sentence1": "私は猫が大好きだ。", "sentence2": "猫が好きです。"}]
            Example 2: [{"sentence1": "天気が良いですね。", "sentence2": "あの人は美しいです。"}]
            In this case, the first pair of sentences of Example 1 is semantically similar, while the second pair of sentences of Example 2 is not.
            You must return the JSON array including the single object.
            """
    try:
        client = ollama.Client(host='http://ollama:11434') # If you run the app in local machine instead of Docker, change the host to 'http://localhost:11434'
        response = client.chat(
            model='mistral',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
            format=SentenceList.model_json_schema(),
        )
        print('Sentence generator\'s response:', response['message']['content'].strip())
        content = response['message']['content'].strip()
        parsed_content = json.loads(content)
        return JsonResponse(parsed_content)
    
    except Exception as e:
        return JsonResponse({'error': f"Error connecting to Ollama: {e}. Make sure Ollama is running locally."})
