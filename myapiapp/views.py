from rest_framework import viewsets
from .models import Sentence
from .serializers import SentenceSerializer
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST, require_GET
from .sentence_generator import generate_sentences_with_llm
from .entailment_checker import check_entailment
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class SentenceViewSet(viewsets.ModelViewSet):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

    throttle_classes = [AnonRateThrottle, UserRateThrottle]

def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def generate_sentences(request) -> JsonResponse:
    if request.GET.get('batch'):
        generated_sentences = generate_sentences_with_llm(True) # Handle multiple pairs of sentence generation
    else:
        generated_sentences = generate_sentences_with_llm() # Handle a single pair of sentence generation
    return generated_sentences

@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def judge_entailment(request) -> JsonResponse:
    try:
        sentences = json.loads(request.body)
        if not sentences:
            return JsonResponse({'error': 'Invalid input - missing sentence1 or sentence2'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f'Missing required field: {e}'}, status=400)
    # Evaluate the two sentences using entailment_checker.py
    entailment_result = evaluate_entailment(sentences)
    if not entailment_result:
        return JsonResponse({'error': 'Invalid input'}, status=400)
    return entailment_result

def evaluate_entailment(sentences: JsonResponse) -> JsonResponse:
    if not sentences:
        return JsonResponse({'error': 'Invalid input'}, status=400)
    result = check_entailment(sentences)
    return result
