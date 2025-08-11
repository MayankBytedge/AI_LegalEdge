# Legal Case Assistant 🏛️⚖️

A powerful Streamlit application that uses Google's Gemini AI to analyze legal cases, provide insights, and offer conversational assistance for legal research.

## Features ✨

- **📄 PDF Case Upload**: Upload and analyze legal case documents
- **🔍 Intelligent Case Analysis**: Extract key details using AI
- **📚 Similar Case Finding**: Discover relevant precedents and case law
- **📊 Case Strength Assessment**: Get probability estimates and recommendations
- **💬 Conversational Interface**: Chat about your case with an AI legal assistant
- **🎯 Strategic Recommendations**: Receive actionable legal advice
- **🔬 Research Suggestions**: Get guidance on areas to investigate further

## Quick Start 🚀

### 1. Get Your Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key for later use

### 2. Install Dependencies
```bash
pip install streamlit google-generativeai PyPDF2 requests python-dotenv pandas numpy
```

Or using the requirements file:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Use the App
1. Enter your Gemini API key in the sidebar
2. Upload a legal case PDF
3. Click "Analyze Case" to get insights
4. Use the chat interface to ask questions

## Sample Cases 📁

The `sample_cases/` directory contains 5 sample legal cases covering different areas of law:

1. **Criminal Law**: Handcuffing violation case
2. **Civil Law**: Land acquisition dispute
3. **Constitutional Law**: Right to education PIL
4. **Service Law**: Premature retirement challenge
5. **NDPS Law**: Bail application

You can convert these text files to PDFs and test them with the app.

## Project Structure 📂

```
legal-case-assistant/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.template                   # Environment variables template
├── README.md                       # This file
└── sample_cases/                   # Sample legal cases for testing
    ├── criminal_handcuffing_case.txt
    ├── civil_land_acquisition_case.txt
    ├── constitutional_education_case.txt
    ├── service_matter_case.txt
    └── ndps_bail_case.txt
```

## Key Capabilities 🎯

### Case Analysis
- **Automatic Information Extraction**: Case title, court, issues, statutes
- **Legal Classification**: Criminal, civil, constitutional categorization
- **Key Facts Identification**: Important factual elements
- **Relief Assessment**: Understanding of requested remedies

### Similar Case Discovery
- **Precedent Finding**: Relevant landmark cases
- **Legal Principle Matching**: Cases with similar legal issues
- **Jurisdiction Awareness**: Supreme Court and High Court cases
- **Context-Aware Search**: Matches based on facts and legal issues

### Strategic Insights
- **Strength Assessment**: 1-10 scale case evaluation
- **Success Probability**: Percentage chance estimates with reasoning
- **Weakness Identification**: Areas that need strengthening
- **Improvement Suggestions**: Actionable recommendations

### Conversational Intelligence
- **Context Awareness**: Remembers case details throughout conversation
- **Legal Expertise**: Provides responses based on Indian legal principles
- **Citation Support**: References to relevant statutes and cases
- **Professional Disclaimers**: Appropriate legal advice warnings

## Usage Examples 💡

### Upload and Analyze
1. Upload a PDF containing a legal case
2. Wait for automatic analysis
3. Review extracted case details
4. Examine similar cases found
5. Study the comprehensive legal analysis

### Ask Strategic Questions
- "What are my strongest arguments?"
- "What precedents support my case?"
- "Where should I focus my research?"
- "What are the main weaknesses in my position?"
- "How can I improve my chances of success?"

### Quick Analysis Buttons
- **Chances Assessment**: Get probability estimates
- **Key Arguments**: Focus areas for legal strategy
- **Research Areas**: Topics for further investigation

## Technical Details 🔧

### AI Model
- **Google Gemini 1.5 Pro**: Latest large language model
- **Context Window**: Handles large legal documents
- **Indian Law Focus**: Trained on diverse legal content

### Features
- **PDF Text Extraction**: Robust document processing
- **JSON Parsing**: Structured information extraction
- **Chat Memory**: Maintains conversation context
- **Error Handling**: Graceful failure management

## Limitations & Disclaimers ⚠️

### Important Legal Disclaimers
- **Not Legal Advice**: This tool provides AI-generated analysis for informational purposes only
- **Professional Consultation Required**: Always consult qualified legal professionals
- **Accuracy Not Guaranteed**: AI analysis may contain errors or omissions
- **Jurisdiction Specific**: Focused on Indian legal system

### Technical Limitations
- **PDF Quality Dependent**: Text extraction quality varies with document quality
- **API Rate Limits**: Gemini API has usage limitations
- **Internet Required**: Needs active internet connection
- **Token Limits**: Very large documents may be truncated

## Troubleshooting 🔧

### Common Issues

1. **"Please enter your Gemini API key"**
   - Get a key from Google AI Studio
   - Enter it in the sidebar

2. **"Error reading PDF"**
   - Ensure PDF is not password protected
   - Try a different PDF file
   - Check file size (under 10MB recommended)

3. **"API request failed"**
   - Check internet connection
   - Verify API key is correct
   - Wait and try again (rate limiting)

### Performance Tips
- Use clear, well-formatted PDF documents
- Avoid very large files (>10MB)
- Break down complex questions into simpler ones
- Clear chat history periodically for better performance

## Contributing 🤝

We welcome contributions! Areas for improvement:
- Additional legal document formats
- Enhanced case law database integration
- Better Indian legal terminology handling
- Performance optimizations
- UI/UX improvements

## License 📄

This project is for educational and research purposes. Please ensure compliance with:
- Google AI terms of service
- Local legal practice regulations
- Professional legal ethics

## Support 💬

For issues or questions:
1. Check the troubleshooting section
2. Review Google AI Studio documentation
3. Ensure all requirements are properly installed

---

**Remember**: This tool is designed to assist legal research and analysis, but it cannot replace professional legal judgment and advice. Always consult with qualified legal professionals for important legal matters.
