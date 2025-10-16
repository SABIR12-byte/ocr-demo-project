import streamlit as st
import sqlite3
import numpy as np
from PIL import Image
import io
import base64

# Configure page
st.set_page_config(page_title="OCR Question Matcher", layout="wide")

st.title("🔍 OCR Question Matcher Demo")
st.write("Upload an image containing a question to check against our database")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

def simulate_ocr_text():
    """Simulate OCR extraction for demo purposes"""
    sample_texts = [
        "Is the sky blue?",
        "Do computers use electricity?",
        "Can humans breathe underwater?",
        "Is Python a programming language?",
        "Do cars fly?",
        "Is the Earth flat?",
        "Does water boil at 100 degrees Celsius?",
        "Can fish live without water?"
    ]
    return np.random.choice(sample_texts)

def query_database(question):
    """Query the SQLite database for the question"""
    try:
        # For demo, we'll use a simulated database
        sample_data = {
            "Is the sky blue?": "TRUE",
            "Do computers use electricity?": "TRUE", 
            "Can humans breathe underwater?": "FALSE",
            "Is Python a programming language?": "TRUE",
            "Do cars fly?": "FALSE",
            "Is the Earth flat?": "FALSE",
            "Does water boil at 100 degrees Celsius?": "TRUE",
            "Can fish live without water?": "FALSE"
        }
        
        # Find closest match
        for db_question, answer in sample_data.items():
            if any(word in question.lower() for word in db_question.lower().split()):
                return answer
        return None
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
        
        with col2:
            st.subheader("OCR Results")
            
            with st.spinner("Processing image and extracting text..."):
                # Simulate OCR processing
                extracted_text = simulate_ocr_text()
                
                st.write("**Extracted Text:**")
                st.info(extracted_text)
                
                # Query database
                answer = query_database(extracted_text)
                
                if answer is not None:
                    st.success(f"**Result: {answer}**")
                    
                    # Show matching animation
                    if answer.upper() == "TRUE":
                        st.balloons()
                    else:
                        st.warning("Question matched but answer is FALSE")
                else:
                    st.error("❌ No matching question found in database")

        # Demo limitations notice
        st.warning("""
        **Demo Limitations:**
        - This is a simulated OCR demo version
        - Full version includes real Tesseract OCR and camera processing
        - Contact for full implementation with live camera support
        """)

if __name__ == "__main__":
    main()
