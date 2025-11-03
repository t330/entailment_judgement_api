# Django Japanese Sentence API

A Django REST API for Japanese sentence generation and entailment judgment using Ollama LLM integration.

## Overview

This API provides two main functionalities:
1. **Japanese Sentence Generation** - Generate semantically similar or dissimilar Japanese sentence pairs
2. **Entailment Judgment** - Evaluate semantic relationships between Japanese sentence pairs

## Features

- **LLM Integration** - Powered by Ollama local language models
- **Batch Processing** - Support for single or bulk sentence generation (up to 100 pairs)
- **Semantic Analysis** - Entailment judgement between sentence pairs
- **REST API** - RESTful endpoints with JSON responses powered

## Installation & Setup

### Docker Setup

#### Prerequisites
- **Docker** and **Docker Compose** installed

#### Quick Start with Docker

1. **Clone the repository:**
```bash
git clone https://github.com/t330/judgement_entailment.git
cd haga-test
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Run database migrations (first time only):**
```bash
docker-compose exec web python manage.py migrate
```

4. **Download Ollama LLM model (mistral) (first time only):**
```bash
docker-compose exec ollama ollama pull mistral
```

The application will be available at http://localhost:8000

5. **Test an application:**

1. Open http://localhost:8000
1. Press F1 button to review F1 implementations
  - It will take about 40 seconds to show the result of entailment judgement
1. Press F2 button to review F2 implementations
  - If the app judges 5 pairs of sentences, it will take about 2 minutes to show the result of entailment judgement
  - **NOTE:** : Currently the number of sentences that can be generated is set to 5. If you obtanin test 100 pairs of sentences, please follow the steps:
    1. Change "5" in line 16 and 20 to "100" in myapiapp/sentence_generator.py
    1. ```bash
        docker-compose down
        docker-compose up
        ```
    1. Close the current brower tab showing the app and open it again
    1. Check if F2 button generates 100 pairs of sentences and results of judgement entailment

## F1 Implementations

### 1. Generate Sentences
**Endpoint:** `GET /generate_sentences/`

**Description:** Generate Japanese sentence pairs using Ollama LLM

**Examples:**

```bash
# Generate single sentence pair
curl http://localhost:8000/generate_sentences/
```

**Response Format:**

```json
{
  "sentences": [
    {
      "sentence1": "私は猫が大好きだ。",
      "sentence2": "猫が好きです。"
    }
  ]
}
```

### 2. Judge Entailment
**Endpoint:** `POST /judge/`

**Description:** Evaluate entailment relationships between Japanese sentence pairs

**Request Body:**
```json
{
  "sentences": [
    {
      "sentence1": "私は猫が大好きだ。",
      "sentence2": "猫が好きです。"
    }
  ]
}
```

**Response Format:**
```json
{
  "results": [
    {
      "label": "ENTAIL",
      "score": "0.90"
    }
  ]
}
```

## F2 Implementations

### 1. Generate Sentences
**Endpoint:** `GET /generate_sentences/`

**Parameters:**
- `batch` (optional): Generate multiple pairs (expected to be up to 100)

**Examples:**

# Generate multiple sentence pairs (batch mode)
```bash
curl http://localhost:8000/generate_sentences/?batch=true
```

**Response Format:**

```json
{
  "sentences": [
    {
      "sentence1": "私は猫が大好きだ。",
      "sentence2": "猫が好きです。"
    },
    {
      "sentence1": "天気が良いですね。",
      "sentence2": "あの人は美しいです。"
    },
    {
      "sentence1": "明日、会いに行くつもりです。",
      "sentence2": "明日、魚を食べるつもりです。"
    },
  ]
}
```

### 2. Judge Entailment
**Endpoint:** `POST /judge/`

**Description:** Evaluate entailment relationships between Japanese sentence pairs

**Headers:**
- `Content-Type: application/json`
- `X-CSRFToken: <csrf_token>` (required for CSRF protection)

**Request Body:**
```json
{
  "sentences": [
    {
      "sentence1": "私は猫が大好きだ。",
      "sentence2": "猫が好きです。"
    },
    {
      "sentence1": "天気が良いですね。",
      "sentence2": "あの人は美しいです。"
    },
    {
      "sentence1": "明日、会いに行くつもりです。",
      "sentence2": "明日、魚を食べるつもりです。"
    }
  ]
}
```

**Response Format:**
```json
{
  "results": [
    {
      "label": "ENTAIL",
      "score": "0.90"
    },
    {
      "label": "NO_ENTAIL",
      "score": "0.30"
    },
    {
      "label": "NO_ENTAIL",
      "score": "0.40"
    }
  ]
}
```

## F3 Implementations

It's been implemented but not working

## Core Components

### Sentence Generator
**File:** `myapiapp/sentence_generator.py`

**Functionality:**
- **Single Pair Generation:** Creates one pair of Japanese sentences (similar or dissimilar)
- **Bulk Generation:** Generates up to 100 pairs of Japanese sentences
- **LLM Integration:** Uses Ollama to generate contextually appropriate Japanese text
- **Semantic Variation:** Produces both semantically similar and dissimilar sentence pairs

**Key Features:**
- Prompt engineering for Japanese language generation
- Structured JSON output formatting
- Error handling for LLM service failures
- Batch processing optimization

### Entailment Checker
**File:** `myapiapp/entailment_checker.py`

**Functionality:**
- **Semantic Analysis:** Evaluates relationships between Japanese sentence pairs
- **Entailment Judgement:** Determines if sentences entail each other
- **Scoring:** Provides entailment scores (0.00-1.00)
- **Batch Processing:** Handles multiple sentence pairs simultaneously

**Output Labels:**
- `ENTAIL`: Sentences are semantically similar/equivalent (greater than or equal to 0.80 score )
- `NO_ENTAIL`: Sentences are semantically dissimilar (less than 0.80 score)

## Technical Architecture

### Framework & Dependencies
- **Python 3.14** - Python
- **Django 5.2.7** - Web framework
- **Django REST Framework 3.16.1** - API development
- **Ollama** - Local LLM integration
- **Pydantic** - Data validation and serialization

## 3 ideas for future accuracy improvements

1. Accuracy of sentence generation
    Sometimes Ollama generates a typo-like sentence
1. Consumption time of generating sentences
    Ollama generates 5 pairs of sentences in about 10 seconds
1. Accuracy of entailement judgement
    Sometimes Ollama produces a different form of score like ".95" instead of 0.95
1. Accuracy of entailement judgement

## Development

### Project Structure
```
haga-test/
├── manage.py
├── haga/                      # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── myapiapp/                  # Main application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── sentence_generator.py  # LLM sentence generation
│   ├── entailment_checker.py  # Entailment judgement
│   ├── serializers.py
│   └── tests.py
└── static/                    # Static files
    └── js/                    # JavaScript files
└── templates/                 # Template files
│   ├── index.html             # HTML files
```
