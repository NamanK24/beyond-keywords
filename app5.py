import os
import time
import numpy as np
import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources
nltk.download("punkt")
nltk.download("stopwords")


class ResumeAnalyzer:
    @staticmethod
    def pdf_to_text(pdf):
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    @staticmethod
    def clean_text(text):
        cleaned_text = "".join(
            [char for char in text if char.isalnum() or char.isspace()]
        )
        return cleaned_text

    @staticmethod
    def tokenize_text(text):
        words = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words("english"))
        filtered_words = [
            word.lower() for word in words if word.lower() not in stop_words
        ]
        return filtered_words

    @staticmethod
    def get_word_frequency(words):
        word_freq = Counter(words)
        return word_freq

    @staticmethod
    def summarize_resume(text, min_sentence_ratio=0.1):
        sentences = sent_tokenize(text)
        if len(sentences) > 3:
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform(sentences)
            similarity_matrix = cosine_similarity(vectors, vectors)
            np.fill_diagonal(similarity_matrix, 0)  # Exclude self-similarity
            sentence_scores = similarity_matrix.sum(axis=1)
            summary_indices = np.argsort(sentence_scores)[::-1][
                :3
            ]  # Get top 3 sentences
            summary = [sentences[i] for i in summary_indices]
            return " ".join(summary)
        else:
            return text

    @staticmethod
    def analyze_strengths_weaknesses(
        words, hr_skills, min_frequency=1.5, min_ratio=0.005
    ):
        freq_dist = FreqDist(words)
        total_words = len(words)
        strengths = [
            word
            for word, freq in freq_dist.items()
            if freq / total_words >= min_ratio and freq >= min_frequency
        ]
        weaknesses = [
            word
            for word, freq in freq_dist.items()
            if freq / total_words <= min_ratio / 2 and freq >= 1
        ]
        highlighted_text = ResumeAnalyzer.highlight_skills(words, hr_skills)
        return strengths, weaknesses, highlighted_text

    @staticmethod
    def suggest_job_titles(words, min_frequency=1.0, min_ratio=0.005):
        freq_dist = FreqDist(words)
        total_words = len(words)
        job_titles = [
            word
            for word, freq in freq_dist.items()
            if freq / total_words >= min_ratio and freq >= min_frequency
        ]
        return job_titles

    @staticmethod
    def highlight_skills(words, skills):
        highlighted_words = []
        for word in words:
            if word.lower() in skills:
                highlighted_words.append(f"<mark>{word}</mark>")
            else:
                highlighted_words.append(word)
        return " ".join(highlighted_words)


def scrape_linkedin_jobs(job_title):
    url = "https://www.linkedin.com/jobs/"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)

    search_box = driver.find_element(By.XPATH, "//input[@name='keywords']")
    search_box.clear()
    search_box.send_keys(job_title)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    job_listings = []
    job_elements = driver.find_elements(
        By.XPATH, "//li[contains(@class, 'job-result-card')]"
    )
    for job_element in job_elements:
        title = job_element.find_element(
            By.XPATH, ".//span[@class='screen-reader-text']"
        ).text.strip()
        company = job_element.find_element(
            By.XPATH, ".//h4[@class='base-search-card__subtitle']"
        ).text.strip()
        location = job_element.find_element(
            By.XPATH, ".//span[@class='job-result-card__location']"
        ).text.strip()
        job_listings.append({"Title": title, "Company": company, "Location": location})

    driver.quit()
    return job_listings


def main():
    st.set_page_config(page_title="Resume Analyzer AI", layout="wide")
    st.markdown(
        """
        <style>
            [data-testid="stHeader"] {
                background: rgba(0,0,0,0);
            }
        </style>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h1 style="text-align: center;">AI-Powered Resume Analyzer</h1>',
        unsafe_allow_html=True,
    )

    hr_skills = ["python", "ai", "rait", "javascript", "development"]

    option = st.sidebar.selectbox(
        "Select Option",
        [
            "Summary",
            "Strength Analysis",
            "Weakness Analysis",
            "Job Title Suggestions",
            "Leaderboard",
            "Scrape LinkedIn Jobs",
        ],
    )

    uploaded_files = os.listdir("uploads")

    if option == "Summary":
        st.subheader("Resume Summary")
        use_existing_resume = st.checkbox("Use existing resume")
        if use_existing_resume:
            selected_resume = st.selectbox("Select Resume", uploaded_files)
            if selected_resume:
                with open(os.path.join("uploads", selected_resume), "rb") as f:
                    text = ResumeAnalyzer.pdf_to_text(f)
                cleaned_text = ResumeAnalyzer.clean_text(text)
                summary = ResumeAnalyzer.summarize_resume(cleaned_text)
                st.write(summary)
        else:
            uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")
            if uploaded_file is not None:
                with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                text = ResumeAnalyzer.pdf_to_text(uploaded_file)
                cleaned_text = ResumeAnalyzer.clean_text(text)
                summary = ResumeAnalyzer.summarize_resume(cleaned_text)
                st.write(summary)

    elif option == "Strength Analysis":
        st.subheader("Strength Analysis")
        use_existing_resume = st.checkbox("Use existing resume")
        if use_existing_resume:
            selected_resume = st.selectbox("Select Resume", uploaded_files)
            if selected_resume:
                with open(os.path.join("uploads", selected_resume), "rb") as f:
                    text = ResumeAnalyzer.pdf_to_text(f)
                cleaned_text = ResumeAnalyzer.clean_text(text)
                words = ResumeAnalyzer.tokenize_text(cleaned_text)
                strengths, weaknesses, highlighted_text = (
                    ResumeAnalyzer.analyze_strengths_weaknesses(words, hr_skills)
                )
                st.write("Strengths:", strengths)
                st.markdown(highlighted_text, unsafe_allow_html=True)
        else:
            uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")
            if uploaded_file is not None:
                with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                text = ResumeAnalyzer.pdf_to_text(uploaded_file)
                cleaned_text = ResumeAnalyzer.clean_text(text)
                words = ResumeAnalyzer.tokenize_text(cleaned_text)
                strengths, weaknesses, highlighted_text = (
                    ResumeAnalyzer.analyze_strengths_weaknesses(words, hr_skills)
                )
                st.write("Strengths:", strengths)
                st.markdown(highlighted_text, unsafe_allow_html=True)

    elif option == "Weakness Analysis":
        st.subheader("Weakness Analysis")
        use_existing_resume = st.checkbox("Use existing resume")
        if use_existing_resume:
            selected_resume = st.selectbox("Select Resume", uploaded_files)
            if selected_resume:
                with open(os.path.join("uploads", selected_resume), "rb") as f:
                    text = ResumeAnalyzer.pdf_to_text(f)
                cleaned_text = ResumeAnalyzer.clean_text(text)
                words = ResumeAnalyzer.tokenize_text(cleaned_text)
                strengths, weaknesses, highlighted_text = (
                    ResumeAnalyzer.analyze_strengths_weaknesses(words, hr_skills)
                )
                st.write("Weaknesses:", weaknesses)
                st.markdown(highlighted_text, unsafe_allow_html=True)
        else:
            uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")
            if uploaded_file is not None:
                with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                text = ResumeAnalyzer.pdf_to_text(uploaded_file)
                cleaned_text = ResumeAnalyzer.clean_text(text)
                words = ResumeAnalyzer.tokenize_text(cleaned_text)
                strengths, weaknesses, highlighted_text = (
                    ResumeAnalyzer.analyze_strengths_weaknesses(words, hr_skills)
                )
                st.write("Weaknesses:", weaknesses)
                st.markdown(highlighted_text, unsafe_allow_html=True)

    elif option == "Job Title Suggestions":
        st.subheader("Job Title Suggestions")
        use_existing_resume = st.checkbox("Use existing resume")
        if use_existing_resume:
            selected_resume = st.selectbox("Select Resume", uploaded_files)
            if selected_resume:
                with open(os.path.join("uploads", selected_resume), "rb") as f:
                    text = ResumeAnalyzer.pdf_to_text(f)
                cleaned_text = ResumeAnalyzer.clean_text(text)
                words = ResumeAnalyzer.tokenize_text(cleaned_text)
                job_titles = ResumeAnalyzer.suggest_job_titles(words)
                st.write("Suggested Job Titles:", job_titles)
        else:
            uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")
            if uploaded_file is not None:
                with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                text = ResumeAnalyzer.pdf_to_text(uploaded_file)
                cleaned_text = ResumeAnalyzer.clean_text(text)
                words = ResumeAnalyzer.tokenize_text(cleaned_text)
                job_titles = ResumeAnalyzer.suggest_job_titles(words)
                st.write("Suggested Job Titles:", job_titles)

    elif option == "Leaderboard":
        st.subheader("Resume Leaderboard")
        leaderboard = []
        for resume in uploaded_files:
            with open(os.path.join("uploads", resume), "rb") as f:
                text = ResumeAnalyzer.pdf_to_text(f)
            cleaned_text = ResumeAnalyzer.clean_text(text)
            words = ResumeAnalyzer.tokenize_text(cleaned_text)
            highlighted_text = ResumeAnalyzer.highlight_skills(words, hr_skills)
            highlighted_words_count = highlighted_text.count("<mark>")
            leaderboard.append((resume, highlighted_words_count))

        leaderboard.sort(key=lambda x: x[1], reverse=True)
        st.write("Leaderboard:")
        for idx, (resume, count) in enumerate(leaderboard, start=1):
            st.write(f"{idx}. {resume} - Highlighted Keywords Count: {count}")

    elif option == "Scrape LinkedIn Jobs":
        st.subheader("Scrape LinkedIn Jobs")
        job_title = st.text_input("Enter Job Title")
        if job_title:
            job_listings = scrape_linkedin_jobs(job_title)
            if job_listings:
                st.write("Job Listings:")
                for job_listing in job_listings:
                    st.write(job_listing)


if __name__ == "__main__":
    # Create directory to store uploaded resumes if not exists
    os.makedirs("uploads", exist_ok=True)
    main()
