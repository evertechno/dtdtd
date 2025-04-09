import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
from io import BytesIO

# Function to extract emails from a given PDF file
def extract_emails_from_pdf(pdf_file):
    # Open the provided PDF using PyMuPDF from the byte content
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    emails = set()  # Using a set to avoid duplicate emails
    
    # Iterate over all pages in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text("text")  # Extract text as plain text
        
        # Regular expression to match emails
        found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_text)
        emails.update(found_emails)  # Add found emails to the set

    return list(emails)  # Convert set back to list

# Function to create and save CSV from email list
def save_emails_to_csv(emails):
    if not emails:
        return None
    
    # Convert emails list to a pandas DataFrame
    df = pd.DataFrame(emails, columns=["Email Addresses"])
    
    # Save DataFrame to a CSV string
    csv_data = df.to_csv(index=False)
    
    return csv_data

# Streamlit app UI and logic
def main():
    # Set up the title and description of the app
    st.title("Email Extractor from PDFs")
    st.write("""
    Upload a PDF file, and this app will extract all email addresses from the document. 
    You can then download the extracted emails as a CSV file.
    """)

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Process the PDF file
        st.info("Processing the PDF... Please wait.")
        
        # Read the uploaded file as a BytesIO object (in-memory file)
        pdf_file = BytesIO(uploaded_file.read())
        
        # Extract emails from the PDF
        emails = extract_emails_from_pdf(pdf_file)
        
        if emails:
            st.success(f"Found {len(emails)} email(s).")
            
            # Display the extracted emails in the app
            st.write("### Extracted Email Addresses:")
            st.write(emails)

            # Create and provide a CSV download option
            csv_data = save_emails_to_csv(emails)
            if csv_data:
                st.download_button(
                    label="Download emails as CSV",
                    data=csv_data,
                    file_name="extracted_emails.csv",
                    mime="text/csv"
                )
        else:
            st.warning("No email addresses were found in the PDF.")
    
if __name__ == "__main__":
    main()
