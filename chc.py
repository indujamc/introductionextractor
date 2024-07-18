
import streamlit as st
from pdfminer.high_level import extract_text
from nltk.tokenize import word_tokenize
from summarizer import Summarizer
from transformers import logging
import nltk

# Disable transformers logging to avoid unnecessary logs in the app
logging.set_verbosity_error()

# Ensure NLTK data is downloaded
#nltk.download('punkt')

def extract_content_between_headings(text, start_heading_keyword):
    content = []
    lines = text.splitlines()
    start_found = False
    next_heading = None

    for line in lines:
        line = line.strip()
        if line:
            words = word_tokenize(line)
            # Check if the line is a heading
            if words and len(words) <= 5 and (words[0][0].isupper() or words[0][0].isdigit()) and not line.endswith('.'):
                if start_found and next_heading is None:
                    next_heading = line
                    break  # Stop after finding the next heading after the start_heading
                # Match any heading containing the start_heading_keyword
                elif start_heading_keyword.lower() in line.lower():
                    start_found = True
            elif start_found and next_heading is None:
                content.append(line)

    return '\n'.join(content), next_heading

def main():
    st.title("PDF Content Extractor and Summarizer")
    
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        start_heading_keyword = st.text_input("Enter the heading keyword to start extraction:")
        
        if st.button("Extract and Summarize"):
            if start_heading_keyword:
                text = extract_text(uploaded_file)
                content, next_heading = extract_content_between_headings(text, start_heading_keyword)
                
                if content:
                    st.write(f"Content between '{start_heading_keyword}' and '{next_heading}':")
                    st.text(content)
                    
                    # Summarize the content
                    model = Summarizer()
                    summary = model(content, num_sentences=5)
                    st.write(f"Summary of the '{start_heading_keyword}' and '{next_heading}':")
                    st.text(summary)
                else:
                    st.write("No content found between the specified headings.")
            else:
                st.write("Please enter a heading keyword to start extraction.")

if __name__ == "__main__":
    main()
