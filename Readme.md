# Beyond-Keywords: Resume Analyzer and Job Search Tool

Beyond-Keywords is an AI-powered tool designed to analyze resumes, identify strengths and weaknesses,
suggest job titles, and scrape job listings from LinkedIn.
This tool aims to provide insights to both job seekers and HR professionals, helping them make informed decisions during the recruitment process.


## Features

1. Resume Analysis
Summary: Generates a concise summary of the resume, highlighting key information.
Strength Analysis: Identifies strengths and highlights relevant skills specified by HR professionals.
Weakness Analysis: Identifies potential weaknesses and areas that might need improvement.

3. Job Search
Job Title Suggestions: Recommends job titles based on the content of the resume.
LinkedIn Job Scraping: Scrapes job listings from LinkedIn based on a specified job title, enabling users to explore job opportunities directly from the application.

## Technologies Used

Python: Core programming language used for development.
Streamlit: Web application framework for building interactive dashboards.
NLTK (Natural Language Toolkit): Library for natural language processing tasks such as tokenization and stopwords removal.
Selenium: Web scraping tool used for scraping job listings from LinkedIn.
PyPDF2: Library for reading PDF files.
NumPy: Library for numerical computing.
pandas: Library for data manipulation and analysis.
scikit-learn (sklearn): Library for machine learning tasks.

## Installation and Usage
Make sure to use Python 3.8.10

Install all the required libraries
```bash
pip install -r requirements.txt
```

To run use the following command:
```bash
streamlit run beyond-keywords.py
```



