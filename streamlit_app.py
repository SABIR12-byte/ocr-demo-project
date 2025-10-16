import streamlit as st
import cv2
import pytesseract
import sqlite3
import numpy as np
from PIL import Image
import tempfile
import os

# Configure page
st.set_page_config(page_title="OCR Question Matcher", layout="wide")

st.title("🔍 OCR Question Matcher Demo")
st.write("Upload an image containing a question to check against our database")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

def preprocess_image(image):
    """Basic image preprocessing for better OCR"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    return thresh

def extract_text_from_image(image):
    """Extract text using OCR"""
    try:
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # OCR configuration
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        return text.strip()
    except Exception as e:
        st.error(f"OCR Error: {str(e)}")
        return ""

def clean_ocr_text(text):
    """Clean and normalize OCR text"""
    # Remove extra whitespace and newlines
    cleaned = ' '.join(text.split())
    
    # Basic cleaning - you might need to adjust this
    cleaned = cleaned.replace('|', 'I').replace('\\', '').replace('/', '')
    
    return cleaned

def query_database(question):
    """Query the SQLite database for the question"""
    try:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        
        # Use LIKE for partial matching
        cursor.execute("SELECT answer FROM questions WHERE question LIKE ?", (f'%{question}%',))
        result = cursor.fetchone()
        
        conn.close()
        
        return result[0] if result else None
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

def main():
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
            # Convert to OpenCV format
            image_cv = np.array(image)
            if len(image_cv.shape) == 3:
                image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
        
        with col2:
            st.subheader("OCR Results")
            
            with st.spinner("Processing image and extracting text..."):
                # Extract text
                raw_text = extract_text_from_image(image_cv)
                
                if raw_text:
                    cleaned_text = clean_ocr_text(raw_text)
                    
                    st.write("**Extracted Text:**")
                    st.info(cleaned_text)
                    
                    # Query database
                    answer = query_database(cleaned_text)
                    
                    if answer is not None:
                        st.success(f"**Result: {answer}**")
                    else:
                        st.error("❌ No matching question found in database")
                else:
                    st.error("❌ No text detected in the image")

        # Demo limitations notice
        st.warning("""
        **Demo Limitations:**
        - This is a temporary demo version
        - Database contains sample questions only
        - Full version includes real-time camera processing
        - Contact for full implementation
        """)

if __name__ == "__main__":
    main()