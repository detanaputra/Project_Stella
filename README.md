# Project Stella

**Semantic Topic ExpLoration and LeArning** — a desktop application that makes topic modelling accessible to social scientists who don't write code.

## What is this?

Project Stella is a free, offline desktop application for analysing collections of text documents — interviews, survey responses, news articles, social media posts — and discovering the topics they discuss. It wraps the BERTopic algorithm in a simple, guided interface, so researchers can go from raw data to interpretable topics without writing a line of Python.

## Why this app?

Topic modelling is a powerful method, but the tools for it assume programming skills. Project Stella removes that barrier:

- **No code required** — a 4-step wizard guides you from file to results.
- **Private by design** — everything runs locally on your machine. Your data never leaves it.
- **Offline** — no internet connection needed.
- **Interpretable output** — see the top terms for each topic, not raw embeddings.
- **Reproducible** — every model's configuration is recorded, so your method is citable.

## Features

- Train a BERTopic model on your own CSV or TXT data
- Guided 4-step setup wizard (file → hyperparameters → preview → summary; "Default Settings" skips the hyperparameters step)
- Configurable hyperparameters: language, embedding model, n-gram range, minimum topic size, and more
- Topic quality metrics: NPMI, C_V, and UMass coherence plus Topic Diversity
- Result tables: top terms per topic and per-document topic assignments
- Five visualizations as in-app tabs (topics, heatmap, barchart, hierarchy, term rank), each with an "Open interactive" button for the full Plotly chart in your browser
- Export results to CSV, JSON, and a methodology report
- Save and reload your work as `.stella` project files

## Who is it for?

Social scientists and researchers — sociologists, political scientists, media and communication scholars — who work with text data and want a reproducible, citable topic-modelling workflow without learning to program.

## Getting started

### Requirements

- Python 3.10+ (3.11 recommended)

### Install

```bash
git clone https://github.com/detanaputra/Project_Stella.git
cd Project_Stella
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

## License

Apache License 2.0. See [LICENSE](LICENSE).
