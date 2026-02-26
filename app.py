"""
Streamlit Deployment App - The Hickory Kampala NLP Classifier
Author: Omoding Isaac (B31331)
Course: MSc Data Science - Data Mining, Modelling and Analytics
University: Uganda Christian University
Semester: EASTER 2026
"""

import streamlit as st
import joblib
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Load model and vectorizer
@st.cache_resource
def load_model():
    model = joblib.load('best_model.joblib')
    tfidf = joblib.load('tfidf_vectorizer.joblib')
    return model, tfidf

model, tfidf = load_model()

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    """Clean, tokenize, remove stopwords, and lemmatize input text."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    tokens = [lemmatizer.lemmatize(t, pos='v') for t in tokens]
    tokens = [lemmatizer.lemmatize(t, pos='n') for t in tokens]
    return ' '.join(tokens)

# Category descriptions
CATEGORY_INFO = {
    'food': 'Food Menu - This text describes a food or meal item',
    'drinks': 'Drinks Menu - This text describes a beverage or cocktail',
    'wines': 'Wine List - This text describes a wine selection',
    'cake': 'Cake Menu - This text describes a cake or bakery item',
    'reviews': 'Customer Review - This text sounds like a customer review',
    'services': 'Services - This text describes a restaurant service',
    'about': 'About / Description - This text describes the restaurant',
    'home': 'General Info - General restaurant information',
    'contact': 'Contact / Location - Location or contact information',
    'events': 'Events - Event-related information',
}

# --- Streamlit UI ---
st.set_page_config(page_title="The Hickory Kampala - NLP Classifier", layout="centered")

st.title("The Hickory Kampala")
st.subheader("Restaurant Content Classifier")
st.markdown("Enter any restaurant-related text and the model will classify it into the appropriate category.")
st.markdown("---")

# Initialize session state for text input
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

user_input = st.text_area(
    "Enter text to classify:",
    value=st.session_state.input_text,
    placeholder="e.g., Grilled salmon fillet with creamy Tuscan sauce served with risotto rice",
    height=120
)

def classify_text(text):
    """Classify text and display results."""
    processed = preprocess(text)
    vec = tfidf.transform([processed])
    prediction = model.predict(vec)[0]

    # Get confidence if model supports predict_proba
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(vec)[0]
        classes = model.classes_
        confidence = max(proba)

        st.success(f"**Predicted Category: {prediction.upper()}**")
        st.markdown(CATEGORY_INFO.get(prediction, prediction))
        st.markdown(f"**Confidence:** {confidence:.1%}")

        st.markdown("#### All Category Probabilities:")
        for cls, prob in sorted(zip(classes, proba), key=lambda x: x[1], reverse=True):
            st.progress(prob, text=f"{cls}: {prob:.1%}")
    else:
        st.success(f"**Predicted Category: {prediction.upper()}**")
        st.markdown(CATEGORY_INFO.get(prediction, prediction))

if st.button("Classify", type="primary"):
    if user_input.strip():
        classify_text(user_input)
    else:
        st.warning("Please enter some text to classify.")

st.markdown("---")
st.markdown("#### Try these examples:")

examples = [
    "Grilled beef fillet with mushroom sauce and mashed potatoes",
    "Vodka based cocktail with fresh lime and mint leaves",
    "South African Cabernet Sauvignon with dark fruit and oak notes",
    "The restaurant has excellent ambiance and friendly staff",
    "Red velvet cake with cream cheese frosting",
]

cols = st.columns(len(examples))
for i, ex in enumerate(examples):
    with cols[i]:
        if st.button(f"Example {i+1}", key=f"ex_{i}", help=ex):
            st.session_state.input_text = ex
            st.rerun()

st.markdown("---")
st.caption("Omoding Isaac (B31331) | MSc Data Science | Uganda Christian University | EASTER 2026")
