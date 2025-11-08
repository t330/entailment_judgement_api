# Entailment Judgement API

A Django REST API for sentence generation and entailment judgment using Ollama LLM integration.

## Overview

This API provides two main functionalities:
1. **Sentence Generation** - Generate semantically similar or dissimilar sentence pairs
2. **Entailment Judgment** - Evaluate semantic relationships between a sentence pair

## Features

- **LLM Integration** - Powered by Ollama local language models
- **Sentence Generation** - Support for single pair or multiple pairs of sentences
- **Semantic Analysis** - Entailment judgement between a sentence pair
- **REST API** - RESTful endpoints with JSON responses

## Installation & Setup

**Prerequisites** Python3 installed

- Follwo [Set up app with Docker](#set-up-app-with-docker) if you run an app with Docker
- Follow [Set up app without Docker](#set-up-app-without-docker) if you run an app without Docker

### Set up app with Docker

#### 1. Set up a docker environment

- Install Docker
  - Windows: https://docs.docker.com/desktop/setup/install/windows-install/
  - MacOS: https://docs.docker.com/desktop/setup/install/mac-install/

#### 2. Clone the repository
```bash
git clone https://github.com/t330/judgement_entailment.git
cd haga-test
```

#### 3. Build and run with Docker Compose
```bash
docker-compose up --build
docker-compose exec ollama ollama pull mistral
```

#### 4. Access app

- Open http://localhost:8000/

### Set up app without Docker

#### 1. Ollama setup

- Install Ollama
  - Windows: https://ollama.com/download/windows
  - MacOS: https://ollama.com/download/mac
- Install LLM model
  ```bash
  ollama pull mistral
  ```

#### 2. Clone the repository
```bash
git clone https://github.com/t330/judgement_entailment.git
cd haga-test
```

#### 3. Change Ollama location

- In line 32 at [sentence_generator.py](myapiapp\sentence_generator.py), replace host='http://ollama:11434' with http://localhost:11434
- In line 32 at [sentence_generator.py](myapiapp\sentence_generator.py), replace host='http://ollama:11434' with http://localhost:11434

#### 4. Run app
```bash
pip install -r requirements.txt
python manage.py runserver 8000
```
- Open http://localhost:8000/

## Implementations

### 1. Generate Sentences

Generate a signle sentence pair using Ollama LLM

#### Single pair
**Endpoint:** `GET /generate_sentences/`

**Examples**

```bash
curl http://localhost:8000/generate_sentences/
```

**Response Format**

```json
{
  "sentences": [
    {
      "sentence1": "I like cats.",
      "sentence2": "I love cats."
    }
  ]
}
```

#### Multiple pairs

**Endpoint:** `GET /generate_sentences/?batch=true`

**Examples**

```bash
curl http://localhost:8000/generate_sentences/?batch=true
```

**Response Format**

```json
{
  "sentences": [
    {
      "sentence1": "I like cats.",
      "sentence2": "I love cats."
    },
    {
      "sentence1": "The weather is nice.",
      "sentence2": "That person is beautiful."
    },
    {
      "sentence1": "I'm going to go see you tomorrow.",
      "sentence2": "I'm going to eat fish tomorrow."
    }
  ]
}
```

### 2. Judge Entailment

Evaluate entailment relationships between sentence pairs

**Endpoint:** `POST /judge/`

#### Request Body

**Single pair**

Replace <YOUR_CSRF_TOKEN> with your CSRF token as needed

**Windows**
```bash
curl.exe "http://localhost:8000/judge/" --request POST --header "Content-Type: application/json" --header "X-CSRFToken: <YOUR_CSRF_TOKEN>" --data '{\"sentences\": [{\"sentence1\": \"I like cats.\", \"sentence2\": \"I love cats.\"}]}'
```

**MacOS**
```bash
curl -X POST \
  http://localhost:8000/judge/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <YOUR_CSRF_TOKEN>" \
  -d '{
        "sentences": [
          {
            "sentence1": "I like cats.",
            "sentence2": "I love cats."
          }
        ]
      }'
```

**Multiple pairs**

Replace <YOUR_CSRF_TOKEN> with your CSRF token as needed

**Windows**
```bash
curl.exe "http://localhost:8000/judge/" --request POST --header "Content-Type: application/json" --header "X-CSRFToken: <YOUR_CSRF_TOKEN>" --data '{\"sentences\": [{\"sentence1\": \"I like cats.\", \"sentence2\": \"I love cats.\"}, {\"sentence1\": \"The weather is nice.\", \"sentence2\": \"That person is beautiful.\"}, {\"sentence1\": \"I''m going to go see you tomorrow.\", \"sentence2\": \"I''m going to eat fish tomorrow.\"}]}'
```

**MacOS**
```bash
curl -X POST \
  http://localhost:8000/judge/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <YOUR_CSRF_TOKEN>" \
  -d '{
        "sentences": [
          {
            "sentence1": "I like cats.",
            "sentence2": "I love cats."
          },
          {
            "sentence1": "The weather is nice.",
            "sentence2": "That person is beautiful."
          },
          {
            "sentence1": "I''m going to go see you tomorrow.",
            "sentence2": "I''m going to eat fish tomorrow."
          }
        ]
      }'
```

#### Response Format

**Single pair**

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

**Multiple pairs**

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

## Core Components

### Sentence Generator
**File:** `myapiapp/sentence_generator.py`

**Functionality**
- **Single Pair Generation:** Creates one pair of sentences (similar or dissimilar)
- **Bulk Generation:** Generates multiple pairs of sentences at a time
- **LLM Integration:** Uses Ollama to generate contextually appropriate text
- **Semantic Variation:** Produces both semantically similar and dissimilar sentence pairs

**Key Features**
- Prompt engineering for language generation
- Structured JSON output formatting
- Error handling for LLM service failures
- Batch processing optimization

### Entailment Checker
**File:** `myapiapp/entailment_checker.py`

**Functionality**
- **Semantic Analysis:** Evaluates relationships between sentence pairs
- **Entailment Judgement:** Determines if sentences entail each other
- **Scoring:** Provides entailment scores (0.00-1.00)
- **Batch Processing:** Handles multiple sentence pairs simultaneously

**Output Labels**
- `ENTAIL`: Sentences are semantically similar/equivalent (greater than or equal to 0.80 score )
- `NO_ENTAIL`: Sentences are semantically dissimilar (less than 0.80 score)

## Technical Architecture

### Framework & Dependencies
- **Python 3.14** - Python
- **Django 5.2.7** - Web framework
- **Django REST Framework 3.16.1** - API development
- **Ollama** - Local LLM integration
- **Pydantic** - Data validation and serialization

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
├── static/                    # Static files
│   └── js/                    # JavaScript files
└── templates/                 # Template files
    └── index.html             # HTML files
```
