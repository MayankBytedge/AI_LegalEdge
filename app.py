
import streamlit as st
import json
import os
import requests
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from PyPDF2 import PdfReader
import re
import time

# Configure page
st.set_page_config(
    page_title="LegalEdge AI", 
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .case-analysis {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #000;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: green;
        margin-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

class LegalAssistant:
    def __init__(self, api_key: str):
        """Initialize the Legal Assistant with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.case_memory = {}

    def extract_pdf_text(self, uploaded_file) -> str:
        """Extract text from uploaded PDF"""
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""

    def extract_case_details(self, text: str) -> Dict[str, Any]:
        """Extract key case details using Gemini"""
        prompt = f"""
        Analyze the following legal case text and extract key information in JSON format:

        {text[:8000]}  # Limit text to avoid token limits

        Please extract and return ONLY a JSON object with these fields:
        {{
            "case_title": "extracted case title",
            "court": "court name",
            "case_type": "criminal/civil/constitutional/administrative",
            "main_issues": ["list", "of", "main", "legal", "issues"],
            "statutes_involved": ["list", "of", "statutes", "sections"],
            "key_facts": "brief summary of key facts",
            "relief_sought": "what relief is being sought",
            "arguments_summary": "summary of main arguments"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            response_text = response.text
            # Find JSON object in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback parsing
                return {
                    "case_title": "Unknown Case",
                    "court": "Unknown Court", 
                    "case_type": "unknown",
                    "main_issues": ["Document analysis pending"],
                    "statutes_involved": [],
                    "key_facts": "Analysis in progress",
                    "relief_sought": "Unknown",
                    "arguments_summary": "Analysis pending"
                }
        except Exception as e:
            st.error(f"Error extracting case details: {str(e)}")
            return {}

    def search_similar_cases(self, case_details: Dict[str, Any]) -> List[Dict[str, str]]:
        """Search for similar cases using Gemini's knowledge"""
        search_prompt = f"""
        Based on this case information:
        - Case Type: {case_details.get('case_type', 'unknown')}
        - Main Issues: {', '.join(case_details.get('main_issues', []))}
        - Statutes: {', '.join(case_details.get('statutes_involved', []))}
        - Key Facts: {case_details.get('key_facts', '')}

        Please provide 5 similar landmark Indian legal cases with brief descriptions.
        Format your response as a list with case name, court, year, and key principle.
        Focus on cases from Supreme Court of India and High Courts.
        """

        try:
            response = self.model.generate_content(search_prompt)
            # Parse the response to extract similar cases
            similar_cases = []
            lines = response.text.split('\n')
            current_case = {}

            for line in lines:
                line = line.strip()
                if line and ('v.' in line or 'vs.' in line or 'V.' in line):
                    if current_case:
                        similar_cases.append(current_case)
                    current_case = {'title': line, 'description': ''}
                elif line and current_case:
                    current_case['description'] += line + ' '

            if current_case:
                similar_cases.append(current_case)

            return similar_cases[:5]  # Return top 5

        except Exception as e:
            st.error(f"Error searching similar cases: {str(e)}")
            return []

    def analyze_case_strength(self, case_details: Dict[str, Any], similar_cases: List[Dict]) -> Dict[str, Any]:
        """Analyze case strength and provide recommendations"""
        analysis_prompt = f"""
        As a legal expert, analyze this case and provide detailed recommendations:

        CASE DETAILS:
        - Title: {case_details.get('case_title', 'Unknown')}
        - Court: {case_details.get('court', 'Unknown')}
        - Type: {case_details.get('case_type', 'unknown')}
        - Issues: {', '.join(case_details.get('main_issues', []))}
        - Statutes: {', '.join(case_details.get('statutes_involved', []))}
        - Facts: {case_details.get('key_facts', '')}
        - Relief Sought: {case_details.get('relief_sought', '')}

        SIMILAR CASES FOUND:
        {chr(10).join([f"- {case.get('title', '')}: {case.get('description', '')}" for case in similar_cases])}

        Please provide a comprehensive analysis in the following format within 500 words:

        **CASE STRENGTH ASSESSMENT (1-10 scale):** [Your assessment with reasoning]

        **CHANCES OF SUCCESS:** [Percentage estimate with detailed reasoning]

        **STRENGTHS OF YOUR CASE:**
        - [List 3-5 key strengths]

        **WEAKNESSES TO ADDRESS:**
        - [List 3-5 potential weaknesses]

        **WHAT YOU CAN CHANGE/IMPROVE:**
        - [Specific actionable recommendations]

        **AREAS FOR FURTHER RESEARCH:**
        - [Specific legal areas, statutes, or cases to research]

        **RECOMMENDED ARGUMENTS:**
        - [Key legal arguments to focus on]

        **WHAT YOU SHOULD KNOW:**
        - [Important legal principles and precedents]

        **DISCLAIMER:** This is AI-generated analysis and should not replace professional legal advice.
        """

        try:
            response = self.model.generate_content(analysis_prompt)
            return {"analysis": response.text}
        except Exception as e:
            st.error(f"Error analyzing case: {str(e)}")
            return {"analysis": "Analysis failed. Please try again."}

    def chat_about_case(self, question: str, case_details: Dict[str, Any], chat_history: List[Dict]) -> str:
        """Handle conversational questions about the case"""
        context = f"""
        You are a legal expert assistant. The user has uploaded a case with these details:
        - Title: {case_details.get('case_title', 'Unknown')}
        - Court: {case_details.get('court', 'Unknown')}
        - Type: {case_details.get('case_type', 'unknown')}
        - Issues: {', '.join(case_details.get('main_issues', []))}
        - Key Facts: {case_details.get('key_facts', '')}

        Chat History:
        {chr(10).join([f"{msg['role']}: {msg['content']}" for msg in chat_history[-5:]])}

        Current Question: {question}

        Please provide a helpful, accurate response based on Indian legal principles in short. 
        Always include relevant case law or statutory references when possible in short.
        Add appropriate disclaimers about seeking professional legal advice in short.
        """

        try:
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question."

# Initialize the app
def main():
    st.markdown('<h1 class="main-header">⚖️ LegalEdge AI</h1>', unsafe_allow_html=True)

    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Configuration")
        api_key = st.text_input("Enter your Key:", type="password", help="Get your API key from Google AI Studio")

        if not api_key:
            st.error("Please enter your key to continue.")
            st.stop()

        st.success("API Key configured!")

        st.header("📋 Features")
        st.write("✅ Upload legal case PDFs")
        st.write("✅ Extract case details")  
        st.write("✅ Find similar cases")
        st.write("✅ Analyze case strength")
        st.write("✅ Get winning chances")
        st.write("✅ Receive recommendations")
        st.write("✅ Conversational Q&A")

        st.markdown("---")
        st.markdown("⚠️ **Disclaimer**: This tool provides AI-generated analysis for informational purposes only and should not replace professional legal advice.")

    # Initialize the assistant
    if 'assistant' not in st.session_state:
        st.session_state.assistant = LegalAssistant(api_key)
    if 'case_details' not in st.session_state:
        st.session_state.case_details = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'case_analyzed' not in st.session_state:
        st.session_state.case_analyzed = False

    # Main interface
    tab1, tab2 = st.tabs(["📄 Upload & Analyze Case", "💬 Chat About Case"])

    with tab1:
        st.header("Upload Your Legal Case")

        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", help="Upload your legal case document")

        if uploaded_file is not None:
            if st.button("🔍 Analyze Case", type="primary"):
                with st.spinner("Extracting text from PDF..."):
                    text = st.session_state.assistant.extract_pdf_text(uploaded_file)

                if text:
                    with st.spinner("Analyzing case details..."):
                        case_details = st.session_state.assistant.extract_case_details(text)
                        st.session_state.case_details = case_details

                    # Display extracted details
                    st.markdown('<div class="case-analysis">', unsafe_allow_html=True)
                    st.subheader("📋 Case Details Extracted")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Case Title:** {case_details.get('case_title', 'Unknown')}")
                        st.write(f"**Court:** {case_details.get('court', 'Unknown')}")
                        st.write(f"**Case Type:** {case_details.get('case_type', 'Unknown').title()}")

                    with col2:
                        st.write(f"**Main Issues:**")
                        for issue in case_details.get('main_issues', [])[:3]:
                            st.write(f"• {issue}")

                        st.write(f"**Statutes Involved:**")
                        for statute in case_details.get('statutes_involved', [])[:3]:
                            st.write(f"• {statute}")

                    st.write(f"**Key Facts:** {case_details.get('key_facts', 'Not extracted')}")
                    st.write(f"**Relief Sought:** {case_details.get('relief_sought', 'Not specified')}")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Find similar cases
                    with st.spinner("Searching for similar cases..."):
                        similar_cases = st.session_state.assistant.search_similar_cases(case_details)

                    if similar_cases:
                        st.subheader("📚 Similar Cases Found")
                        for i, case in enumerate(similar_cases, 1):
                            with st.expander(f"Case {i}: {case.get('title', 'Unknown Case')}"):
                                st.write(case.get('description', 'No description available'))

                    # Analyze case strength
                    with st.spinner("Analyzing case strength and generating recommendations..."):
                        analysis = st.session_state.assistant.analyze_case_strength(case_details, similar_cases)

                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.subheader("🎯 Legal Analysis & Recommendations")
                    st.markdown(analysis.get('analysis', 'Analysis not available'))
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.session_state.case_analyzed = True

                else:
                    st.error("Could not extract text from the PDF. Please check the file and try again.")

    with tab2:
        st.header("💬 Ask Questions About Your Case")

        if not st.session_state.case_analyzed:
            st.info("👆 Please upload and analyze a case first in the 'Upload & Analyze Case' tab.")
        else:
            # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message assistant-message"><strong>Legal Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)

            # Chat input
            question = st.text_input("Ask a question about your case:", placeholder="e.g., What are the strongest arguments I can make?")

            if st.button("Send", type="primary") and question:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "content": question})

                with st.spinner("Thinking..."):
                    response = st.session_state.assistant.chat_about_case(
                        question, 
                        st.session_state.case_details,
                        st.session_state.chat_history
                    )

                # Add assistant response to history
                st.session_state.chat_history.append({"role": "assistant", "content": response})

                # Refresh the page to show new messages
                st.rerun()

            # Quick question buttons
            st.subheader("💡 Quick Questions")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("What are my chances?"):
                    st.session_state.chat_history.append({"role": "user", "content": "What are my chances of winning this case?"})
                    with st.spinner("Analyzing..."):
                        response = st.session_state.assistant.chat_about_case(
                            "What are my chances of winning this case?",
                            st.session_state.case_details,
                            st.session_state.chat_history
                        )
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()

            with col2:
                if st.button("Key arguments?"):
                    st.session_state.chat_history.append({"role": "user", "content": "What are the key arguments I should focus on?"})
                    with st.spinner("Analyzing..."):
                        response = st.session_state.assistant.chat_about_case(
                            "What are the key arguments I should focus on?",
                            st.session_state.case_details,
                            st.session_state.chat_history
                        )
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()

            with col3:
                if st.button("What to research?"):
                    st.session_state.chat_history.append({"role": "user", "content": "What areas should I research further?"})
                    with st.spinner("Analyzing..."):
                        response = st.session_state.assistant.chat_about_case(
                            "What areas should I research further?",
                            st.session_state.case_details,
                            st.session_state.chat_history
                        )
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()

            # Clear chat button
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()

if __name__ == "__main__":
    main()
