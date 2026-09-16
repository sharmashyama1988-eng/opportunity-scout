"""Formatters for Opportunity Scout.
Provides Rich Terminal Rendering, Markdown Dossier generation,
and an Executive Classical UI HTML Report generator.
"""

from datetime import datetime
import json
from pathlib import Path
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from oppscout.languages import get_localized_headers, normalize_language_choice
from oppscout.models import AnalysisReport, OpportunityDossier, UserProfile

console = Console()


def print_rich_report(report: AnalysisReport):
    """Renders the executive dossier to the terminal using Rich with classical styling."""
    profile = report.profile

    # 1. Header Banner
    header_text = Text()
    header_text.append("OPPORTUNITY SCOUT ", style="bold gold1")
    header_text.append("| REAL PROBLEM & NICHE DISCOVERY ENGINE\n", style="bold white")
    header_text.append(f"Generated on {report.generated_at} | Profile: {profile.name} ({profile.location})", style="dim italic")

    console.print()
    console.print(Panel(header_text, border_style="gold1", title="[bold white]EXECUTIVE BRIEFING[/bold white]"))

    # 2. Profile Matrix Table
    p_table = Table(title="Founder Profile & Strategic Leverage", border_style="bright_blue", show_header=True)
    p_table.add_column("Dimension", style="bold cyan", width=22)
    p_table.add_column("Extracted Ground Truth", style="white")

    p_table.add_row("Hard & Technical Skills", ", ".join(profile.hard_skills) or "None specified")
    p_table.add_row("Focus Domains", ", ".join(profile.domains) or "General SME")
    p_table.add_row("Geographic Foothold", profile.location or "Global")
    p_table.add_row("Unfair Network Advantage", "\n".join([f"• {a}" for a in profile.unfair_advantages]) or "Direct Local Access")
    p_table.add_row("Capital / Constraints", profile.capital)
    console.print(p_table)

    # 3. Market Signals Mined
    console.print()
    sig_tree = Tree(f"[bold green]Market Signals & Real Friction Mined ({report.total_signals_mined} verified sources)[/bold green]")
    for sig in report.signals[:4]:
        node = sig_tree.add(f"[bold yellow]{sig.source}[/bold yellow]: [white]{sig.title}[/white]")
        node.add(f"[dim italic]\"{sig.snippet[:180]}...\"[/dim italic]")
    console.print(sig_tree)

    # 4. Opportunity Dossiers
    console.print()
    console.print("[bold gold1]================================================================================[/bold gold1]")
    console.print("[bold white]TOP RANKED UNCONVENTIONAL REAL-WORLD OPPORTUNITIES (HIGH FOUNDER-PROBLEM FIT)[/bold white]")
    console.print("[bold gold1]================================================================================[/bold gold1]")

    for idx, opp in enumerate(report.opportunities, 1):
        score = opp.scores.composite_score
        score_color = "green" if score >= 90 else "gold1"

        card_text = Text()
        card_text.append(f"PROBLEM STATEMENT:\n", style="bold red")
        card_text.append(f"{opp.problem_statement}\n\n", style="white")

        card_text.append(f"WHO SUFFERS & PAYS (CUSTOMER AVATAR):\n", style="bold yellow")
        card_text.append(f"{opp.target_customer}\n\n", style="bright_white")

        card_text.append(f"CURRENT PAINFUL WORKAROUNDS:\n", style="bold magenta")
        card_text.append(f"{opp.current_workarounds}\n\n", style="dim")

        card_text.append(f"YOUR UNFAIR ADVANTAGE (FOUNDER-PROBLEM FIT):\n", style="bold cyan")
        card_text.append(f"{opp.founder_advantage_explanation}\n\n", style="italic cyan")

        card_text.append(f"DAY-1 (48-HOUR) VALIDATION BLUEPRINT (THE MOM TEST):\n", style="bold green")
        for step in opp.day1_validation_plan:
            card_text.append(f"  • {step}\n", style="bright_green")

        if opp.is_high_ticket_tech:
            card_text.append(f"[HIGH-TICKET B2B TECH | NO FREELANCING]\n", style="bold reverse bright_magenta")
            card_text.append(f"MONTHLY EARNING POTENTIAL: {opp.earning_potential}\n\n", style="bold bright_green")
            if opp.high_ticket_tech_blueprint:
                card_text.append(f"ENTERPRISE TECH ARCHITECTURE & ANTI-FREELANCING DIRECTIVE:\n", style="bold bright_cyan")
                card_text.append(f"{opp.high_ticket_tech_blueprint}\n\n", style="cyan")

        card_text.append(f"LEAN TECH STACK: ", style="bold blue")
        card_text.append(f"{', '.join(opp.mvp_tech_stack)}\n", style="bright_blue")

        card_text.append(f"MONETIZATION MODEL: ", style="bold gold1")
        card_text.append(f"{opp.monetization}\n", style="bright_yellow")

        # Score Breakdown sub-table
        scores_table = Table(box=None, padding=(0, 2), show_header=False)
        scores_table.add_column("Metric", style="dim")
        scores_table.add_column("Value", style="bold white")
        scores_table.add_row("Pain Intensity", f"{opp.scores.pain_intensity}/10")
        scores_table.add_row("Willingness to Pay (WTP)", f"{opp.scores.willingness_to_pay}/10")
        scores_table.add_row("Founder-Problem Fit", f"{opp.scores.founder_fit}/10")
        scores_table.add_row("Competition Whitespace", f"{opp.scores.whitespace}/10")
        scores_table.add_row("Composite Score", f"[{score_color}]{score}/100[/{score_color}]")

        title_line = f" #{idx} - {opp.title} [Composite: {score}/100] "
        console.print(
            Panel(
                card_text,
                title=f"[bold white]{title_line}[/bold white]",
                border_style=score_color,
                subtitle="[dim]Opportunity Scout Dossier[/dim]"
            )
        )
        console.print(scores_table)
        console.print()


def generate_markdown_report(report: AnalysisReport, output_path: Path):
    """Generates clean, full-detail Markdown dossier localized in the chosen language."""
    p = report.profile
    lang = p.language or "English"
    lh = get_localized_headers(lang)

    lines = [
        f"# Executive Opportunity Dossier: Real Problems & High-Fit Niches",
        f"**Language:** {lang} | **Generated Date:** {report.generated_at}",
        f"**Profile:** {p.name} | **Location:** {p.location}",
        f"**Focus Domains:** {', '.join(p.domains)}",
        f"**Core Hard Skills:** {', '.join(p.hard_skills)}",
        f"**Unfair Advantages:** {', '.join(p.unfair_advantages) or 'Local presence'}",
        "",
        "---",
        "## Executive Summary",
        report.executive_summary,
        "",
        "---",
        "## Mined Real-World Market Signals",
    ]

    for s in report.signals:
        lines.append(f"### {s.title} ({s.source})")
        lines.append(f"> *\"{s.snippet}\"*")
        if s.url:
            lines.append(f"- Source URL: [{s.url}]({s.url})")
        lines.append("")

    lines.append("---")
    lines.append("## Validated Opportunities & Action Blueprints")

    for idx, opp in enumerate(report.opportunities, 1):
        lines.append(f"### Opportunity #{idx}: {opp.title}")
        lines.append(f"**Composite Opportunity Score:** `{opp.scores.composite_score} / 100`")
        lines.append("")
        lines.append(f"| Metric | Score | Note |")
        lines.append(f"|---|---|---|")
        lines.append(f"| Pain Intensity | `{opp.scores.pain_intensity} / 10` | Urgent operational friction |")
        lines.append(f"| Willingness to Pay | `{opp.scores.willingness_to_pay} / 10` | Daily cash/time leakage |")
        lines.append(f"| Founder-Problem Fit | `{opp.scores.founder_fit} / 10` | Direct match to skills & advantage |")
        lines.append(f"| Competition Whitespace | `{opp.scores.whitespace} / 10` | Underserved, non-obvious niche |")
        lines.append(f"| Day-1 Feasibility | `{opp.scores.day1_feasibility} / 10` | Immediate 48-hr validation |")
        lines.append("")
        lines.append(f"#### 1. {lh['problem_title']}")
        lines.append(opp.problem_statement)
        lines.append("")
        lines.append(f"#### 2. {lh['customer_title']}")
        lines.append(opp.target_customer)
        lines.append("")
        lines.append(f"#### 3. {lh['workarounds_title']}")
        lines.append(opp.current_workarounds)
        lines.append("")
        lines.append(f"#### 4. {lh['unfair_edge_title']}")
        lines.append(opp.founder_advantage_explanation)
        lines.append("")
        lines.append(f"#### 5. {lh['validation_title']}")
        for step in opp.day1_validation_plan:
            lines.append(f"- [ ] {step}")
        lines.append("")
        lines.append(f"#### 6. {lh['tech_blueprint_title']}")
        lines.append(f"- **{lh['earning_title']}:** `{opp.earning_potential}`")
        lines.append(f"- **{lh['monetization_title']}:** {opp.monetization}")
        lines.append(f"- **Lean MVP Tech Stack:** `{', '.join(opp.mvp_tech_stack)}`")
        lines.append("")
        lines.append("---")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")

def generate_individual_opportunity_markdown(opp: OpportunityDossier, profile: UserProfile, idx: int) -> str:
    """Creates a standalone, detailed executive action dossier for an individual opportunity in the selected language."""
    lang = profile.language or "English"
    lh = get_localized_headers(lang)
    script = lh["mom_test_question"].format(target=opp.target_customer, location=profile.location)

    lines = [
        f"# Output #{idx}: {opp.title}",
        f"**Language:** {lang} | **Composite Opportunity Score:** `{opp.scores.composite_score} / 100`",
        f"**Target Market / Location:** {profile.location}",
        f"**Target Persona ({lh['customer_title']}):** {opp.target_customer}",
        "",
        "---",
        f"## 1. {lh['problem_title']}",
        opp.problem_statement,
        "",
        "### Ground Truth Market Evidence Mined:",
    ]
    for ev in opp.why_it_is_real:
        lines.append(f"- {ev}")
    lines.append("")
    lines.append(f"### {lh['workarounds_title']}:")
    lines.append(opp.current_workarounds)
    lines.append("")
    lines.append("---")
    lines.append(f"## 2. {lh['unfair_edge_title']}")
    lines.append(opp.founder_advantage_explanation)
    lines.append("")
    lines.append("---")
    lines.append(f"## 3. {lh['mom_test_title']}")
    lines.append(f"> *\"{script}\"*")
    lines.append("")
    lines.append("---")
    lines.append(f"## 4. {lh['validation_title']}")
    for step in opp.day1_validation_plan:
        lines.append(f"- [ ] {step}")
    lines.append("")
    lines.append("---")
    lines.append(f"## 5. {lh['tech_blueprint_title']}")
    lines.append(f"- **{lh['earning_title']}:** `{opp.earning_potential}`")
    lines.append(f"- **{lh['monetization_title']}:** {opp.monetization}")
    lines.append(f"- **Lean MVP Tech Stack:** `{', '.join(opp.mvp_tech_stack)}`")
    lines.append("")
    if opp.high_ticket_tech_blueprint:
        lines.append("```yaml")
        lines.append(opp.high_ticket_tech_blueprint)
        lines.append("```")
    lines.append("")
    return "\n".join(lines)


def generate_structured_outputs(report: AnalysisReport, base_dir: Path, timestamp: str) -> Dict[str, Path]:
    """Generates structured individual files (Output 1, 2, 3) as well as consolidated dossiers."""
    base_dir.mkdir(parents=True, exist_ok=True)
    run_dir = base_dir / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    created_paths = {}

    # 1. Individual Output Files (Output 1, Output 2, Output 3)
    for idx, opp in enumerate(report.opportunities, 1):
        clean_title = "".join([c if c.isalnum() else "_" for c in opp.title[:30]]).strip("_").lower()
        content = generate_individual_opportunity_markdown(opp, report.profile, idx)

        # Save inside run directory
        run_file = run_dir / f"output_{idx}_{clean_title}.md"
        run_file.write_text(content, encoding="utf-8")

        # Also save at root of outputs/ for quick access
        root_file = base_dir / f"output_{idx}.md"
        root_file.write_text(content, encoding="utf-8")

        created_paths[f"output_{idx}"] = root_file

    # 2. Consolidated Executive Markdown Summary
    full_md = run_dir / "full_summary.md"
    generate_markdown_report(report, full_md)
    root_summary = base_dir / "full_summary.md"
    generate_markdown_report(report, root_summary)
    created_paths["summary"] = root_summary

    # 3. Classical UI HTML Dashboard
    full_html = run_dir / "full_dossier.html"
    generate_classical_html_report(report, full_html)
    root_html = base_dir / "full_dossier.html"
    generate_classical_html_report(report, root_html)
    created_paths["html"] = root_html

    # 4. JSON Dataset
    full_json = run_dir / "dataset.json"
    full_json.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    root_json = base_dir / "dataset.json"
    root_json.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    created_paths["json"] = root_json

    return created_paths


def generate_classical_html_report(report: AnalysisReport, output_path: Path):
    """Generates an executive HTML report inspired by Classical UI principles
    (Garamond typography, Roman Imperial / Slate palette, double-line framing, Golden Ratio balance).
    """
    p = report.profile
    lang_name, lang_code = normalize_language_choice(p.language)
    lh = get_localized_headers(lang_name)

    opp_html_cards = ""
    for idx, opp in enumerate(report.opportunities, 1):
        validation_steps_html = "".join([f"<li>{step}</li>" for step in opp.day1_validation_plan])
        evidence_html = "".join([f"<li>{ev}</li>" for ev in opp.why_it_is_real])
        stack_badges = "".join([f"<span class='tech-badge'>{tech}</span>" for tech in opp.mvp_tech_stack])

        opp_html_cards += f"""
        <article class="dossier-card">
            <header class="dossier-header">
                <div class="dossier-meta">
                    <span class="dossier-tag">Opportunity #{idx} ({lang_name})</span>
                    <span class="score-badge">Score: {opp.scores.composite_score}/100</span>
                </div>
                <h2 class="dossier-title">{opp.title}</h2>
            </header>

            <div class="metrics-grid">
                <div class="metric-cell">
                    <div class="metric-label">Pain Intensity</div>
                    <div class="metric-value">{opp.scores.pain_intensity}/10</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-label">Willingness To Pay</div>
                    <div class="metric-value">{opp.scores.willingness_to_pay}/10</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-label">Founder-Problem Fit</div>
                    <div class="metric-value">{opp.scores.founder_fit}/10</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-label">Competition Whitespace</div>
                    <div class="metric-value">{opp.scores.whitespace}/10</div>
                </div>
                <div class="metric-cell">
                    <div class="metric-label">Day-1 Feasibility</div>
                    <div class="metric-value">{opp.scores.day1_feasibility}/10</div>
                </div>
            </div>

            <section class="dossier-section">
                <h3>{lh['problem_title']}</h3>
                <p class="highlight-p">{opp.problem_statement}</p>
            </section>

            <section class="dossier-section">
                <h3>{lh['customer_title']}</h3>
                <p>{opp.target_customer}</p>
            </section>

            <section class="dossier-section">
                <h3>{lh['workarounds_title']}</h3>
                <p>{opp.current_workarounds}</p>
            </section>

            <section class="dossier-section unfair-edge-box">
                <h3>{lh['unfair_edge_title']}</h3>
                <p>{opp.founder_advantage_explanation}</p>
            </section>

            <section class="dossier-section">
                <h3>{lh['validation_title']}</h3>
                <ol class="action-list">
                    {validation_steps_html}
                </ol>
            </section>

            {f'''
            <section class="dossier-section tech-blueprint-box">
                <div class="tech-blueprint-header">
                    <span class="badge-high-ticket">High-Ticket B2B Tech &bull; Anti-Freelancing</span>
                    <span class="badge-mrr">{opp.earning_potential}</span>
                </div>
                <h3>{lh['tech_blueprint_title']}</h3>
                <pre class="blueprint-code">{opp.high_ticket_tech_blueprint}</pre>
            </section>
            ''' if opp.is_high_ticket_tech and opp.high_ticket_tech_blueprint else ''}

            <div class="execution-footer">
                <div>
                    <strong>Lean Tech Stack:</strong>
                    <div class="tech-container">{stack_badges}</div>
                </div>
                <div class="monetization-block">
                    <strong>{lh['monetization_title']}:</strong>
                    <span>{opp.monetization}</span>
                </div>
            </div>
        </article>
        """

    signals_html = ""
    for s in report.signals[:6]:
        signals_html += f"""
        <div class="signal-item">
            <div class="signal-source">{s.source} &bull; {s.pain_category}</div>
            <div class="signal-title">{s.title}</div>
            <div class="signal-snippet">"{s.snippet}"</div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Opportunity Scout | Executive Strategic Dossier</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=EB+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0e0e11;
            --bg-secondary: #141419;
            --bg-card: #181820;
            --accent-gold: #c5a059;
            --accent-gold-light: #e6c88b;
            --text-primary: #ece8df;
            --text-muted: #9e9a91;
            --border-classical: #2f2d38;
            --border-gold: #8e733e;
            --font-serif: 'EB Garamond', Georgia, serif;
            --font-display: 'Cinzel', serif;
            --font-mono: 'JetBrains Mono', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-serif);
            font-size: 19px;
            line-height: 1.65;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 960px;
            margin: 0 auto;
        }}

        .classical-frame {{
            border: 1px solid var(--border-gold);
            padding: 6px;
            margin-bottom: 40px;
        }}

        .classical-inner-frame {{
            border: 1px solid var(--border-classical);
            background: var(--bg-secondary);
            padding: 40px;
            text-align: center;
        }}

        .brand-eyebrow {{
            font-family: var(--font-mono);
            text-transform: uppercase;
            letter-spacing: 3px;
            font-size: 13px;
            color: var(--accent-gold);
            margin-bottom: 12px;
        }}

        h1.main-title {{
            font-family: var(--font-display);
            font-size: 38px;
            letter-spacing: 1.5px;
            color: #ffffff;
            margin-bottom: 14px;
            font-weight: 800;
        }}

        .executive-summary-text {{
            font-size: 21px;
            font-style: italic;
            color: var(--text-muted);
            max-width: 780px;
            margin: 0 auto;
        }}

        .profile-strip {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            background: var(--bg-card);
            border: 1px solid var(--border-classical);
            padding: 24px;
            margin-bottom: 40px;
        }}

        .profile-cell strong {{
            display: block;
            font-family: var(--font-display);
            font-size: 14px;
            letter-spacing: 1px;
            color: var(--accent-gold);
            margin-bottom: 4px;
        }}

        .profile-cell span {{
            font-size: 16px;
            color: var(--text-primary);
        }}

        .section-heading {{
            font-family: var(--font-display);
            font-size: 24px;
            color: var(--accent-gold);
            border-bottom: 1px solid var(--border-classical);
            padding-bottom: 8px;
            margin: 40px 0 24px 0;
            letter-spacing: 1px;
        }}

        .signals-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 40px;
        }}

        @media (max-width: 768px) {{
            .signals-container {{ grid-template-columns: 1fr; }}
        }}

        .signal-item {{
            background: var(--bg-card);
            border-left: 3px solid var(--accent-gold);
            padding: 16px;
            border-top: 1px solid var(--border-classical);
            border-right: 1px solid var(--border-classical);
            border-bottom: 1px solid var(--border-classical);
        }}

        .signal-source {{
            font-family: var(--font-mono);
            font-size: 11px;
            text-transform: uppercase;
            color: var(--accent-gold);
            margin-bottom: 6px;
        }}

        .signal-title {{
            font-weight: 700;
            font-size: 17px;
            color: #ffffff;
            margin-bottom: 6px;
        }}

        .signal-snippet {{
            font-size: 15px;
            font-style: italic;
            color: var(--text-muted);
        }}

        .dossier-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-classical);
            margin-bottom: 40px;
            padding: 32px;
            position: relative;
        }}

        .dossier-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .dossier-tag {{
            font-family: var(--font-display);
            color: var(--accent-gold);
            font-size: 14px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .score-badge {{
            background: rgba(197, 160, 89, 0.15);
            border: 1px solid var(--accent-gold);
            color: var(--accent-gold-light);
            font-family: var(--font-mono);
            padding: 4px 12px;
            font-size: 14px;
            font-weight: 600;
        }}

        .dossier-title {{
            font-family: var(--font-display);
            font-size: 26px;
            color: #ffffff;
            margin-bottom: 20px;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            background: var(--bg-card);
            padding: 16px;
            border: 1px solid var(--border-classical);
            margin-bottom: 24px;
            text-align: center;
        }}

        .metric-label {{
            font-size: 12px;
            font-family: var(--font-display);
            color: var(--text-muted);
            letter-spacing: 0.5px;
        }}

        .metric-value {{
            font-family: var(--font-mono);
            font-size: 20px;
            font-weight: bold;
            color: var(--accent-gold-light);
            margin-top: 4px;
        }}

        .dossier-section {{
            margin-bottom: 20px;
        }}

        .dossier-section h3 {{
            font-family: var(--font-display);
            font-size: 16px;
            color: var(--accent-gold);
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}

        .highlight-p {{
            font-size: 20px;
            color: #ffffff;
        }}

        .unfair-edge-box {{
            background: rgba(197, 160, 89, 0.08);
            border-left: 3px solid var(--accent-gold);
            padding: 16px;
        }}

        .tech-blueprint-box {{
            background: #111117;
            border: 1px solid #3c324a;
            border-left: 3px solid #b388ff;
            padding: 20px;
            margin-top: 16px;
        }}

        .tech-blueprint-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .badge-high-ticket {{
            background: rgba(179, 136, 255, 0.2);
            border: 1px solid #b388ff;
            color: #d1b3ff;
            font-family: var(--font-mono);
            font-size: 12px;
            padding: 3px 10px;
            text-transform: uppercase;
            font-weight: bold;
        }}

        .badge-mrr {{
            background: rgba(80, 250, 123, 0.15);
            border: 1px solid #50fa7b;
            color: #50fa7b;
            font-family: var(--font-mono);
            font-size: 13px;
            padding: 3px 10px;
            font-weight: bold;
        }}

        .blueprint-code {{
            font-family: var(--font-mono);
            font-size: 14px;
            background: #09090d;
            border: 1px solid #23222a;
            padding: 16px;
            color: #b0aec2;
            white-space: pre-wrap;
            line-height: 1.5;
            margin-top: 8px;
        }}

        .action-list {{
            padding-left: 24px;
            color: var(--text-primary);
        }}

        .action-list li {{
            margin-bottom: 6px;
        }}

        .execution-footer {{
            border-top: 1px solid var(--border-classical);
            padding-top: 20px;
            margin-top: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .tech-container {{
            margin-top: 6px;
        }}

        .tech-badge {{
            display: inline-block;
            background: #252430;
            color: #d1cdd9;
            font-family: var(--font-mono);
            font-size: 13px;
            padding: 3px 8px;
            margin-right: 6px;
            border-radius: 3px;
        }}

        .monetization-block span {{
            display: block;
            color: var(--accent-gold-light);
            font-style: italic;
        }}

        footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 24px;
            border-top: 1px solid var(--border-classical);
            font-size: 14px;
            color: var(--text-muted);
            font-family: var(--font-display);
            letter-spacing: 1px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="classical-frame">
            <div class="classical-inner-frame">
                <div class="brand-eyebrow">Opportunity Scout Strategic Dossier</div>
                <h1 class="main-title">Validated Market Pain & Niche Blueprint</h1>
                <p class="executive-summary-text">"{report.executive_summary}"</p>
            </div>
        </div>

        <div class="profile-strip">
            <div class="profile-cell">
                <strong>Founder Skills</strong>
                <span>{', '.join(p.hard_skills) or 'Generalist'}</span>
            </div>
            <div class="profile-cell">
                <strong>Local Foothold</strong>
                <span>{p.location}</span>
            </div>
            <div class="profile-cell">
                <strong>Domain Context</strong>
                <span>{', '.join(p.domains)}</span>
            </div>
            <div class="profile-cell">
                <strong>Unfair Advantage</strong>
                <span>{p.unfair_advantages[0] if p.unfair_advantages else 'Boots on Ground'}</span>
            </div>
        </div>

        <h2 class="section-heading">Verified Field Signals Mined</h2>
        <div class="signals-container">
            {signals_html}
        </div>

        <h2 class="section-heading">Bespoke High-Conviction Opportunities</h2>
        <div class="dossiers-wrapper">
            {opp_html_cards}
        </div>

        <footer>
            Opportunity Scout &bull; Formatted with Classical UI Harmony &bull; Generated {report.generated_at}
        </footer>
    </div>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
