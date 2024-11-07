import streamlit as st
from PIL import Image
import fitz  # PyMuPDF for PDF text extraction
import matplotlib.pyplot as plt
from langdetect import detect, DetectorFactory
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd
from io import BytesIO
from utils import *
import langdetect

# Seed for language detection consistency
DetectorFactory.seed = 0

def extract_text_from_pdf(pdf_file):
    pdf_reader = fitz.open(stream=pdf_file.read(), filetype="pdf")
    page_texts = [pdf_reader[page_num].get_text() for page_num in range(len(pdf_reader))]
    pdf_reader.close()
    return page_texts

def detect_language(text):
    try:
        language = detect(text)
    except langdetect.lang_detect_exception.LangDetectException:
        language = "unknown"
    return language

def textblobSentiment(user_input):
    # Translate non-English text to English
    language = detect_language(user_input)
    if language != 'en':
        user_input = GoogleTranslator(source=language, target='en').translate(user_input)
    
    # Analyze sentiment
    textblob_sentiment = textblob_score(user_input)
    return textblob_sentiment, language

def VaderSentiment(user_input):
    vader_sentiment = vader_score(user_input)
    return vader_sentiment

def sentiment_trends(page_texts, method):
    sentiments = []
    for page_text in page_texts:
        if method == "TextBlob":
            sentiment = textblob_score(page_text)
        elif method == "Vader":
            sentiment = vader_score(page_text)
        
        # Extract polarity score as a number
        polarity_score = float(sentiment.split("(")[-1].replace("%)", "").strip())
        sentiments.append(polarity_score)
    return sentiments

def plot_sentiment_trend(sentiments, method):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(sentiments) + 1), sentiments, marker='o', linestyle='-', color='b')
    plt.title(f"Sentiment Trend Across PDF Pages ({method})")
    plt.xlabel("Page Number")
    plt.ylabel("Sentiment Polarity (%)")
    plt.grid()
    st.pyplot(plt)

def main():
    st.title("Sentiment Analysis App with Multi-Language and Sentiment Trends Visualization")
    image_path = "data/Sentiment-Analysis.png"
    st.image(image_path, use_column_width=True)

    # Adding PDF upload option
    uploaded_file = st.file_uploader("Upload a PDF file for sentiment analysis", type=["pdf"])

    # Check if a file was uploaded
    if uploaded_file:
        page_texts = extract_text_from_pdf(uploaded_file)
        pdf_text = " ".join(page_texts)  # Combine all pages' text
    else:
        page_texts = []
        pdf_text = ""

    # Text input area
    user_input = st.text_area(label="**Enter your Opinion or Use Extracted PDF Text:**", height=150, value=pdf_text)

    # Options for sentiment analysis
    data = ["TextBlob", "Vader"]
    selected_option = st.sidebar.selectbox("Select an option", data)
    plot_selection = st.sidebar.radio("Performance Visualization", ('Yes', 'No'))

    # Sentiment Trends Visualization if a PDF is uploaded
    if uploaded_file and st.sidebar.checkbox("Show Sentiment Trend Across Pages"):
        sentiments = sentiment_trends(page_texts, selected_option)
        plot_sentiment_trend(sentiments, selected_option)

    if user_input:
        language = detect_language(user_input)
        st.write(f"**Detected Language:** {language}")

        # Perform sentiment analysis based on the selected method
        if selected_option == "TextBlob":
            sentiment, detected_language = textblobSentiment(user_input)
            st.write(f"**TextBlob Sentiment:** {sentiment}")
        elif selected_option == "Vader":
            vader_sentiment = VaderSentiment(user_input)
            st.write(f"**VADER Sentiment:** {vader_sentiment}")

        # Prepare DataFrame for export
        data = {
            "User Input": [user_input],
            "Detected Language": [language],
            "TextBlob Sentiment": [sentiment if selected_option == "TextBlob" else ""],
            "VADER Sentiment": [vader_sentiment if selected_option == "Vader" else ""]
        }
        df = pd.DataFrame(data)

        # Export options
        st.subheader("Export Sentiment Analysis Results")
        export_format = st.selectbox("Choose Export Format", ["CSV", "Excel", "Text"])

        if export_format == "CSV":
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download CSV", data=csv, file_name="sentiment_analysis.csv", mime="text/csv")

        elif export_format == "Excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name="Sheet1")
                writer.save()
            st.download_button(label="Download Excel", data=output.getvalue(), file_name="sentiment_analysis.xlsx", mime="application/vnd.ms-excel")

        elif export_format == "Text":
            text_data = df.to_string(index=False)
            st.download_button(label="Download Text", data=text_data, file_name="sentiment_analysis.txt", mime="text/plain")

if __name__ == "__main__":
    main()
