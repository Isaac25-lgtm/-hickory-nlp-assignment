# NLP-Based Machine Learning Pipeline: The Hickory Kampala Restaurant

**Course:** Data Mining, Modelling and Analytics — Assignment 3 (Individual)
**Student:** Omoding Isaac (B31331)
**Program:** MSc Data Science
**University:** Uganda Christian University
**Semester:** EASTER 2026

---

## Objective

This project implements a complete data mining and analytics pipeline by scraping, processing, analysing, modelling, and deploying an NLP-based machine learning solution using real-world restaurant data from **The Hickory Kampala** (https://thehickorykampala.com).

## Live Deployment

**Streamlit App:** https://omoding-hickory-nlp.streamlit.app

The deployed application accepts any restaurant-related text input and classifies it into the appropriate content category (food, drinks, wines, cake, reviews, services, or about) using a trained machine learning model.

## Project Structure

| File | Description |
|------|-------------|
| `Omoding_NLP_Assignment.ipynb` | Complete Jupyter notebook covering all 7 assignment tasks |
| `scraper.py` | Web scraping script using BeautifulSoup |
| `Omoding.csv` | Scraped dataset (712 records) |
| `Omoding.pkl` | Cleaned and preprocessed dataset (pickle format) |
| `best_model.joblib` | Best performing trained model (Logistic Regression, 91.5% accuracy) |
| `tfidf_vectorizer.joblib` | Fitted TF-IDF vectorizer |
| `app.py` | Streamlit deployment application |
| `requirements.txt` | Python dependencies |

## Pipeline Summary

1. **Business Identification** — Selected The Hickory Kampala, an upscale restaurant in Kololo, Kampala with rich online textual data across menus, reviews, and services.

2. **Data Mining** — Scraped 712 unique records from the restaurant's website using BeautifulSoup, supplemented with verified data from TripAdvisor and the Kampala Tourism Portal.

3. **NLP Preprocessing** — Applied text normalisation, tokenisation, stopword removal, and lemmatisation (using NLTK WordNetLemmatizer). Saved as `Omoding.pkl`.

4. **Exploratory Data Analysis** — Analysed word frequencies, text length distributions, and dominant themes per category. Generated word clouds and visualisations.

5. **Feature Engineering** — Transformed text using TF-IDF vectorisation (500 features, unigrams + bigrams) with dimensionality reduction via Truncated SVD (50 components).

6. **Model Development** — Trained and evaluated three classifiers:
   - Logistic Regression — **91.5% accuracy** (best)
   - Linear SVC — 91.5% accuracy
   - Random Forest — 90.8% accuracy

7. **Deployment** — Deployed via Streamlit at https://omoding-hickory-nlp.streamlit.app

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data Source

**The Hickory Kampala** — https://thehickorykampala.com
Plot 11 Ngabo Road, Kololo, Kampala, Uganda
