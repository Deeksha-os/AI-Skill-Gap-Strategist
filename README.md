# AI Skill-Gap Strategist
### *Autonomous AI Agent for Intelligent Skill Gap Analysis & ATS Optimization*

---

##  Key Features

* **Agentic Orchestration:** Utilizes specialized AI agents for extraction and reasoning, ensuring high accuracy and reliability.
* **Intelligent Gap Analysis:** Moves beyond simple keyword matching to perform **Semantic Reasoning**—understanding *why* a gap exists and how to bridge it.
* **ATS Optimization Engine:** Provides high-impact, actionable tips to help resumes bypass automated filters.
* **4-Week 'Path to Hired' Roadmap:** Generates a structured, time-bound study plan to master missing competencies identified during the analysis.
* **Persistence Layer:** Built with Streamlit Session State to ensure a seamless user experience during data export (preventing app refreshes).
* **Professional PDF Export:** Generates a comprehensive intelligence report for offline mentoring or review.

---

##  Tech Stack & Architecture

This project follows a modular **Agentic Workflow** to ensure scalability and speed:

* **Orchestration Framework:** LangChain
* **Primary Reasoning Agent:** **Gemini 3.1 Flash-Lite** (Optimized for deep semantic analysis)
* **Extraction Agent:** **Llama 3.3-70B** (via Groq for sub-second JSON parsing)
* **Frontend:** Streamlit (Responsive Dashboard)
* **PDF Engine:** FPDF / ReportLab
* **Environment Management:** Python-Dotenv

---

## System Logic

1.  **Extraction:** `PyPDF2`  parses the raw text from the uploaded Resume.
2.  **Analyst Agent (Groq):** Processes the text to extract structured data regarding matched and missing skills with high precision.
3.  **Strategist Agent (Gemini):** Performs deep contextual analysis to provide strategic feedback and career "pivots."
4.  **Mentorship Agent (Gemini):** Cross-references missing skills to generate a tailored 4-week learning roadmap.

---

##  Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/AI-Skill-Gap-Strategist.git](https://github.com/your-username/AI-Skill-Gap-Strategist.git)
    cd AI-Skill-Gap-Strategist
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    GOOGLE_API_KEY=your_google_api_key_here
    ```

4.  **Launch the Application:**
    ```bash
    streamlit run app.py
    ```

---
