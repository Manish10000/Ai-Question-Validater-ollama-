import streamlit as st
import pandas as pd
import re
import time
import io
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configure the Llama 3.2 model
llm = ChatOllama(model="llama3.2:3b", temperature=0.7, base_url="http://localhost:11434")
search_tool = DuckDuckGoSearchAPIWrapper(max_results=5)

# Define the prompt template
prompt_template = PromptTemplate(
    template="""
    You are an AI assistant that provides accurate and concise answers based on web search results.
    Question: {question}
    Options:
    A) {option_a}
    B) {option_b}
    C) {option_c}
    D) {option_d}
    Web Search Context: {context}
    
    Provide the correct answer in the following format:
    ANSWER: X
    """,
    input_variables=["question", "option_a", "option_b", "option_c", "option_d", "context"],
)

response_chain = prompt_template | llm | StrOutputParser()

def generate_sample_csv():
    sample_data = {
        "id": [1, 2],
        "sub_category": ["Basic Hardware", "Software"],
        "category": ["Technical", "Technical"],
        "question_name": ["Which component stores the OS?", "What is an example of OS?"],
        "question_description": ["Identify where the OS is stored.", "Choose an example of an OS."],
        "A": ["RAM", "Chrome"],
        "B": ["Hard Drive", "Windows"],
        "C": ["GPU", "Google Drive"],
        "D": ["Cache", "CPU"],
        "Answer": ["B", "B"],
        "Level": [1, 1]
    }
    df = pd.DataFrame(sample_data)
    return df.to_csv(index=False, encoding='utf-8')

st.title("Question Validation System")

# Button to download sample CSV
sample_csv = generate_sample_csv()
st.download_button(
    label="Download Sample CSV",
    data=sample_csv,
    file_name="sample_questions.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Clear previous content
    st.session_state.clear()
    df = pd.read_csv(uploaded_file)
    report = []
    total_questions = len(df)
    progress_bar = st.progress(0)
    
    for index, row in df.iterrows():
        with st.expander(f"🔍 Processing Question {row['id']}: {row['question_description']}", expanded=True):
            question_text = row["question_description"]
            option_a, option_b, option_c, option_d = row["A"], row["B"], row["C"], row["D"]
            correct_answer = row["Answer"].strip().upper()

            st.write(f"Options: A) {option_a}, B) {option_b}, C) {option_c}, D) {option_d}")
            
            with st.spinner("🔄 Searching the internet..."):
                search_results = search_tool.run(question_text)
                time.sleep(2)  # Simulating loading time
            
            with st.spinner("🤖 Generating AI-based answer..."):
                ai_answer_raw = response_chain.invoke({
                    "question": question_text,
                    "option_a": option_a,
                    "option_b": option_b,
                    "option_c": option_c,
                    "option_d": option_d,
                    "context": search_results
                }).strip().upper()
                time.sleep(2)
            
            # Extract AI answer
            match = re.search(r"ANSWER:\s*(A|B|C|D)", ai_answer_raw)
            ai_answer = match.group(1) if match else "?"
            
            # Determine status
            status = "✅ Correct" if ai_answer == correct_answer else "❌ Incorrect"
            st.write(f"💡 AI Answer: {ai_answer}")
            st.write(f"📌 Correct Answer: {correct_answer}")
            st.write(f"📊 Status: {status}")
            
            # Append to report
            report.append([row['id'], question_text, correct_answer, ai_answer, status])
            
            # Update progress bar
            progress_bar.progress((index + 1) / total_questions)
    
    # Generate downloadable report
    report_df = pd.DataFrame(report, columns=["ID", "Question", "Correct Answer", "AI Answer", "Status"])
    report_csv = report_df.to_csv(index=False, encoding='utf-8')
    st.download_button("Download Report", report_csv, "question_validation_report.csv", "text/csv")
    
    # Auto-scroll to bottom
    st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)
