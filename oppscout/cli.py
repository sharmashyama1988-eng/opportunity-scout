"""Command-Line Interface (CLI) for Opportunity Scout.
Supports folder/file drag-and-drop, 20+ specialized search algorithms,
structured outputs (Output 1, Output 2, Output 3), interactive explanation coaching,
and hyper-deep research re-runs if the user wants even better opportunities.
"""

import argparse
import asyncio
import os
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

from oppscout.algorithms import SpecializedSearchAlgorithms
from oppscout.analyzer import OpportunityAnalyzer
from oppscout.explainer import answer_founder_question, explain_opportunity_in_detail
from oppscout.formatters import (
    generate_structured_outputs,
    print_rich_report,
)
from oppscout.languages import normalize_language_choice, prompt_user_language
from oppscout.parser import clean_file_path, parse_target_path
from oppscout.researcher import DeepMarketScraper

console = Console()

BANNER = """[bold gold1]
 ╔════════════════════════════════════════════════════════════════════════════╗
 ║                      O P P O R T U N I T Y   S C O U T                    ║
 ║           Autonomous Real-World Problem Discovery & Niche Engine           ║
 ║          "Logo ke paas opportunity hoti hai but pta nahi hota hai"        ║
 ╚════════════════════════════════════════════════════════════════════════════╝[/bold gold1]
[dim italic] Uncovers non-obvious, unsexy operational problems with high willingness-to-pay
 Powered by 20+ specialized friction algorithms & automated multi-format ingestion.
 Supports .md, .txt, .pdf, .xlsx, .docx, .pptx, code OR entire document folders.[/dim italic]
"""

SAMPLE_PROFILE_MD = """# Founder Strategic Profile

## About Me & Background
I am a software engineer and builder based in Jaipur, Rajasthan.
I have worked on backend systems and IoT prototypes, and I want to start a high-margin business or build technology that solves real problems.

## Hard Skills
- Python, FastAPI, PostgreSQL, Next.js
- Basic IoT & Hardware Prototyping (ESP32, GSM modems)
- Data extraction & Workflow automation

## Target Domains & Interests
- Trucking & Regional Freight Logistics
- Stone & Marble Cutting / Processing (Kishangarh & Makrana belt)
- B2B SME Wholesale Distribution

## My Location & Local Foothold
- Jaipur & Western Rajasthan Industrial Corridor

## Unfair Advantages & Network Access
- My uncle owns a regional fleet of 45 freight trucks running between Rajasthan, Gujarat, and Delhi NCR.
- My school friend manages a stone processing and marble export unit in Kishangarh.
- Direct boots-on-the-ground access to fleet drivers, brokers, and warehouse managers.

## Constraints & Capital
- Bootstrapped: ₹50,000 - ₹1,00,000 initial budget
- Commitment: 30-40 hours per week
"""


def ensure_sample_template() -> Path:
    """Creates a sample profile file in templates/ if not already present."""
    template_dir = Path("templates")
    template_dir.mkdir(parents=True, exist_ok=True)
    sample_file = template_dir / "sample_profile.md"
    if not sample_file.exists():
        sample_file.write_text(SAMPLE_PROFILE_MD, encoding="utf-8")
    return sample_file


async def interactive_coaching_loop(report, target_path: Path, auto_open: bool = False):
    """Interactive post-analysis coaching loop.
    Explains outputs to the user, answers questions, or triggers hyper-deep research
    with 20+ specialized algorithms if the user wants even better/different ideas.
    """
    profile = report.profile
    opportunities = report.opportunities

    while True:
        console.print()
        console.print("[bold gold1]┌─────────────────────────────────────────────────────────────┐[/bold gold1]")
        console.print("[bold white]│ WHAT WOULD YOU LIKE TO DO NEXT? (EXPLAIN / DEEPEN / COACH)  │[/bold white]")
        console.print("[bold gold1]└─────────────────────────────────────────────────────────────┘[/bold gold1]")
        console.print(" [bold cyan][1][/bold cyan]  Samjhao Output #1 (Detailed breakdown + customer script)")
        console.print(" [bold cyan][2][/bold cyan]  Samjhao Output #2 (Detailed breakdown + customer script)")
        console.print(" [bold cyan][3][/bold cyan]  Samjhao Output #3 (Detailed breakdown + customer script)")
        console.print(" [bold yellow][4][/bold yellow]  \"Pasand nahi aayi\" -> Run Hyper-Deep Research with 20+ Algorithms (Aur better nikaalo)")
        console.print(" [bold green][5][/bold green]  Ask a custom execution question (e.g. Zero-budget bootstrapping)")
        console.print(" [bold blue][6][/bold blue]  Open Classical HTML Executive Report in browser")
        console.print(" [bold dim][0][/bold dim]  Done / Exit")

        choice = Prompt.ask("\n[bold gold1]Enter your choice[/bold gold1]", choices=["0", "1", "2", "3", "4", "5", "6"], default="1")

        if choice == "0":
            console.print("[bold green]All the best founder! Go build something real.[/bold green]\n")
            break
        elif choice in ["1", "2", "3"]:
            idx = int(choice) - 1
            if idx < len(opportunities):
                explain_opportunity_in_detail(opportunities[idx], profile)
            else:
                console.print(f"[bold red]Output #{choice} not found.[/bold red]")
        elif choice == "4":
            console.print("\n[bold yellow]⚡ Activating Hyper-Deep Research Mode with 20+ Algorithms...[/bold yellow]")
            algo_queries = SpecializedSearchAlgorithms.get_queries_for_profile(
                profile.domains[0] if profile.domains else "B2B SME",
                profile.location
            )
            console.print(f"[dim]Deploying {len(algo_queries)} algorithmic vectors (Batch Rejections, E-Waybill Rules, Khata Defaults, Demurrage, Emergency Breakdown)...[/dim]")
            # Rerun discovery pipeline with deep algorithm sampling
            await run_discovery_pipeline(target_path, language=profile.language, deep_mode=True, auto_open=auto_open, interactive=False)
            break
        elif choice == "5":
            q = Prompt.ask(f"[bold green]Ask custom question in {profile.language} (e.g. Pehle 10 din mein client kaise milega?)[/bold green]")
            if q.strip():
                top_opp = opportunities[0]
                await answer_founder_question(q, top_opp, profile)
        elif choice == "6":
            html_file = Path("outputs") / "full_dossier.html"
            if html_file.exists():
                webbrowser.open(html_file.resolve().as_uri())
                console.print("[bold green]Opened HTML report in browser![/bold green]")


async def run_discovery_pipeline(
    target_path: Path,
    language: str = "English",
    domain_override: str = None,
    location_override: str = None,
    tech_only: bool = False,
    auto_open: bool = True,
    deep_mode: bool = False,
    interactive: bool = True,
):
    """Executes the complete end-to-end automated discovery pipeline."""
    if not target_path.exists():
        console.print(f"[bold red]Error:[/bold red] Path not found at '{target_path}'.")
        return

    console.print()
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[bold yellow]{task.description}[/bold yellow]"),
        console=console,
    ) as progress:
        # Step 1: Universal Parsing (File or Folder)
        task1 = progress.add_task("[1/4] Scanning target & extracting founder leverage...", total=1)
        profile, ingested_files = parse_target_path(target_path)
        profile.language = language

        if domain_override:
            profile.domains = [domain_override] + profile.domains
        if location_override:
            profile.location = location_override
        if tech_only:
            profile.is_tech_user = True

        progress.advance(task1)

        # Step 2: 20+ Specialized Algorithms Live Scraping
        status_msg = "[2/4] Executing 20+ specialized friction algorithms & live forum mining..." if deep_mode else "[2/4] Deep-scraping Reddit, HackerNews & DuckDuckGo for real complaints..."
        task2 = progress.add_task(status_msg, total=1)
        scraper = DeepMarketScraper()
        signals = await scraper.execute_deep_research(profile, max_signals=10 if deep_mode else 8)
        await scraper.close()
        progress.advance(task2)

        # Step 3: Synthesis & Scoring
        task3 = progress.add_task("[3/4] Synthesizing bespoke B2B opportunities (5-Factor Matrix)...", total=1)
        analyzer = OpportunityAnalyzer()
        report = await analyzer.analyze_and_synthesize(profile, signals)
        progress.advance(task3)

        # Step 4: Formatting & Structured Deliverables
        task4 = progress.add_task("[4/4] Writing structured Output 1, 2, 3 files & executive dossiers...", total=1)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        outputs_dir = Path("outputs")

        created_paths = generate_structured_outputs(report, outputs_dir, timestamp)
        html_path = created_paths["html"]
        progress.advance(task4)

    # Ingestion Notification
    files_summary = ", ".join(ingested_files[:4])
    if len(ingested_files) > 4:
        files_summary += f" and {len(ingested_files)-4} more"
    console.print(f"[bold green]✔ Ingested Ground Truth ({len(ingested_files)} sources):[/bold green] [dim]{files_summary}[/dim]")
    if profile.is_tech_user:
        console.print("[bold magenta]⚡ High-Ticket Tech Mode Active:[/bold magenta] Anti-freelancing guard enabled, B2B architecture & ARR ladders unlocked.")

    # Render Terminal Report
    print_rich_report(report)

    # Summary Panel of Generated Deliverables
    console.print(
        Panel(
            f"[bold green]Discovery Complete! Structured Outputs Generated:[/bold green]\n\n"
            f"[bold yellow]• Output #1 Dossier:[/bold yellow] {created_paths.get('output_1', '').resolve()}\n"
            f"[bold yellow]• Output #2 Dossier:[/bold yellow] {created_paths.get('output_2', '').resolve()}\n"
            f"[bold yellow]• Output #3 Dossier:[/bold yellow] {created_paths.get('output_3', '').resolve()}\n\n"
            f"[bold cyan]• Full Classical HTML Dossier:[/bold cyan] {html_path.resolve()}\n"
            f"[bold cyan]• Complete Summary Markdown:[/bold cyan] {created_paths.get('summary', '').resolve()}\n"
            f"[bold cyan]• Structured JSON Dataset:[/bold cyan] {created_paths.get('json', '').resolve()}",
            title="[bold white]STRUCTURED OUTPUTS CREATED IN outputs/[/bold white]",
            border_style="green",
        )
    )

    if auto_open:
        try:
            webbrowser.open(html_path.resolve().as_uri())
        except Exception:
            pass

    if interactive:
        await interactive_coaching_loop(report, target_path, auto_open=auto_open)


def main():
    """Main CLI entrypoint with expanded controls."""
    parser = argparse.ArgumentParser(
        description="Opportunity Scout: Autonomous Real-World Problem Discovery & Niche Engine."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Path to file (.md, .txt, .pdf, .xlsx, .docx) OR entire folder of documents (or drag-and-drop into terminal).",
    )
    parser.add_argument(
        "--domain",
        type=str,
        default=None,
        help="Explicit domain/industry to focus on (e.g. 'AgriTech', 'Trucking', 'Textile').",
    )
    parser.add_argument(
        "--location",
        type=str,
        default=None,
        help="Explicit geographic location or local cluster to focus on (e.g. 'Jaipur', 'Surat', 'Punjab').",
    )
    parser.add_argument(
        "--tech-only",
        action="store_true",
        help="Force high-ticket tech/SaaS opportunities only (bans low-margin freelancing).",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Run hyper-deep research with all 20+ specialized friction algorithms.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Do not enter interactive coaching loop after analysis.",
    )
    parser.add_argument(
        "--mcp",
        action="store_true",
        help="Run as an MCP (Model Context Protocol) server for AI agents.",
    )
    parser.add_argument(
        "--template",
        action="store_true",
        help="Generate a sample profile markdown file in templates/ and exit.",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open the HTML report in web browser.",
    )
    parser.add_argument(
        "--language",
        "-l",
        type=str,
        default=None,
        help="Preferred output language (e.g. 'English', 'Hinglish', 'Hindi', 'Spanish', 'German', or ANY language in the world).",
    )

    args = parser.parse_args()

    if args.mcp:
        from oppscout.mcp_server import run_server
        run_server()
        return

    if args.template:
        sample_path = ensure_sample_template()
        console.print(f"[bold green]Created sample profile at:[/bold green] {sample_path.resolve()}")
        return

    console.print(BANNER)

    # STEP 1: Prompt for language FIRST before asking for path!
    if args.language:
        selected_language, _ = normalize_language_choice(args.language)
        console.print(f"[bold green]✔ Language selected via flag:[/bold green] [bold white]{selected_language}[/bold white]\n")
    elif not args.non_interactive:
        selected_language, _ = prompt_user_language()
    else:
        selected_language = "English"

    # STEP 2: Ingestion & Document Selection
    raw_target = args.target
    if not raw_target:
        ensure_sample_template()
        console.print("[bold bright_white]STEP 2: Document / Folder Ingestion Options:[/bold bright_white]")
        console.print(" 1. [bold yellow]Drag and drop[/bold yellow] any file (.md, .txt, .pdf, .xlsx, .docx) into this terminal.")
        console.print(" 2. [bold yellow]Or drag and drop an entire folder[/bold yellow] with all your resumes, notes, and records!")
        console.print(" 3. Or type [bold cyan]'sample'[/bold cyan] (or press [bold cyan]Enter[/bold cyan]) to run the built-in demo.\n")

        user_input = Prompt.ask("[bold gold1]Drag & Drop file/folder here (or enter path)[/bold gold1]", default="sample")
        if user_input.strip().lower() in ["sample", "demo", ""]:
            raw_target = "templates/sample_profile.md"
        else:
            raw_target = user_input

    cleaned_path = clean_file_path(raw_target)
    asyncio.run(
        run_discovery_pipeline(
            cleaned_path,
            language=selected_language,
            domain_override=args.domain,
            location_override=args.location,
            tech_only=args.tech_only,
            auto_open=not args.no_browser,
            deep_mode=args.deep,
            interactive=not args.non_interactive,
        )
    )


if __name__ == "__main__":
    main()
