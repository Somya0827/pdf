import os
import PyPDF2
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client with your API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(file)  # Use PdfReader instead of PdfFileReader
    text = ''
    
    for page in range(len(pdf_reader.pages)):  # Use len(pdf_reader.pages) instead of pdf_reader.numPages
        text += pdf_reader.pages[page].extract_text()  # Updated method call
    
    return text

def get_response(question, pdf_content):
    """Send a question along with PDF content to the Groq API."""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Answer the following question based on the provided text: {question}\n\nText: {pdf_content}"
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    return chat_completion.choices[0].message.content

# Streamlit application layout
st.title("PDF Query Application")
st.write("Upload a PDF file and ask questions about its content.")

# File uploader for PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    pdf_content = extract_text_from_pdf(uploaded_file)
    
    # Display the extracted text (optional)
    st.subheader("Extracted Text")
    st.write(pdf_content)

    # User input for question
    question = st.text_input("Ask a question about the PDF content:")

    if st.button("Get Answer"):
        if question:
            # Get response from Groq API
            answer = get_response(question, pdf_content)
            st.subheader("Answer")
            st.write(answer)
        else:
            st.warning("Please enter a question.")
