import PyPDF2
import re
from fpdf import FPDF

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def clean_json_string(text):
    match = re.search(r'```json?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def clean_markdown(text):
    if not text:
        return ""
    # Removes bold (**) and headers (##)
    text = text.replace("**", "").replace("##", "")
    # Removes bullet points (*) at the start of lines and replaces with a cleaner dash
    text = re.sub(r'^\s*[\*\-]\s+', '- ', text, flags=re.MULTILINE)
    # Ensure characters are compatible with FPDF (Latin-1)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def create_pdf_report(score, matched, missing, feedback):
    """
    Creates a professional PDF report. 
    To include the roadmap, ensure it is appended to the 'feedback' string 
    before calling this function.
    """
    clean_feedback = clean_markdown(feedback)
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- 1. REPORT HEADER ---
    pdf.set_fill_color(31, 41, 55) 
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_y(15)
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "RESUME INTELLIGENCE REPORT", ln=True, align='C')
    
    # --- 2. SCORE BANNER ---
    pdf.ln(25)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 102, 204) 
    pdf.cell(0, 10, f"ATS Compatibility Score: {score}%", ln=True, align='L')
    pdf.set_draw_color(0, 102, 204)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) 
    
    # --- 3. SKILLS ANALYSIS SECTION ---
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "Skill Gap Analysis", ln=True)
    
    # Matched Skills
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(34, 139, 34) 
    pdf.cell(0, 8, "Matched Competencies:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 7, ", ".join(matched) if matched else "No direct matches found.")
    
    # Missing Skills
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(200, 0, 0) 
    pdf.cell(0, 8, "Identified Gaps:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 7, ", ".join(missing) if missing else "Candidate meets all requirements.")
    
    # --- 4. STRATEGIC INSIGHTS & ROADMAP ---
    pdf.ln(10)
    pdf.set_fill_color(245, 245, 245) 
    pdf.set_font("Arial", 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Detailed Analysis & Roadmap", ln=True, fill=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", '', 11)
    # This will automatically flow onto Page 2 if the roadmap is long
    pdf.multi_cell(0, 7, clean_feedback)
    
    # --- 5. FOOTER (Branding) ---
    # We add this at the end of the content
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(150, 150, 150)
   
    report_path = "Resume_Analysis_Report.pdf"
    pdf.output(report_path)
    return report_path