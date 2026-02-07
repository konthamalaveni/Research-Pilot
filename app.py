import streamlit as st
from groq import Groq
import wikipedia
from duckduckgo_search import DDGS
import os
from dotenv import load_dotenv
from gtts import gTTS
from langdetect import detect
import tempfile
import streamlit.components.v1 as components

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="ResearchPilot AI Agent", layout="wide")

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- SESSION STATE ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

if "report" not in st.session_state:
    st.session_state.report = ""

if "research_data" not in st.session_state:
    st.session_state.research_data = ""

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

# ---------------- FUNCTIONS ---------------- #

def collect_research_data(topic):
    try:
        wiki_data = wikipedia.summary(topic, sentences=5)
    except:
        wiki_data = "No Wikipedia data found."

    web_data = ""
    with DDGS() as ddgs:
        for r in ddgs.text(topic, max_results=5):
            web_data += r["body"] + "\n"

    return wiki_data + "\n" + web_data


def generate_report(data, topic):
    prompt = f"""
    Create a structured research report on {topic} with:
    Introduction, Applications, Challenges, Future Scope, Conclusion.
    {data}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def chat_with_agent(question):
    prompt = f"""
    You are ResearchPilot AI Agent.
    Research Report:
    {st.session_state.report}

    User Question: {question}
    Answer clearly and helpfully.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def speak_text_to_bytes(text):
    try:
        lang = detect(text)
    except:
        lang = "en"

    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        with open(fp.name, "rb") as f:
            audio_bytes = f.read()
    return audio_bytes


# ---------------- VOICE INPUT ---------------- #

voice_html = """
<script>
var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";

function startDictation() {
    recognition.start();
}

recognition.onresult = function(event) {
    let transcript = event.results[0][0].transcript;

    const inputs = window.parent.document.querySelectorAll('input[type="text"]');
    const lastInput = inputs[inputs.length - 1];

    lastInput.value = transcript;
    lastInput.dispatchEvent(new Event('change', { bubbles: true }));
};
</script>

<button onclick="startDictation()">🎤 Speak</button>
"""

# ---------------- UI ---------------- #

st.title("🧠 ResearchPilot AI Agent")
st.subheader("Autonomous Research Intelligence Hub")
st.divider()

topic = st.text_input("🔎 Enter your research topic")

if st.button("🔍 Start Research"):
    if topic:
        with st.spinner("Researching..."):
            st.session_state.research_data = collect_research_data(topic)
            st.session_state.report = generate_report(st.session_state.research_data, topic)
            st.session_state.messages = []
        st.success("Research Completed ✅")
    else:
        st.warning("Enter a topic")

# ---------------- REPORT ---------------- #

if st.session_state.report:
    st.subheader("📄 Research Report")
    st.write(st.session_state.report)
    st.download_button("📥 Download Report", st.session_state.report, f"{topic}.txt")

# ---------------- CHAT ---------------- #

st.subheader("💬 Ask Question by Voice or Text")

components.html(voice_html, height=60)

question = st.text_input("Voice / Typed Question", key="question_input")

send_clicked = st.button("Send")

if send_clicked and question.strip() != "":
    # save user message
    st.session_state.messages.append({"role": "user", "content": question})

    # get answer
    answer = chat_with_agent(question)

    # save assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # generate audio
    st.session_state.audio_bytes = speak_text_to_bytes(answer)

    # clear input
    st.session_state.question_input = ""

# ---------------- CHAT HISTORY ---------------- #

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- AUDIO OUTPUT ---------------- #

if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")
    st.success("🔊 Click Play to hear the answer")

# ---------------- CLEAR CHAT ---------------- #

if st.button("🧹 Clear Chat History"):
    st.session_state.messages = []
    st.session_state.audio_bytes = None
    st.rerun()
