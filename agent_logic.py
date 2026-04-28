import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# --- Initialize Models ---

groq_llm = ChatGroq(
    model_name="llama-3.3-70b-versatile", 
    groq_api_key=os.getenv("GROQ_API_KEY")
)

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)

def analyze_resume(resume_text, jd_text):
    # Agent 1: The Data Analyst (Extraction)
    skill_prompt = f"""
    You are a Data Extraction Agent. Analyze the following:
    Resume: {resume_text}
    JD: {jd_text}
    Extract technical skills and calculate a weighted match score.
    Return ONLY a valid JSON: {{"matched_skills": [], "missing_skills": [], "match_percentage": 0}}
    """
    
    # Agent 2: The Career Strategist (Gap Analysis)
    recruiter_prompt = f"""
    You are an AI Career Strategist. Perform a deep-dive Gap Analysis.
    Resume: {resume_text}
    JD: {jd_text}
    
    Provide your analysis in Markdown:
    ###  Semantic Gap Analysis
    Explain *why* the candidate's current background (e.g., academic projects) creates a bridge or a gap to the role.
    
    ###  Strategic Pivot
    How can the candidate use their existing strengths (like their 9.4 CGPA or specific projects) to compensate for missing technical tools?
    
    ###  ATS Optimization
    Provide 3 high-impact bullet point rewrites to make the resume more visible to automated filters.
    """

    skill_analysis = groq_llm.invoke(skill_prompt)
    general_analysis = gemini_llm.invoke(recruiter_prompt)
    
    return skill_analysis.content, general_analysis.content
    
def generate_roadmap(missing_skills):
    if not missing_skills:
        return "You are ready for the role!"
    prompt = f"Create a 4-week roadmap for: with links {', '.join(missing_skills)}."
    roadmap = gemini_llm.invoke(prompt)
    return roadmap.content