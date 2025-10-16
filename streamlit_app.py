import streamlit as st
import sqlite3
from PIL import Image

st.set_page_config(page_title="OCR Question Matcher", layout="wide")
st.title("🔍 OCR Question Matcher Demo")
st.write("Demo Version - Upload any image to simulate OCR processing")

uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

def main():
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
        
        with col2:
            st.subheader("Simulated OCR Results")
            
            # Simulated OCR text
            sample_questions = [
                "Is the sky blue? - Result: TRUE",
                "Do computers use electricity? - Result: TRUE", 
                "Can humans breathe underwater? - Result: FALSE",
                "Is Python a programming language? - Result: TRUE"
            ]
            
            for question in sample_questions:
                st.write(f"• {question}")
            
            st.success("✅ Demo: Full version includes real OCR and database matching")

if __name__ == "__main__":
    main()
