import os
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader

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
