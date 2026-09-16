"""Fast deterministic unit test runner."""
import asyncio
import tempfile
from pathlib import Path
from oppscout.analyzer import OpportunityAnalyzer
from oppscout.models import UserProfile
from oppscout.parser import (
    clean_file_path,
    extract_sections_heuristic,
    load_content_from_target,
    parse_target_path,
)
from oppscout.tools import generate_high_ticket_tech_blueprint

def run():
    print("1. Testing clean_file_path...")
    assert str(clean_file_path('"F:\\test.md"')) == "F:\\test.md"
    assert str(clean_file_path("'F:\\test.pdf'")) == "F:\\test.pdf"
    assert str(clean_file_path("& 'F:\\test.docx'")) == "F:\\test.docx"
    print("   [OK] Path cleaning works.")

    print("2. Testing tech profile parsing...")
    text = "# Profile\n## Skills\nPython, FastAPI, Docker, SQL\n## Location\nJaipur\n## Advantages\nUncle has 40 trucks\n"
    p = extract_sections_heuristic(text)
    assert p.is_tech_user is True
    assert "Jaipur" in p.location
    assert len(p.unfair_advantages) > 0
    print("   [OK] Tech profile & leverage extraction works.")

    print("3. Testing folder ingestion...")
    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        (td / "doc1.md").write_text("# Skills\nPython, IoT", encoding="utf-8")
        (td / "doc2.txt").write_text("Family owns marble processing plant in Kishangarh", encoding="utf-8")
        combined, files = load_content_from_target(td)
        assert len(files) == 2
        assert "Kishangarh" in combined
    print("   [OK] Folder ingestion works.")

    print("4. Testing high-ticket tech blueprint...")
    b = generate_high_ticket_tech_blueprint("Audit Suite", "Fleet Owners", ["Python", "FastAPI", "IoT"])
    assert "architecture_name" in b
    assert "anti_freelancing_rule" in b
    print("   [OK] High-ticket B2B blueprint works.")

    print("5. Testing algorithmic opportunity scoring & dossiers...")
    analyzer = OpportunityAnalyzer()
    dossiers = analyzer._synthesize_tailored_algorithmic(p, [])
    assert len(dossiers) >= 3
    for d in dossiers:
        assert 1 <= d.scores.pain_intensity <= 10
        assert 0.0 <= d.scores.composite_score <= 100.0
        assert d.is_high_ticket_tech is True
        assert len(d.day1_validation_plan) >= 3
    print("   [OK] Opportunity dossiers & scoring valid.")

    print("6. Testing universal language normalization & dictionary...")
    from oppscout.languages import normalize_language_choice, get_localized_headers
    assert normalize_language_choice("1") == ("English", "en")
    assert normalize_language_choice("2") == ("Hinglish", "hi-Latn")
    assert normalize_language_choice("3") == ("Hindi", "hi")
    assert normalize_language_choice("spanish") == ("Spanish", "es")
    assert normalize_language_choice("4") == ("Spanish", "es")
    assert normalize_language_choice("deutsch") == ("German", "de")
    assert normalize_language_choice("Japanese") == ("Japanese", "ja")
    # Universal: Any world language supported
    assert normalize_language_choice("Vietnamese") == ("Vietnamese", "en")
    assert normalize_language_choice("Swahili") == ("Swahili", "en")

    h_en = get_localized_headers("English")
    h_hi = get_localized_headers("Hindi")
    h_hing = get_localized_headers("Hinglish")
    h_es = get_localized_headers("Spanish")
    assert "Real-World" in h_en["problem_title"]
    assert "वास्तविक" in h_hi["problem_title"]
    assert "Dard" in h_hing["problem_title"]
    assert "Problema" in h_es["problem_title"]
    print("   [OK] Universal multilingual engine & dictionary valid.")

    print("7. Testing multilingual markdown & HTML generation...")
    from oppscout.formatters import generate_individual_opportunity_markdown, generate_classical_html_report
    from oppscout.models import AnalysisReport
    p_hindi = UserProfile(
        name="Amit",
        hard_skills=["Python", "FastAPI"],
        location="Jaipur",
        unfair_advantages=["Fleet trucks connection"],
        language="Hindi"
    )
    md_hindi = generate_individual_opportunity_markdown(dossiers[0], p_hindi, 1)
    assert "वास्तविक जमीनी समस्या" in md_hindi or "Language: Hindi" in md_hindi

    with tempfile.TemporaryDirectory() as tmpdir:
        report = AnalysisReport(
            profile=p_hindi,
            generated_at="2026-09-16 12:00:00",
            total_signals_mined=len(dossiers),
            signals=[],
            opportunities=dossiers,
            executive_summary="Executive summary test"
        )
        html_file = Path(tmpdir) / "test.html"
        generate_classical_html_report(report, html_file)
        html_text = html_file.read_text(encoding="utf-8")
        assert '<html lang="hi">' in html_text
        assert "वास्तविक जमीनी समस्या" in html_text
    print("   [OK] Multilingual markdown and HTML report generation verified.")

    print("\n>>> ALL 7 CORE SUITES PASSED FLAWLESSLY! <<<")

if __name__ == "__main__":
    run()
