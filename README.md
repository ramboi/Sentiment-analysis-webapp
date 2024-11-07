# Sentiment Analysis Application

This project is a comprehensive sentiment analysis application developed with **Streamlit**. It allows users to input text or upload PDF files to analyze sentiment, detect language, and visualize sentiment trends. The application includes support for multiple sentiment analysis techniques, language detection, translation, trend visualization, and export of analysis results.

---

## Overview

This sentiment analysis tool provides a streamlined way to assess the emotional tone of user inputs and PDF content. It uses the **TextBlob** and **VADER** sentiment analysis models to evaluate and visualize the sentiment trend across multi-page PDF documents. Additionally, the app supports language detection and translation, enabling accurate sentiment analysis even on non-English text. Users can export results in CSV, Excel, or Text formats.

## Features

- **Sentiment Analysis Models**: Uses TextBlob and VADER for lexical-based sentiment scoring.
- **PDF Text Extraction**: Supports PDF uploads, extracts text, and allows direct analysis.
- **Language Detection & Translation**: Detects the language of the input text and translates it to English for accurate sentiment scoring.
- **Sentiment Trends Visualization**: Displays sentiment trends across PDF pages to highlight sentiment changes throughout the document.
- **Data Export Options**: Users can export sentiment analysis results in CSV, Excel, or Text formats.

## Technologies Used

- **Python**: Core programming language.
- **Streamlit**: For building the web interface.
- **TextBlob**: For sentiment analysis and language processing.
- **VADER (Valence Aware Dictionary and sEntiment Reasoner)**: For rule-based sentiment analysis.
- **PyMuPDF (Fitz)**: For PDF text extraction.
- **LangDetect & Google Translator (Deep Translator)**: For language detection and translation.
- **Matplotlib**: For plotting sentiment trends.
- **Pandas**: For data handling and export functionality.

## Installation

To get started, clone this repository and install the required packages:

```bash
git clone https://github.com/ramboi/sentiment-analysis-app.git
cd sentiment-analysis-app
pip install -r requirements.txt
streamlit run app.py
