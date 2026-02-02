## Welcome

AI use has grown rapidly over the last few years. Far from being a sci-fi replacement for humans, where it really shines is in automating the boring, repetitive, or slow parts of our day. Most of the value isn’t in building huge, complicated systems, but in streamlining simple ones.

This project is about exploring practical, lightweight uses of AI. What can we build in a few hours that’s actually useful? By the end of the day, we should have a better sense of how these tools behave, where they’re strong, where they fall over, and how to use them with minimal effort.

Keeping it deliberately simple with one core task and an optional extra:

* A HR chatbot that can answer questions using policy text.


## Tooling

#### Gemini API
A large language model that handles natural-language tasks. In our case this is answering HR questions and generating recommendations.

#### ChromaDB
A lightweight vector database that stores text as embeddings. ChromaDB finds the most relevant chunks of text based on our questions which we can then include in our prompts. This allows us to avoid uploading documents to Gemini directly.

#### Embeddings
Instead of storing raw text, we convert each chunk into a vector using Google’s embedding model. Distance between vectors tells us how semantically similar two pieces of text are. This is what allows Gemini to answer from the correct policy section.

#### Python
The suggested language to link the component parts together is python. It's popular, simple, and robust.

#### Retrieval-Augmented Generation (RAG)
The 'proper' name for the simple pattern we’re using:

* Retrieve relevant text from ChromaDB.

* Feed it into the Gemini model to answer the question.

## API keys
use your na

## Getting started

#### 1 - Clone the starter pack

```bash
# https
git clone https://github.com/femy4ever/AL_hr_assistant.git

# ssh
git clone https://github.com/femy4ever/AL_hr_assistant.git
```

#### 2 - Create an environment.

***Linux (incl. WSL)***
```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set Gemini API key
export GEMINI_API_KEY=<API KEY>

# 4. Run the demo
cd hr_assistant
python demo.py
```

***Windows (powershell)***
```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2 Install dependencies
pip install -r requirements.txt

# 3. Set Gemini API key
env$GEMINI_API_KEY="<API_KEY>"

# 4. Run the demo
cd hr_assistant
python demo.py
```

## FAQs & gotchas
#### Common issues:

* `Collection already exists` - delete ~/.chromadb/ or `python cleanup_chroma.py`

* Empty responses - increase `n_results` (try 3–5)

* Hallucinations - tighten prompt wording

* API errors - check api key is present in environment

* Slow retrieval - reduce `chunk_size`
