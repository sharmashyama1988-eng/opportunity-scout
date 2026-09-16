# 🎯 Opportunity Scout (OpporTune CLI)
> **Autonomous Real-World Problem Discovery & High-Conviction B2B Niche Engine**  
> *"Logo ke paas opportunity hoti hai, but pata nahi hota hai."*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini%202.5%20Flash-orange.svg)](https://aistudio.google.com/)
[![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter%20Cascade-purple.svg)](https://openrouter.ai/)
[![MCP Server](https://img.shields.io/badge/protocol-MCP%20Enabled-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Opportunity Scout is an enterprise-grade CLI application that analyzes your skills, professional background, geography, and unfair network advantages, and runs **live, multi-source investigative research** across DuckDuckGo, Reddit, and HackerNews to uncover **real-world, unsexy operational problems** with high willingness-to-pay.

If you have a technical background, it explicitly **bans low-margin freelancing** (Fiverr/Upwork gigs) and generates **high-ticket B2B software & automation architectures** earning ₹1.5L - ₹4.5L / month recurring.

---

## ⚡ Key Highlights & Architecture

- 🧠 **Google Gemini Native Engine & Elite System Prompt**:
  - Direct native API support for Google's official Gemini models (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`) with structured `responseMimeType: "application/json"`.
  - Backed by an **Elite System Prompt (`GEMINI_SYSTEM_PROMPT`)** enforcing founder grounding, anti-freelancing B2B tech rules, unsexy operational friction, The Mom Test opening scripts, and native language fidelity.
  - Multi-model OpenRouter fallback cascade (`nex-agi/nex-n2.5-pro:free`, `nvidia/nemotron-3.5-lightning:free`, `google/gemma-4-26b-a4b-it:free`, etc.) with defensive Pydantic schema normalization.

- 🔍 **Dynamic Profile-Driven Research Scraper**:
  - Automatically derives bespoke research queries from your profile's extracted **hard skills, target domains, geographic market, and unfair advantages**.
  - Dispatches concurrent asynchronous search queries to DuckDuckGo (`ddgs`), Reddit operator communities (`r/smallbusiness`, `r/sysadmin`, `r/devops`), and HackerNews Algolia.
  - Zero hardcoded queries: a systems/hardware founder gets queries on socket leaks and edge hardware telemetry, while a logistics founder gets queries on weighbridge fraud and E-Waybill penalties.

- 🛡️ **Zero-Repeat Domain-Isolated Opportunity Vectors**:
  - Fully dynamic multi-vector synthesizer with domain isolation:
    - **Systems / Desktop / Hardware / AI Founders:** Industrial Edge Microcontroller Telemetry & Silent Failure Sentinel, Autonomous Multi-Agent Reconciliation Pipelines, Desktop Multi-GB Asset Sync Accelerators, Enterprise Bandwidth Abuse & Socket Telemetry Guardians.
    - **Logistics & Fleet Operators:** 24-Hour E-Waybill Detention Guardians, Highway Diesel Siphoning Audits, Port & Customs Demurrage Avoidance, Perishable Cold-Chain Spoilage Shields.
    - **Manufacturing & Industrial Plants:** Batch-to-Batch Color & Dimension Rejection Shields, Machine Breakdown Vibration Sentinels, Scrap Metal Tare Manipulation Detectors.
    - **Wholesale & Distribution:** WhatsApp Group Order Ingestion & ERP Bridges, Disputed Challan & Khata Credit Lock Systems.

- 🌐 **Language-First Universal Multilingual Engine**:
  - Select your preferred language at launch (supports 21 quick-select languages including **English, Hinglish, Hindi, Spanish, French, German, Japanese, Mandarin, Arabic, Portuguese**, and freeform input for any world language).
  - Dossiers, problem statements, customer avatars, Mom Test scripts, and coaching advice are rendered in native, fluent prose.

- 📂 **Universal Folder & Multi-Format Ingestion**:
  - Drag and drop any single file (`.md`, `.txt`, `.pdf`, `.pptx`, `.xlsx`, `.csv`, `.docx`, code files like `.py`, `.go`, `.cpp`, `.js`, `.ts`) **OR an entire folder**!
  - The recursive parser scans directories, traverses document pages, and extracts complete skill trees (languages, frameworks, systems utilities, domain protocols).

- 🛡️ **Zero-Guesswork Execution Directives**:
  - **Where to go:** Exact local industrial cluster, agency, or office corridor.
  - **Who to meet:** Specific customer persona with purchasing power (e.g. *Plant Maintenance Head, Dispatch Supervisor, IT Director*).
  - **The Mom Test Script:** Word-for-word door-opener interview question (no sales pitches).
  - **48-Hour Day 1-3 Blueprint:** Step-by-step validation without building heavy software upfront.
  - **Lean Tech Stack:** Automatically constructed from the founder's verified hard skills.
  - **Monetization Ladder:** Upfront pilot pricing and recurring retainers/subscriptions.

- 🏛️ **Classical UI Executive Dossiers**:
  - Produces standalone HTML executive dossiers following Classical UI design principles (Golden Ratio phi=1.618 balance, Cinzel & Garamond typography, Slate/Obsidian palette, responsive scorecards).
  - Automatically generates granular Markdown files and machine-readable JSON datasets.

- 🤖 **Model Context Protocol (MCP) Server**:
  - Native MCP server support (`python -m oppscout --mcp`) exposing tools for Claude Desktop and agentic systems to run automated market research and high-ticket B2B synthesis.

---

## 🚀 Quick Start (Drag & Drop in 30 Seconds)

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/sharmashyama1988-eng/opportunity-scout.git
cd opportunity-scout
pip install -r requirements.txt
```

### 2. Configure Environment (`.env`)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` to configure your API keys:
```ini
# Primary: Google Gemini Native API (100% Free at https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Fallback: OpenRouter API (Free keys at https://openrouter.ai/keys)
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=nex-agi/nex-n2.5-pro:free
```
*(Note: If no API keys are configured, Opportunity Scout seamlessly falls back to its deterministic 21-vector domain synthesis engine with zero downtime).*

### 3. Launch the Interactive CLI
```bash
python -m oppscout
```

### 4. Run Discovery Pipeline
1. Select your preferred language (e.g. `1` for English, `2` for Hinglish, `3` for Hindi, or type your language).
2. Drag and drop your profile file (`profile.md`, `.pdf`, `.docx`, etc.) or folder into the terminal and press Enter.
3. Opportunity Scout will scan your leverage, mine real-world operator complaints, and generate 3 bespoke dossiers in seconds.

---

## 🛠️ CLI Options & Command Reference

| Command | Description |
|---|---|
| `python -m oppscout` | Interactive launcher with language menu and drag-and-drop ingestion |
| `python -m oppscout path/to/profile.md` | Direct execution on a target profile or folder |
| `python -m oppscout -l Hinglish profile.md` | Execute with preferred language (e.g. `English`, `Hinglish`, `Hindi`, `Spanish`) |
| `python -m oppscout --tech-only profile.md` | Force high-ticket B2B tech/SaaS opportunities only (bans freelancing) |
| `python -m oppscout --domain "Network Infrastructure"` | Override or narrow domain focus |
| `python -m oppscout --location "Jaipur"` | Override geographic location / regional cluster |
| `python -m oppscout --deep profile.md` | Run hyper-deep research mode across all 20+ specialized algorithms |
| `python -m oppscout --non-interactive profile.md` | Direct run without entering post-analysis coaching loop |
| `python -m oppscout --no-browser profile.md` | Disables automatic browser launch of HTML executive dossier |
| `python -m oppscout --template` | Generates a fresh `templates/sample_profile.md` template |
| `python -m oppscout --mcp` | Runs as a Model Context Protocol (MCP) server for AI agents |

---

## 🏛️ Structured Outputs Generated Per Run

Every discovery run writes timestamped deliverables into the `outputs/` directory:

| Deliverable | Format | Description |
|---|---|---|
| `outputs/output_1.md` | Markdown | Deep-dive dossier for Top Opportunity #1 (Problem, Customer, Mom Test, Tech Stack, Validation) |
| `outputs/output_2.md` | Markdown | Deep-dive dossier for Top Opportunity #2 |
| `outputs/output_3.md` | Markdown | Deep-dive dossier for Top Opportunity #3 |
| `outputs/full_summary.md` | Markdown | Complete executive overview comparing all 3 opportunities and score matrices |
| `outputs/full_dossier.html` | Classical HTML | Breathtaking, standalone executive dashboard with 5-Factor scorecards and print-ready styles |
| `outputs/dataset.json` | JSON | Fully typed, machine-readable JSON dataset conforming to Pydantic schemas |

---

## 🧠 Sample 5-Factor Opportunity Scoring Matrix

Every opportunity is scored on a rigorous 100-point composite matrix:

$$\text{Composite Score} = (\text{Pain} \times 3.0) + (\text{WTP} \times 2.5) + (\text{Founder Fit} \times 2.5) + (\text{Whitespace} \times 1.0) + (\text{Feasibility} \times 1.0)$$

- **Pain Intensity (1–10):** Measures financial bleeding, legal detention, or operational paralysis.
- **Willingness to Pay (1–10):** Urgency of business operators to cut checks immediately.
- **Founder-Problem Fit (1–10):** Alignment with the founder's verified hard skills and unfair network access.
- **Whitespace (1–10):** Freedom from crowded consumer SaaS competition in unsexy B2B niches.
- **Day-1 Feasibility (1–10):** Ability to validate with customer interviews in 48 hours without writing heavy code.

---

## 🧪 Testing & Verification

Run the comprehensive unit and integration test suite:
```bash
python run_tests.py
```

Tests verify:
1. Terminal path cleaning and drag-and-drop artifacts.
2. Multi-skill extraction and technical leverage parsing.
3. Universal folder and multi-document ingestion.
4. High-ticket B2B architecture and anti-freelancing directives.
5. Algorithmic opportunity scoring and Pydantic validation.
6. Universal language normalization and multilingual dictionaries.
7. Multilingual Markdown and Classical HTML dossier generation.

---

## 📄 Documentation & Playbook

- **Founder Playbook & Customer Discovery Guide:** See [HOW_TO_USE.md](HOW_TO_USE.md) for a comprehensive guide on crafting your profile, executing The Mom Test interviews, and closing paid pilots in 48 hours.
- **System Architecture & Dataflow:** See [docs/architecture.html](docs/architecture.html) for an interactive system diagram.

---

## 📜 License
MIT License. Built for builders, systems engineers, and pragmatic founders.

