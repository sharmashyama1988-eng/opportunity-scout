# 🎯 Opportunity Scout (OpporTune CLI)
> **Autonomous Real-World Problem Discovery & Niche Engine**  
> *"Logo ke paas opportunity hoti hai, but pata nahi hota hai."*

Opportunity Scout is an enterprise-grade CLI application that takes your skills, background, geography, and unfair network advantages, and runs **live, multi-source investigative research** across Reddit, HackerNews, and DuckDuckGo to uncover **real-life, unsexy operational problems** with high willingness-to-pay.

If you have a technical background, it explicitly **bans low-margin freelancing** (Fiverr/Upwork gigs) and gives you **high-ticket B2B software & automation architectures** earning ₹1.5L - ₹4.5L / month recurring.

---

## ⚡ Key Highlights & Capabilities

- 🌐 **Language-First Universal Multilingual Engine**: Select your preferred language right at the start (supports 21 quick-select languages including English, Hinglish, Hindi, Spanish, French, German, Japanese, Mandarin, Arabic, Portuguese, etc., plus any world language). Dossiers, Mom Test scripts, and coaching are fully localized.
- 🧠 **Google Gemma 4 26B Powered**: Uses Google's frontier `google/gemma-4-26b-a4b-it:free` model with intelligent JSON preamble extraction and resilient multi-model cascade (`nemotron-3.5-lightning`, `nex-n2.5-pro`, `north-mini-code`).
- ⚡ **21-Vector Dynamic Algorithmic Engine**: Samples from 21 distinct industrial friction vectors (Demurrage detention, Highway diesel siphoning, Weighbridge fraud, Cold-chain spoilage, Ghost-worker muster verification, WhatsApp order ingestion, E-Waybill compliance, etc.). Every single run generates unique, high-margin opportunities with zero static repeats.
- 📂 **Universal Folder & Multi-Format Ingestion**: Drag & drop any single file (`.md`, `.txt`, `.pdf`, `.pptx`, `.xlsx`, `.csv`, `.docx`, code files like `.py`, `.js`, `.ts`, `.html`) **OR an entire folder**! The tool recursively scans and extracts your true skills and assets.
- 🚀 **20x Fast Async Concurrency**: Non-blocking asynchronous network pooling (`httpx` + `asyncio.gather`) across Reddit, HackerNews Algolia, and DuckDuckGo. Complete execution in 3–5 seconds.
- 🛡️ **Zero Guesswork Execution Directives**: Tells you **EXACTLY WHAT TO DO**:
  - Which industrial cluster/office to visit.
  - The exact job title to meet (e.g. *Dispatch Head, Plant Supervisor*).
  - Verbatim **The Mom Test** door-opener interview script.
  - **48-Hour Day 1-3 validation blueprint** (validating before writing code).
  - Exact pricing & monetization formula.
- ⚡ **Anti-Freelancing High-Ticket Tech Engine**: Developers are given enterprise architecture blueprints (Edge-to-Cloud Telemetry, Autonomous Reconciliation Pipelines) with monthly recurring revenue (MRR) ladders.
- 🏛️ **Classical UI Executive Dossiers**: Generates breathtaking HTML reports with Classical UI principles (Cinzel & Garamond typography, Slate/Obsidian palette, Golden Ratio balance), plus persistent Markdown and JSON exports.
- 🤖 **Model Context Protocol (MCP) Server**: Exposes tools for Claude Desktop and other autonomous AI agents to perform problem discovery and tech blueprint generation.
- 🔒 **Secure OpenRouter Integration**: Protected `.env` integration supporting verified free intelligence models with instant offline deterministic fallback.

---

## 🚀 Quick Start (Drag & Drop in 30 Seconds)

### 1. Configure Environment
Copy `.env.example` to `.env` and add your OpenRouter API key (free key available at [openrouter.ai](https://openrouter.ai/keys)):
```bash
cp .env.example .env
```

### 2. Launch Interactive CLI
```bash
python -m oppscout
```
*Or:*
```bash
python oppscout/cli.py
```

### 3. Select Your Language & Drag-and-Drop Profile
1. Choose your preferred language from the interactive menu (or pass `--language Hindi`).
2. Simply **drag and drop** your profile file (`.md`, `.txt`, `.pdf`, `.xlsx`, `.docx`, `.pptx`) **OR an entire folder** into the terminal and press Enter!

> 💡 **Demo Run:** Press `Enter` or type `sample` to immediately test with our built-in profile!

---

## 🛠️ CLI Options & Controls

| Command | Description |
|---|---|
| `python -m oppscout` | Interactive launcher with language menu and drag-and-drop prompt |
| `python -m oppscout path/to/profile.md` | Direct execution on target profile |
| `python -m oppscout -l Hindi` | Execute with specific output language (e.g., Hindi, English, Hinglish, Spanish) |
| `python -m oppscout --tech-only` | Force high-ticket B2B tech/SaaS opportunities |
| `python -m oppscout --domain "AgriTech"` | Focus on a specific industry or vertical |
| `python -m oppscout --location "Jaipur"` | Focus on a specific geographic market |
| `python -m oppscout --template` | Generates a fresh `templates/sample_profile.md` |
| `python -m oppscout --no-browser` | Disables auto-launch of the HTML report |
| `python -m oppscout --mcp` | Starts the Model Context Protocol (MCP) server |

---

## 🏛️ Structured Outputs Generated Per Run

All outputs are cleanly structured and saved automatically in `outputs/`:
- **`outputs/output_1.md`**: In-depth dossier for Top Opportunity #1.
- **`outputs/output_2.md`**: In-depth dossier for Top Opportunity #2.
- **`outputs/output_3.md`**: In-depth dossier for Top Opportunity #3.
- **`outputs/full_summary.md`**: Complete comparative analysis across all discovered opportunities.
- **`outputs/full_dossier.html`**: Standalone Classical UI executive dossier with scorecards, validation steps, and tech blueprints.
- **`outputs/dataset.json`**: Machine-readable structured JSON dataset.
- **`docs/architecture.html`**: Interactive Archify dataflow architecture diagram.

---

## 🧪 Testing

Run our verified unit test suite:
```bash
python run_tests.py
```

---

## 📄 User Playbook
For a detailed guide written in Hinglish & English on how to build your profile, how to interview customers, and how to execute the Day-1 validation blueprint, see [HOW_TO_USE.md](HOW_TO_USE.md).

