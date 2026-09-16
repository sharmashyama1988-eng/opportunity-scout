# 🎯 Opportunity Scout: User Manual & Execution Playbook
*“Logo ke paas opportunity hoti hai, but pata nahi hota hai. Ye tool aapko exact real-life problem aur karne ka step-by-step tarika batayega.”*

---

## ⚡ Quick Start in 30 Seconds (The Drag & Drop Way)

### Step 1: Open Your Terminal & Run
```bash
python -m oppscout
```

### Step 2: Choose Your Language FIRST / अपनी भाषा चुनें (Universal Multilingual)
CLI start hote hi sabse pehle aapse **aapki man-pasand bhasha** puchega:
```text
🌐 STEP 1: CHOOSE YOUR PREFERRED LANGUAGE / अपनी भाषा चुनें
[1] English (Global)    [2] Hinglish (Practical)   [3] हिन्दी (Hindi)
[4] Español (Spanish)   [5] Français (French)      [6] Deutsch (German)
... ya duniya ki koi bhi bhasha direct type kar sakte hain!
```
- Bas number enter karein (e.g., `2` for Hinglish, `3` for Hindi) ya direct naam likhein (e.g. `Spanish`, `Marathi`, `Russian`, `Italian`, `Korean`, etc.).
- Default ke liye bas **Enter** press karein!
- Saara analysis, individual `output_1.md`, `output_2.md`, `output_3.md`, Mom Test scripts aur HTML report usi bhasha mein banega!

### Step 3: Drag & Drop File ya Pura Ka Pura Folder
Language select hone ke baad CLI aapse path mangega:
```text
Drag & Drop file/folder here (or enter path) [sample]:
```
1. **Single File:** `.md`, `.txt`, `.pdf`, `.xlsx`, `.docx`, `.pptx`, code files.
2. **Or ENTIRE FOLDER:** Saare documents, sheets aur notes ek folder mein daal ke pura folder path drag & drop kar dein! Tool recursive scan karke sab data auto-ingest kar lega.
3. 💡 **Demo run karna hai?** Bas bina kuch likhe **Enter** daba do ya `sample` likh do!

### Step 4: Sit Back — Everything Else is 100% Automated!
Tool khud-b-khud:
1. Aapki unique skills, geography, aur **unfair network advantages** ko extract karega.
2. 20+ Specialized Algorithms se **Reddit, Hacker News, aur DuckDuckGo** par live unsexy problems aur complaints ko deep-scrape karega.
3. 5-Factor Scoring Matrix se evaluate karega.
4. Structured Output folder (`outputs/`) mein `output_1.md`, `output_2.md`, `output_3.md`, `full_summary.md`, aur `full_dossier.html` create karega!

---

## 📝 Apni Profile Markdown (`.md`) File Kaise Banayein?

Aapko koi complex format follow karne ki zaroorat nahi hai. Ek normal `.md` file banayein (jaise `my_profile.md`) aur khulkar likhein:

```markdown
# Mera Profile & Background

## Mere Baare Mein
Mera naam Rahul hai, main Jaipur (Rajasthan) mein rehta hoon.
Main ek full-stack developer hoon, but mujhe generic SaaS nahi banana. Mujhe real grounded business khada karna hai.

## Hard Skills (Jo kaam mujhe aate hain)
- Python, FastAPI, PostgreSQL, Next.js
- Workflow automation, Excel & Tally data parsing
- Basic IoT & Hardware (ESP32 microcontrollers)

## Domain & Interests (Kis sector mein ruchi hai)
- Logistics & Inter-state Trucking
- Stone & Marble Cutting Factories (Kishangarh & Makrana belt)
- Wholesale Mandis & B2B Distribution

## Mera Location & Foothold
- Jaipur & Western India Trade Belt

## Mere Unfair Advantages & Network (Sabse Important!)
- Mere uncle ke paas 45 inter-state freight trucks ka fleet hai.
- Mera school friend Kishangarh mein marble cutting unit chalata hai.
- Main directly transport nagar jaakar fleet managers aur dispatchers se mil sakta hoon.

## Budget & Time
- Budget: Bootstrapped (₹50,000)
- Time: 30-40 hours per week
```

> 🎯 **Pro-Tip:** Jitna zyaada aap apne **Unfair Network Advantages** (family business, dost ki factory, relative ka hospital/shop, local contacts) ke baare mein likhenge, tool utni hi zyada powerful aur proprietary opportunity nikaal kar dega jo **kisi aur ke paas nahi ho sakti!**

---

## 🧠 Tool Aapko Kya-Kya Deta Hai? (Zero Guesswork)

Aapko dobara kisi se puchna nahi padega ki *"ab main kya karun?"*. Tool aapko har opportunity ke liye **exact operational blueprint** deta hai:

1. **The Bleeding-Neck Problem (Asli Dard):**
   - Generic ideas nahi (No AI chatbots, No generic CRM).
   - Real operational friction jaise: *Diesel theft, 24-hour E-Waybill seizure penalties, batch color rejection in marble manufacturing, uncollected B2B delivery challans.*

2. **Target Customer Persona (Kisko Milna Hai):**
   - Exact job title aur location (e.g. *Dispatch Head in Transport Nagar, Jaipur*).

3. **The Mom Test Door-Opener Script (Pehla Sawal Kya Puchna Hai):**
   - Salesman ki tarah pitch nahi karna.
   - Exact question jo owner ke real dard ko bahar nikaal de (e.g., *"Sir, pichle mahine highway checkpost par E-Waybill expire hone par kitna fine bharna pada tha?"*).

4. **Day 1 to Day 3 Validation Blueprint (48-Hour Plan):**
   - **Day 1:** Physical meeting aur live records inspection (unke raw slips/photos dekhna).
   - **Day 2:** 1-page Python script ya manual concierge demonstration se unko unka bacha hua paisa dikhana.
   - **Day 3:** Code likhne se pehle ₹5,000 se ₹20,000 ka advance/pre-order lena.

5. **Monetization & Pricing Formula:**
   - Kitna charge karna hai (e.g. *₹499/truck/month* ya *15% recovery fee*).

6. **Lean Tech Stack:**
   - Aapke hard skills ke hisab se exact recommended tools (e.g. *Python + WhatsApp Business API + Supabase*).

---

## 📂 Output Deliverables (Kahan Save Hota Hai?)

Har run ke baad saare reports `outputs/` folder mein automatically save hote hain:

1. **`outputs/opportunity_dossier_<timestamp>.html`**
   - Ek Classical Editorial UI styled report (Cinzel / Garamond typography, responsive, printable, Golden-ratio layout).
   - Run hote hi aapke default browser mein automatic open ho jaati hai!
2. **`outputs/opportunity_dossier_<timestamp>.md`**
   - Complete markdown dossier jise aap Notion, Obsidian ya GitHub par rakh sakte hain.
3. **`outputs/opportunity_data_<timestamp>.json`**
   - Raw JSON data for programmatic integrations.

---

## ⚙️ OpenRouter API & Settings Configuration

Tool ke andar OpenRouter API integrated hai jo `.env` file se secure tarike se load hoti hai:

```env
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=nvidia/nemotron-3.5-lightning:free
```

- **100% Secure:** Key `.env` mein rehti hai aur `.gitignore` se protected hai.
- **Ultra Low-Cost / Free:** OpenRouter ke verified high-reasoning free models (`nvidia/nemotron-3.5-lightning:free`, `inclusionai/ling-3.0-flash-vl:free`) use hote hain.
- **Zero-Key Fallback:** Agar internet down ho ya API key na ho, tab bhi hamara **Deterministic Algorithmic Engine** offline kaam karega aur aapka tool kabhi crash nahi hoga!

---

## 🤖 MCP (Model Context Protocol) Server Mode

Agar aap is tool ko Claude Desktop ya kisi doosre AI agent ke sath connect karna chahte hain:
```bash
python -m oppscout.cli --mcp
```
Ye FastMCP server start kar deta hai jisme tools available hain:
- `discover_opportunities_from_markdown(markdown_content)`
- `research_domain_pain_points(domain, location)`

---

## 🚀 Commands Reference Summary

| Command | Description |
|---|---|
| `python -m oppscout.cli` | Interactive launcher (drag & drop prompt) |
| `python -m oppscout.cli path/to/profile.md` | Direct file execution |
| `python -m oppscout.cli --template` | Generates a fresh `templates/sample_profile.md` |
| `python -m oppscout.cli --no-browser` | Runs without opening the browser automatically |
| `python -m oppscout.cli --mcp` | Starts the Model Context Protocol (MCP) server |
