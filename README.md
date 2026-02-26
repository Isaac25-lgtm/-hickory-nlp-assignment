# NLP-Based Machine Learning Pipeline: The Hickory Kampala Restaurant

> **Course:** Data Mining, Modelling and Analytics — Assignment 3 (Individual)
> **Student:** Omoding Isaac (B31331)
> **Program:** MSc Data Science and Analytics
> **University:** Uganda Christian University
> **Semester:** Easter 2026
> **Submission Date:** 26 February 2026

---

## Table of Contents

1. [Objective](#objective)
2. [Live Deployment](#live-deployment)
3. [Business Identification](#business-identification)
4. [Pipeline Overview](#pipeline-overview)
5. [Project Structure](#project-structure)
6. [Methodology](#methodology)
   - [Data Mining](#1-data-mining-web-scraping)
   - [NLP Preprocessing](#2-nlp-preprocessing)
   - [Exploratory Data Analysis](#3-exploratory-data-analysis)
   - [Feature Engineering](#4-feature-engineering)
   - [Model Development](#5-model-development)
   - [Deployment](#6-deployment)
7. [Results Summary](#results-summary)
8. [How to Run Locally](#how-to-run-locally)
9. [Dependencies](#dependencies)
10. [References](#references)

---

## Objective

This project implements a complete data mining and analytics pipeline — from acquisition to deployment — using real-world restaurant data sourced from a Ugandan business website. The pipeline covers web scraping, natural language processing (NLP) with lemmatisation, exploratory data analysis, TF-IDF feature engineering, supervised classification modelling, and interactive model deployment via Streamlit.

---

## Live Deployment

**Streamlit Application:** [https://omoding-hickory-nlp.streamlit.app](https://omoding-hickory-nlp.streamlit.app)

The deployed application accepts any restaurant-related text input and classifies it into the appropriate content category using a trained machine learning model.

**Supported categories:** `food` · `drinks` · `wines` · `cake` · `reviews` · `services` · `about` · `home`

---

## Business Identification

| Attribute | Detail |
|-----------|--------|
| **Restaurant** | The Hickory Kampala |
| **Location** | Plot 11 Ngabo Road, Kololo, Kampala, Uganda |
| **Website** | [https://thehickorykampala.com](https://thehickorykampala.com) |
| **Justification** | The Hickory Kampala is an upscale restaurant with a rich and well-structured online presence, offering diverse textual content across menus, service descriptions, and customer reviews — making it highly suitable for NLP analysis. |

**Supplementary sources:** TripAdvisor reviews and the Kampala Tourism Portal were used to enrich the dataset with additional customer feedback and descriptive content.

---

## Pipeline Overview

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  1. Scraping  │───▶│ 2. NLP Pre-  │───▶│   3. EDA &   │
│ (BeautifulSoup)│   │  processing  │    │ Visualisation│
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
┌──────────────┐    ┌──────────────┐    ┌──────┴───────┐
│ 6. Streamlit │◀───│  5. Model    │◀───│ 4. Feature   │
│  Deployment  │    │  Training    │    │ Engineering  │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## Project Structure

| File | Description |
|------|-------------|
| `Omoding_NLP_Assignment.ipynb` | Complete Jupyter notebook covering all 7 assignment tasks |
| `scraper.py` | Web scraping script using BeautifulSoup |
| `Omoding.csv` | Raw scraped dataset (712 records, 10 content categories) |
| `Omoding.pkl` | Cleaned and preprocessed dataset (pickle format) |
| `best_model.joblib` | Best performing model — Logistic Regression (91.5% accuracy) |
| `logistic_regression.joblib` | Trained Logistic Regression classifier |
| `linear_svc.joblib` | Trained Linear SVC classifier |
| `random_forest.joblib` | Trained Random Forest classifier |
| `tfidf_vectorizer.joblib` | Fitted TF-IDF vectoriser |
| `app.py` | Streamlit deployment application |
| `requirements.txt` | Python dependencies |
| `confusion_matrix.png` | Model evaluation — confusion matrix visualisation |
| `eda_plots.png` | Exploratory data analysis visualisations |
| `wordcloud.png` | Word cloud of dominant terms |

---

## Methodology

### 1. Data Mining (Web Scraping)

Text data was collected from The Hickory Kampala's website using **BeautifulSoup** (`scraper.py`). The scraping process targeted restaurant descriptions, menu items (food, drinks, wines, cakes), service offerings, customer reviews, and general "about" information. A total of **712 unique records** were extracted and stored in `Omoding.csv` with each record assigned a content category label.

### 2. NLP Preprocessing

The raw text underwent the following preprocessing pipeline:

- **Text normalisation** — lowercasing, removal of special characters and HTML artefacts
- **Tokenisation** — splitting text into individual word tokens
- **Stopword removal** — filtering out common English stopwords using NLTK
- **Lemmatisation** — reducing words to their base dictionary form using NLTK's `WordNetLemmatizer`

The cleaned dataset was saved as `Omoding.pkl`.

### 3. Exploratory Data Analysis

EDA was conducted to understand the textual characteristics of the dataset, including:

- Word frequency distributions across content categories
- Text length analysis (character and token counts)
- Identification of dominant themes and terms per category
- Word cloud generation for visual theme exploration

Business-relevant interpretations were derived from the patterns observed, highlighting the restaurant's content distribution and linguistic characteristics.

### 4. Feature Engineering

Text was transformed into numerical representations using **TF-IDF (Term Frequency–Inverse Document Frequency)** vectorisation with the following configuration:

- **Max features:** 500
- **N-gram range:** Unigrams + Bigrams (1, 2)
- **Dimensionality reduction:** Truncated SVD reducing to 50 components

This approach balances feature richness with computational efficiency while capturing both individual terms and meaningful phrase-level patterns.

### 5. Model Development

Three supervised classifiers were trained and evaluated on the content classification task:

| Model | Accuracy | Notes |
|-------|----------|-------|
| **Logistic Regression** | **91.5%** | Best performer — selected for deployment |
| Linear SVC | 91.5% | Comparable performance, linear decision boundary |
| Random Forest | 90.8% | Ensemble approach, slightly lower accuracy |

All models were saved as `.joblib` files. Evaluation included accuracy scores, classification reports, and confusion matrix analysis (see `confusion_matrix.png`).

### 6. Deployment

The best-performing model (Logistic Regression) was deployed as an interactive web application using **Streamlit**. The application:

- Accepts free-text user input describing any restaurant-related content
- Applies the same preprocessing and TF-IDF transformation pipeline
- Returns a predicted content category with model confidence

---

## Results Summary

- **Dataset:** 712 records across 10 content categories
- **Best model:** Logistic Regression with **91.5% classification accuracy**
- **Feature space:** 500 TF-IDF features reduced to 50 SVD components
- **Deployment:** Fully functional Streamlit app accessible at [omoding-hickory-nlp.streamlit.app](https://omoding-hickory-nlp.streamlit.app)

---

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/Isaac25-lgtm/-hickory-nlp-assignment.git
cd -hickory-nlp-assignment

# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit app
streamlit run app.py
```

To explore the full notebook, open `Omoding_NLP_Assignment.ipynb` in Jupyter Notebook or JupyterLab.

---

## Dependencies

Key libraries used in this project:

- `beautifulsoup4` — Web scraping
- `nltk` — NLP preprocessing and lemmatisation
- `scikit-learn` — TF-IDF vectorisation, model training, and evaluation
- `pandas` / `numpy` — Data manipulation
- `matplotlib` / `seaborn` / `wordcloud` — Visualisation
- `streamlit` — Model deployment
- `joblib` — Model serialisation

See `requirements.txt` for the complete list.

---

## References

- The Hickory Kampala — [https://thehickorykampala.com](https://thehickorykampala.com)
- NLTK Documentation — [https://www.nltk.org](https://www.nltk.org)
- Scikit-learn Documentation — [https://scikit-learn.org](https://scikit-learn.org)
- Streamlit Documentation — [https://docs.streamlit.io](https://docs.streamlit.io)

---

<p align="center">
  <em>Submitted in partial fulfilment of the requirements for MSc Data Science and Analytics</em><br>
  <em>Uganda Christian University — Easter Semester 2026</em>
</p>
