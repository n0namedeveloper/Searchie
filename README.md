<div align="center">
  <img src="./assets/logo.png" alt="Searchie" width="100" />
  <h1>Searchie</h1>
  <p><strong>Research anything, verified by AI.</strong></p>
  <p>Searchie orchestrates four specialized agents to search, extract, synthesize, and fact-check — delivering trustworthy research reports in seconds.</p>
</div>

---

## Overview

Searchie is a sophisticated multi-agent system designed to automate deep research. Unlike standard conversational AI, Searchie doesn't just answer questions; it conducts thorough, verifiable research. 

It breaks down complex queries, browses the internet, extracts factual data, synthesizes comprehensive reports, and finally, self-verifies every claim made to ensure zero hallucinations.

![Searchie Homepage](https://raw.githubusercontent.com/nonameoff/Searchie/main/assets/homepage.png)
*(Homepage - Clean, distraction-free interface for initiating research jobs)*

## The Pipeline

Searchie employs a 4-step autonomous pipeline:

1. **Search Agent**: Deconstructs your topic into precise queries, scours the web, and compiles raw source material.
2. **Extract Agent**: Parses the raw data to extract concrete, verifiable facts and citations.
3. **Synthesis Agent**: Weaves the extracted facts into a coherent, highly structured Markdown report.
4. **Fact-Check Agent**: Reviews the final report against the extracted facts, assigning confidence scores and verifying every single claim.

![Searchie Final Report](https://raw.githubusercontent.com/nonameoff/Searchie/main/assets/report.png)
*(Job Detail - Live pipeline status tracking and final fact-checked markdown report)*

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite + Vanilla CSS
- **AI Gateway**: DigitalOcean AI Gateway (Patched for compatibility)
- **Models**: `kimi-k2.6` (via DO AI Gateway)

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Searchie.git
cd Searchie

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure Environment Variables
cp .env.example .env
# Edit .env with your DigitalOcean AI Gateway Key and Base URL

# 4. Start the FastAPI server
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

### Frontend Setup

```bash
# 1. Navigate to the web directory
cd web

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev -- --port 5174
```

Visit `http://localhost:5174` in your browser to start researching.

## Project Structure

```
Searchie/
├── app/
│   ├── agents/         # AI Agents (Search, Extract, Synthesis, Fact-check)
│   ├── main.py         # FastAPI application and pipeline orchestrator
│   ├── schemas.py      # Pydantic data models
│   ├── state.py        # In-memory State Management
│   └── do_patch.py     # Transport patch for DO AI Gateway strict/response_format
├── web/
│   ├── src/            # React Frontend
│   │   ├── components/ # Layout, Pipeline status, Badges
│   │   ├── pages/      # Home, JobDetail
│   │   └── index.css   # Core Design System (Glassmorphism, Teal Accents)
│   └── vite.config.js
└── e2e.py              # CLI End-to-End Test Script
```

## License

MIT License. See `LICENSE` for more information.

---

*Made with ❤️ and 🤖 by Artsiom Beniash. Make the world a better place to live! <3*
