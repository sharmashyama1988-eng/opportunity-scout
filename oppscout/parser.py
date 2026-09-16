"""Universal Omnivore Ingestion Engine for Opportunity Scout.
Recursively scans and extracts deep intelligence from entire folders or single files:
- Code files (.py, .js, .ts, .tsx, .html, .css, .json, .sql, .rs, .go, .java, .cpp, .yaml)
- Spreadsheets (.xlsx, .xls, .csv)
- Presentations (.pptx, .potx)
- Documents (.pdf, .docx)
- Text & Notes (.md, .txt, .log, .rst)
- Hyperlinks & URLs discovered inside files
"""

import csv
import json
import logging
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Set, Tuple
from oppscout.models import UserProfile

logger = logging.getLogger("oppscout.parser")


def clean_file_path(raw_input: str) -> Path:
    """Cleans up paths pasted or dragged-and-dropped into the Windows terminal.
    Handles quotes, PowerShell `& '...'` artifacts, and surrounding whitespace.
    """
    clean = raw_input.strip()

    if clean.startswith("&"):
        clean = clean[1:].strip()

    clean = clean.strip('"').strip("'").strip()

    if clean.startswith("file:///"):
        clean = clean.replace("file:///", "")

    return Path(clean)


def extract_text_from_pdf(file_path: Path) -> str:
    """Extracts text from PDF documents using pypdf."""
    text_chunks = []
    try:
        import pypdf
        reader = pypdf.PdfReader(str(file_path))
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(f"[Page {page_num+1}]\n{page_text}")
    except Exception as e:
        logger.warning(f"Error reading PDF {file_path}: {e}")
    return "\n\n".join(text_chunks)


def extract_text_from_pptx(file_path: Path) -> str:
    """Zero-dependency PowerPoint (.pptx, .potx) slide and bullet extractor using zipfile & XML."""
    text_chunks = []
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            slide_files = [f for f in z.namelist() if f.startswith("ppt/slides/slide") and f.endswith(".xml")]
            # Sort slides naturally slide1.xml, slide2.xml ...
            slide_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

            for idx, slide_name in enumerate(slide_files, 1):
                xml_data = z.read(slide_name)
                root = ET.fromstring(xml_data)
                # Find all text elements <a:t>
                slide_texts = [elem.text.strip() for elem in root.iter() if elem.tag.endswith("}t") and elem.text and elem.text.strip()]
                if slide_texts:
                    text_chunks.append(f"[Slide {idx}]\n" + "\n".join([f"• {t}" for t in slide_texts]))
    except Exception as e:
        logger.warning(f"Error reading PPTX {file_path}: {e}")
    return "\n\n".join(text_chunks)


def extract_text_from_excel(file_path: Path) -> str:
    """Extracts text from Excel spreadsheets (.xlsx, .xls) using openpyxl."""
    text_chunks = []
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(file_path), data_only=True)
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            text_chunks.append(f"--- Sheet: {sheet_name} ---")
            for row in sheet.iter_rows(values_only=True):
                row_vals = [str(v).strip() for v in row if v is not None and str(v).strip()]
                if row_vals:
                    text_chunks.append(" | ".join(row_vals))
    except Exception as e:
        logger.warning(f"Error reading Excel {file_path}: {e}")
    return "\n".join(text_chunks)


def extract_text_from_csv(file_path: Path) -> str:
    """Extracts text from CSV files."""
    text_chunks = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            for row in reader:
                vals = [c.strip() for c in row if c.strip()]
                if vals:
                    text_chunks.append(" | ".join(vals))
    except Exception as e:
        logger.warning(f"Error reading CSV {file_path}: {e}")
    return "\n".join(text_chunks)


def extract_text_from_docx(file_path: Path) -> str:
    """Extracts text from Word documents (.docx) using python-docx."""
    text_chunks = []
    try:
        import docx
        doc = docx.Document(str(file_path))
        for p in doc.paragraphs:
            if p.text.strip():
                text_chunks.append(p.text.strip())
        for table in doc.tables:
            for row in table.rows:
                vals = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if vals:
                    text_chunks.append(" | ".join(vals))
    except Exception as e:
        logger.warning(f"Error reading DOCX {file_path}: {e}")
    return "\n".join(text_chunks)


def extract_text_from_code(file_path: Path) -> str:
    """Analyzes source code files (.py, .js, .ts, .html, .sql, etc.)
    and extracts tech stack cues, imported libraries, function signatures, and docstrings.
    """
    try:
        raw_code = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

    lines = raw_code.splitlines()
    detected_meta = [f"File: {file_path.name} ({file_path.suffix.upper()} source code, {len(lines)} lines)"]

    # Extract imports / dependencies
    imports = []
    for line in lines[:80]:
        line_clean = line.strip()
        if re.match(r'^(import |from |require\(|import \{)', line_clean):
            imports.append(line_clean)

    if imports:
        detected_meta.append("Imports / Dependencies:\n" + "\n".join(imports[:15]))

    # Extract docstrings, comments and functions
    docstrings = re.findall(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'|/\*(.*?)\*/', raw_code, re.DOTALL)
    if docstrings:
        flat_docs = [" ".join(d).strip() for d in docstrings if any(d)]
        if flat_docs:
            detected_meta.append("Docstrings & Context:\n" + "\n".join(flat_docs[:5]))

    # Add code excerpt (first 50 lines)
    code_snippet = "\n".join(lines[:60])
    detected_meta.append(f"Code Excerpt:\n{code_snippet}")

    return "\n\n".join(detected_meta)


def extract_text_from_file(file_path: Path) -> str:
    """Intelligently parses any recognized document or code file."""
    ext = file_path.suffix.lower()

    # Code formats
    code_extensions = {
        ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".htm", ".css",
        ".sql", ".rs", ".go", ".java", ".cpp", ".c", ".h", ".sh",
        ".yaml", ".yml", ".toml", ".env.example"
    }

    if ext in [".md", ".markdown", ".txt", ".rst", ".log"]:
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return file_path.read_text(encoding="latin-1", errors="replace")
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".pptx", ".potx"]:
        return extract_text_from_pptx(file_path)
    elif ext in [".xlsx", ".xls"]:
        return extract_text_from_excel(file_path)
    elif ext == ".csv":
        return extract_text_from_csv(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext in code_extensions:
        return extract_text_from_code(file_path)
    elif ext == ".json":
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            return json.dumps(data, indent=2)[:3000]
        except Exception:
            return file_path.read_text(encoding="utf-8", errors="replace")
    else:
        try:
            return file_path.read_text(encoding="utf-8", errors="ignore")[:2000]
        except Exception:
            return ""


def load_content_from_target(target_path: Path) -> Tuple[str, List[str]]:
    """Recursively scans a directory OR processes a single file across all supported formats.
    Extracts text, discovers links, and builds an exhaustive ground-truth knowledge bundle.
    """
    if not target_path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target_path}")

    ingested_files: List[str] = []
    collected_texts: List[str] = []
    discovered_urls: Set[str] = set()

    supported_exts = {
        ".md", ".markdown", ".txt", ".pdf", ".pptx", ".potx",
        ".xlsx", ".xls", ".csv", ".docx", ".json",
        ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".htm",
        ".css", ".sql", ".rs", ".go", ".java", ".cpp", ".c",
        ".yaml", ".yml"
    }

    if target_path.is_file():
        text = extract_text_from_file(target_path)
        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)
        discovered_urls.update(urls)
        ingested_files.append(f"{target_path.name} ({len(text)} chars)")
        collected_texts.append(f"# File: {target_path.name}\n\n{text}")
    elif target_path.is_dir():
        for root, _, files in os.walk(target_path):
            # Skip hidden dirs like .git, node_modules, __pycache__
            if any(part.startswith(".") or part in ["node_modules", "__pycache__", "venv", ".venv"] for part in Path(root).parts):
                continue

            for file in sorted(files):
                fpath = Path(root) / file
                if fpath.suffix.lower() in supported_exts:
                    file_text = extract_text_from_file(fpath)
                    if file_text.strip():
                        urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', file_text)
                        discovered_urls.update(urls)
                        ingested_files.append(f"{file} ({len(file_text)} chars)")
                        collected_texts.append(f"## Document / Asset: {file}\n\n{file_text}\n")

    if not collected_texts:
        raise ValueError(f"No readable files found in '{target_path}'. Supported: .md, .txt, .pdf, .pptx, .xlsx, .docx, .csv, code files")

    # Append discovered links if present
    if discovered_urls:
        url_section = "### Discovered Reference Links & Portfolios:\n" + "\n".join([f"- {u}" for u in list(discovered_urls)[:15]])
        collected_texts.append(url_section)

    combined_text = "\n\n========================================\n\n".join(collected_texts)
    return combined_text, ingested_files


def extract_sections_heuristic(text: str) -> UserProfile:
    """Heuristic / Rule-based extraction that works completely offline with zero API keys.
    Parses headers, code signatures, bullet points, skills, geography, and insider advantages.
    """
    lines = text.splitlines()

    hard_skills: List[str] = []
    soft_skills: List[str] = []
    domains: List[str] = []
    unfair_advantages: List[str] = []
    location = "Global / Remote"
    capital = "Bootstrapped / Low Capital"
    time_commitment = "Full-time / High Priority"
    notes: List[str] = []

    tech_keywords = {
        "python", "javascript", "typescript", "react", "next.js", "node", "django", "fastapi",
        "sql", "postgresql", "mysql", "mongodb", "docker", "kubernetes", "aws", "gcp",
        "excel", "tally", "accounting", "cad", "solidworks", "hardware", "iot", "embedded",
        "flutter", "android", "ios", "machine learning", "data science", "llm", "ai",
        "sales", "cold calling", "marketing", "seo", "copywriting", "graphic design",
        "logistics", "supply chain", "operations", "chemical", "civil", "mechanical", "flask",
        "express", "c++", "rust", "golang", "pandas", "numpy", "tensorflow", "pytorch",
        "esp32", "arduino", "raspberry pi", "gsm", "gps", "lora"
    }

    domain_keywords = {
        "agritech", "agriculture", "farming", "dairy", "logistics", "trucking", "freight",
        "warehousing", "textile", "garments", "manufacturing", "factories", "healthcare",
        "clinics", "pharmacy", "hospitals", "real estate", "construction", "interior design",
        "education", "edtech", "coaching", "sme", "kirana", "retail", "wholesale",
        "b2b", "legal", "compliance", "gst", "customs", "import export", "hospitality",
        "hotels", "restaurants", "food", "waste management", "solar", "renewable",
        "stone", "marble", "granite", "ceramics", "mining", "metals", "scrap"
    }

    current_section = "general"

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        lower = stripped.lower()

        # Check section headers
        if re.search(r'(skills?|technologies|tools?|expertise|languages|competencies|stack)', lower) and (line.startswith("#") or ":" in line):
            current_section = "skills"
            continue
        elif re.search(r'(domain|industry|interest|sector|area|field|market|vertical)', lower) and (line.startswith("#") or ":" in line):
            current_section = "domain"
            continue
        elif re.search(r'(location|city|state|geography|region|place|address|where)', lower) and (line.startswith("#") or ":" in line):
            current_section = "location"
            continue
        elif re.search(r'(advantage|network|connection|insider|family|access|moat|resource|assets|clients)', lower) and (line.startswith("#") or ":" in line):
            current_section = "advantage"
            continue
        elif re.search(r'(budget|capital|money|funds?|investment)', lower) and (line.startswith("#") or ":" in line):
            current_section = "capital"
            continue
        elif re.search(r'(time|hours?|availability|commitment)', lower) and (line.startswith("#") or ":" in line):
            current_section = "time"
            continue

        cleaned_item = re.sub(r'^[-*•\d\.\>\s]+', '', stripped).strip()

        if current_section == "skills":
            if cleaned_item:
                items = [x.strip() for x in re.split(r'[,|;]', cleaned_item) if x.strip()]
                for item in items:
                    if len(item) > 1:
                        hard_skills.append(item)
        elif current_section == "domain":
            if cleaned_item:
                items = [x.strip() for x in re.split(r'[,|;]', cleaned_item) if x.strip()]
                for item in items:
                    if len(item) > 1:
                        domains.append(item)
        elif current_section == "location":
            if cleaned_item and location == "Global / Remote":
                location = cleaned_item
        elif current_section == "advantage":
            if cleaned_item:
                unfair_advantages.append(cleaned_item)
        elif current_section == "capital":
            if cleaned_item:
                capital = cleaned_item
        elif current_section == "time":
            if cleaned_item:
                time_commitment = cleaned_item
        else:
            for kw in tech_keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', lower) and kw not in [s.lower() for s in hard_skills]:
                    hard_skills.append(kw.title())
            for dm in domain_keywords:
                if re.search(r'\b' + re.escape(dm) + r'\b', lower) and dm not in [d.lower() for d in domains]:
                    domains.append(dm.title())

            geo_matches = re.findall(
                r'\b(jaipur|delhi|mumbai|bangalore|bengaluru|pune|hyderabad|chennai|kolkata|ahmedabad|surat|indore|bhopal|punjab|haryana|rajasthan|gujarat|maharashtra|up|uttar pradesh|bihar|tier-2|tier 2|tier-3|india|usa|uk|germany|remote)\b',
                lower
            )
            if geo_matches and location == "Global / Remote":
                location = geo_matches[0].title()

            notes.append(stripped)

    # Search for unlabelled advantage clues
    advantage_clues = [
        "family business", "uncle", "father", "brother", "friend", "access to", "worked in",
        "years experience", "factory", "fleet", "shop", "hospital", "contacts", "clients",
        "insider", "network", "warehouse", "quarry", "mine", "clinic"
    ]
    for line in lines:
        for clue in advantage_clues:
            if clue in line.lower() and line.strip() not in unfair_advantages:
                unfair_advantages.append(line.strip().lstrip("-*•> "))
                break

    hard_skills = list(dict.fromkeys(hard_skills))
    domains = list(dict.fromkeys(domains))
    unfair_advantages = list(dict.fromkeys(unfair_advantages))

    if not domains:
        domains = ["B2B SME Operations & Trade Workflows"]
    if not hard_skills:
        hard_skills = ["Problem Solving", "Rapid Execution", "Customer Outreach"]

    # Detect if user is technical (software, coding, hardware, data)
    tech_identifiers = {
        "python", "javascript", "typescript", "react", "next.js", "node", "django", "fastapi",
        "sql", "postgresql", "backend", "frontend", "fullstack", "developer", "engineer",
        "docker", "aws", "iot", "hardware", "embedded", "data science", "machine learning", "coding"
    }
    is_tech = any(
        any(t in skill.lower() for t in tech_identifiers) for skill in hard_skills
    ) or any(t in text.lower() for t in ["developer", "software engineer", "coder", "programmer", "fullstack", "backend", "hardware engineer"])

    return UserProfile(
        name="Founder",
        hard_skills=hard_skills[:15],
        soft_skills=soft_skills[:10],
        domains=domains[:10],
        location=location,
        unfair_advantages=unfair_advantages[:8],
        capital=capital,
        time_commitment=time_commitment,
        interests_and_notes="\n".join(notes[:15]),
        raw_text=text,
        is_tech_user=is_tech
    )


def parse_target_path(target_path: Path) -> Tuple[UserProfile, List[str]]:
    """Ingests any file (.md, .txt, .pdf, .pptx, .xlsx, .csv, .docx, code) OR entire folder,
    and constructs the parsed UserProfile.
    """
    combined_text, files_ingested = load_content_from_target(target_path)
    profile = extract_sections_heuristic(combined_text)
    return profile, files_ingested
