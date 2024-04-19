import os
import streamlit as st
from resume_analyzer import ResumeAnalyzer
from linkedin_scraper import scrape_linkedin_jobs


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
        '<h1 style="text-align: center;">BEYOND-KEYWORDS</h1>',
        unsafe_allow_html=True,
    )

    hr_skills = ["python", "ai", "rait", "javascript", "development"]

    uploaded_files = os.listdir("uploads")

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
    os.makedirs("uploads", exist_ok=True)
    main()
