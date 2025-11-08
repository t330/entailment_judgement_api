import json
from django.http import JsonResponse
import ollama
from pydantic import BaseModel

class ResultList(BaseModel):
    results: list[dict[str, str]]

def check_entailment(sentences: JsonResponse) -> JsonResponse:
    """Judges how much two sentences have the same meaning."""
    sentenceArray = sentences.get('sentences', [])

    # The prompt instructs the AI model to generate the sentence

    # Judging entailment between sentences
    prompt = """
    Produce the results of entailment judgment between a pairs of sentences.
    Here is the example of how you evaluate a pair of sentences.
    If you are given the following JSON array as input:
    [{"sentence1": "I like cats.", "sentence2": "I love cats."}, {"sentence1": "The weather is nice.", "sentence2": "That person is beautiful."}, {"sentence1": "I'm going to go see you tomorrow.", "sentence2": "I'm going to eat fish tomorrow."}]
    You need to evaluate how much semantically similar a pair of sentences of each object in this array is and return the result of each object as the following:
    [{"label": "ENTAIL", "score": 0.90}, {"label": "NO_ENTAIL", "score": 0.30}, {"label": "NO_ENTAIL", "score": 0.40}]
    label has ENTAIL whose score is greater than or equal to 0.80, or NO_ENTAIL whose score is less than 0.80.
    score is a decimal fraction between 0.00 and 1.00, where 0.00 is completely not semantically similar. and 1.00 is completely semantically similar.
    score must be given with decimal franctions from 0.00 to 1.00 and do not include any other characters.
    These results indicate that the first pair of sentences is semantically similar with ENTAIL and a score of 0.90, the second pair is not semantically similar with NO_ENTAIL and a score of 0.30 and the third pair is not semantically similar with NO_ENTAIL and a score of 0.40.
    These scores are just an example, so you need to evaluate the actual semantic similarity of each pair of sentences.
    The number of objects in the input JSON array can be from 1 to 100, so please evaluate all pairs of sentences in the input JSON array and return the results as a JSON array including the same number of objects.
    Now here is the input JSON array:
    """ + json.dumps(sentenceArray, ensure_ascii=False)
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
            format=ResultList.model_json_schema(),
        )
        print('Entailment checker\'s response:', response['message']['content'].strip())
        content = response['message']['content'].strip()
        parsed_content = json.loads(content)
        return JsonResponse(parsed_content)
    
    except Exception as e:
        return JsonResponse({'error': f"Error connecting to Ollama: {e}. Make sure Ollama is running locally."})
