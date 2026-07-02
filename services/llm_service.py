import google.generativeai as genai
import os


from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.5-flash")



def analyze_resume(resume, job_description):
    prompt = f"""
    You are a resume analyzer. You are given a resume and a job description. You need to analyze the resume and compare it to the job description.
    
    The resume is: {resume}
    The job description is: {job_description}

    Return the resume analysis in JSON format only.

    {{
        "match_score":"number between 0 and 100",
        "matching_skills":[],
        "missing_skills":[],
        "strengths":[],
        "weaknesses":[],
        "resume_improvements":["list of improvements to the resume"]
    }}

    """
    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown code blocks
    if text.startswith("```json"):
       text = text.replace("```json", "")

    if text.startswith("```"):
        text = text.replace("```", "")

    text = text.replace("```", "").strip()

    return text  