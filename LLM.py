import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- CONFIGURATION & SETUP ---
def setup_environment():
    """Load environment variables and configure the Gemini API."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ API Key missing! Please check your .env file.")
        return None
    
    genai.configure(api_key=api_key)
    return api_key

def get_ai_response(user_query):
    """Fetch structured recommendations from Gemini API."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Professional Prompt Engineering for structured output
        system_instruction = (
            "You are a professional media recommendation engine. "
            "Analyze the user's emotional state or requirements and provide curated suggestions. "
            "Format: 3 Movies and 2 Books. Include a 'Why it fits your mood' section for each recommendation. "
            "Use a clean markdown structure with bold headers and bullet points."
        )
        
        full_prompt = f"{system_instruction}\nUser Mood/Request: {user_query}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error fetching recommendations: {str(e)}"

# --- UI DESIGN (Streamlit) ---
def main():
    # Page Configuration
    st.set_page_config(page_title="VibeCheck AI", page_icon="🎬", layout="centered")

    # Sidebar for project metadata
    with st.sidebar:
        st.title("📌 Project Metadata")
        st.info("Model: Gemini 1.5 Flash\nFramework: Streamlit\nEnvironment: Python 3.x")
        st.markdown("---")
        st.caption("This application utilizes Generative AI to map user sentiment to curated media content.")

    # Main Header Section
    st.title("🎬 VibeCheck: AI Recommendation Engine")
    st.write("Professional-grade movie and book suggestions tailored to your current mood.")

    # Custom CSS for refined UI
    st.markdown("""
        <style>
        .stTextArea textarea { font-size: 1.1rem !important; }
        .stButton>button {
            border-radius: 20px;
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ff3333;
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize API
    api_key = setup_environment()

    # User Input Section
    mood_input = st.text_area("Describe your current mood or interest:", 
                             placeholder="E.g., I am looking for an uplifting story with a touch of mystery...",
                             height=150)

    # Execution Trigger
    if st.button("Generate Curated List"):
        if not mood_input:
            st.warning("Please provide a mood description to proceed.")
        elif not api_key:
            st.error("Authentication Error: API Key not found in environment.")
        else:
            with st.spinner('Analyzing sentiment and fetching recommendations...'):
                result = get_ai_response(mood_input)
                
                st.markdown("### 🌟 Your Personalized Recommendations")
                st.markdown("---")
                st.markdown(result)
                st.balloons() # Visual feedback for successful generation

    # Footer Section
    st.markdown("---")
    st.caption("© 2026 AI Media Engine | Software Engineering Project")

if __name__ == "__main__":
    main()