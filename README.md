ResearchPilot AI Agent:

ResearchPilot is an autonomous AI research assistant that collects information from multiple sources, generates structured research reports, and allows users to interact with the research using both text and voice queries.
The system integrates AI models, web search, Wikipedia data, and voice interaction to create an intelligent research environment.

 Features:

          Automated Research Collection
*Fetches research data from Wikipedia and web search results.

        AI-Generated Research Reports
*Uses a large language model to generate structured reports including:
Introduction
Applications
Challenges
Future Scope
Conclusion

           Interactive AI Chat Assistant
*Users can ask questions related to the generated research report.

            Voice Input Support
*Users can speak questions using the browser microphone.

             AI Voice Response
*Answers are converted into speech using Text-to-Speech.

              Download Research Report
*Generated reports can be downloaded as a text file.






Tech Stack

Frontend
  *Streamlit

Backend
   *Python

AI Model
   *Llama-3 via Groq

APIs & Libraries
       Wikipedia API
       DuckDuckGo Search
       gTTS (Text-to-Speech)
       LangDetect
        Dotenv





 System Architecture
User Input (Text / Voice)
        │
        ▼
Research Topic
        │
        ▼
Data Collection
(Wikipedia + Web Search)
        │
        ▼
AI Report Generation
(Llama-3 Model)
        │
        ▼
Research Report Display
        │
        ▼
User Chat with AI Agent
        │
        ▼
Voice Answer (Text-to-Speech)
