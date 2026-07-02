# AI Resume Reviewer

A Streamlit web app that compares your resume against a job description using Google Gemini AI. Upload a resume, paste a job posting, and get a structured analysis with a match score, skill gaps, and actionable improvement suggestions.

## Features

- **Resume upload** — Accepts PDF, DOCX, and DOC files via the UI
- **Job description input** — Paste the full job posting for comparison
- **Match score** — 0–100% fit rating with a visual progress bar
- **Skill analysis** — Lists matching skills and missing skills side by side
- **Strengths & weaknesses** — Highlights what works and what needs attention
- **Improvement suggestions** — Concrete recommendations to tailor your resume
- **Raw JSON view** — Expandable panel to inspect the full AI response

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | [Streamlit](https://streamlit.io/) |
| LLM | [Google Gemini](https://ai.google.dev/) (`gemini-2.5-flash`) |
| PDF parsing | [PyMuPDF](https://pymupdf.readthedocs.io/) |
| Config | [python-dotenv](https://github.com/theskumar/python-dotenv) |

## Project Structure

```
resume-reviewer/
├── app.py                  # Streamlit UI and analysis flow
├── styles.css              # Custom UI styling
├── requirements.txt        # Python dependencies
├── .env                    # API key (not committed — create locally)
├── uploads/                # Temporary resume storage (not committed)
├── services/
│   ├── pdf_parser.py       # Extracts text from PDF files
│   └── llm_service.py      # Sends resume + job description to Gemini
└── README.md
```

## Prerequisites

- Python 3.9+
- A [Google AI Studio](https://aistudio.google.com/) API key for Gemini

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ranavandana94/resume-reviewer.git
cd resume-reviewer
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

### 5. Create the uploads directory

```bash
mkdir -p uploads
```

## Usage

Start the app:

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

1. Upload your resume (PDF recommended — see note below)
2. Paste the job description into the text area
3. Click **Analyze Resume**
4. Review the match score, skills breakdown, strengths, weaknesses, and suggestions

## How It Works

1. **Upload** — The resume file is saved to `uploads/resume.pdf`.
2. **Extract** — `pdf_parser.py` uses PyMuPDF to pull plain text from the PDF.
3. **Analyze** — `llm_service.py` sends the resume text and job description to Gemini with a structured JSON prompt.
4. **Display** — `app.py` parses the JSON response and renders the results in the UI.

### AI Response Format

Gemini returns JSON with these fields:

```json
{
  "match_score": 75,
  "matching_skills": ["Python", "SQL"],
  "missing_skills": ["Kubernetes", "AWS"],
  "strengths": ["Strong backend experience"],
  "weaknesses": ["No cloud certifications listed"],
  "resume_improvements": ["Add AWS experience to the skills section"]
}
```

## File Format Note

The file uploader accepts PDF, DOCX, and DOC, but text extraction currently uses PyMuPDF and expects a **PDF**. For best results, upload a PDF resume. DOCX/DOC support would require an additional parser.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key |

## Dependencies

```
streamlit
google-generativeai
python-dotenv
PyMuPDF
pandas
```

## License

This project is open source. Use and modify it as needed.
