# Searchie v1.0.0: The AI Research Orchestrator 🚀

We are thrilled to announce the first stable release of **Searchie**! 

Searchie is a sophisticated multi-agent pipeline designed to automate deep research. It orchestrates four specialized AI agents to search, extract, synthesize, and fact-check information, delivering highly accurate, verifiable Markdown reports in seconds.

## ✨ Key Features in v1.0.0
- **Multi-Agent Pipeline**: Seamlessly hands off data between Search, Extract, Synthesis, and Fact-check agents.
- **Zero-Hallucination Architecture**: Every claim in the final report is cross-verified against extracted raw data.
- **DigitalOcean AI Gateway Ready**: Fully integrated with DO AI Gateway (tested with `kimi-k2.6`) including a custom transport patch to handle strict JSON schema constraints.
- **Premium UI (Vite + React)**: A stunning, glassmorphism-inspired dark theme interface that looks professional and clean.
- **Real-Time Job Tracking**: Watch the AI agents work in real-time with our pipeline status indicator.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python), asyncio tasks, In-memory State Management (zero dependencies).
- **Frontend**: React, Vite, Vanilla CSS.

## 📦 How to run
Check out the exact setup instructions in the [README.md](./README.md).

*Made with ❤️ and 🤖 by Artsiom Beniash. Make the world a better place to live! <3*
