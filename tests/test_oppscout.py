"""Comprehensive automated test suite for Opportunity Scout.
Verifies multi-format parsing, folder ingestion, deep research,
5-factor validation, tech blueprints, and reporting.
"""

import asyncio
from pathlib import Path
import unittest
from oppscout.analyzer import OpportunityAnalyzer
from oppscout.models import UserProfile
from oppscout.parser import (
    clean_file_path,
    extract_sections_heuristic,
    load_content_from_target,
    parse_target_path,
)
from oppscout.researcher import DeepMarketScraper
from oppscout.tools import generate_high_ticket_tech_blueprint, search_market_pain


def test_clean_file_path():
    """Verifies that Windows drag-and-drop artifacts are stripped properly."""
    # Test double quotes
    p1 = clean_file_path('"C:\\Users\\Test\\profile.md"')
    assert str(p1) == "C:\\Users\\Test\\profile.md"

    # Test single quotes
    p2 = clean_file_path("'F:\\data\\profile.pdf'")
    assert str(p2) == "F:\\data\\profile.pdf"

    # Test PowerShell call prefix & '...'
    p3 = clean_file_path("& 'F:\\data\\profile.docx'")
    assert str(p3) == "F:\\data\\profile.docx"

    # Test file:/// URL
    p4 = clean_file_path("file:///F:/data/notes.txt")
    assert "notes.txt" in str(p4)


def test_tech_detection_and_profile_extraction():
    """Verifies profile extraction and tech founder classification."""
    sample_text = """# Developer Profile
## Skills
Python, FastAPI, Docker, PostgreSQL, React
## Domain
Logistics & Freight
## Location
Jaipur
## Advantage
Uncle owns 30 trucks
"""
    profile = extract_sections_heuristic(sample_text)
    assert profile.is_tech_user is True
    assert "Python" in profile.hard_skills or "python" in [s.lower() for s in profile.hard_skills]
    assert profile.location.lower() == "jaipur"
    assert len(profile.unfair_advantages) > 0


def test_folder_ingestion(tmp_path):
    """Verifies that dropping a whole folder ingests all documents inside."""
    doc1 = tmp_path / "skills.md"
    doc1.write_text("# My Skills\nPython, Machine Learning", encoding="utf-8")

    doc2 = tmp_path / "notes.txt"
    doc2.write_text("Uncle owns stone cutting quarry in Makrana", encoding="utf-8")

    doc3 = tmp_path / "data.csv"
    doc3.write_text("TruckID,Route,Loss\nTR-01,Jaipur-Delhi,15000", encoding="utf-8")

    combined, files = load_content_from_target(tmp_path)
    assert len(files) == 3
    assert "Python" in combined
    assert "Makrana" in combined
    assert "TR-01" in combined

    profile, _ = parse_target_path(tmp_path)
    assert profile.is_tech_user is True
    assert len(profile.unfair_advantages) > 0


def test_high_ticket_tech_blueprint():
    """Verifies that tech blueprints ban low-margin freelancing and deliver B2B architecture."""
    blueprint = generate_high_ticket_tech_blueprint(
        "Autonomous Freight Toll & Diesel Reconciler",
        "Fleet Owners in Jaipur",
        ["Python", "FastAPI", "PostgreSQL", "IoT"]
    )
    assert "Edge-to-Cloud" in blueprint["architecture_name"] or "Autonomous" in blueprint["architecture_name"]
    assert "anti_freelancing_rule" in blueprint
    assert "monthly_recurring_revenue" in blueprint
    assert len(blueprint["customer_acquisition_playbook"]) >= 3


async def test_analyzer_scoring_and_dossiers():
    """Verifies that the 5-factor scoring engine and dossier generation work within mathematical bounds."""
    profile = UserProfile(
        name="Founder Rahul",
        hard_skills=["Python", "FastAPI", "PostgreSQL"],
        domains=["Logistics", "Trucking"],
        location="Jaipur",
        unfair_advantages=["Family owns 45 freight trucks"],
        is_tech_user=True
    )
    scraper = DeepMarketScraper()
    signals = scraper.get_curated_high_value_ground_truth(profile.domains, profile.location)
    await scraper.close()

    analyzer = OpportunityAnalyzer()
    report = await analyzer.analyze_and_synthesize(profile, signals)

    assert len(report.opportunities) >= 3
    for opp in report.opportunities:
        assert 1 <= opp.scores.pain_intensity <= 10
        assert 1 <= opp.scores.willingness_to_pay <= 10
        assert 1 <= opp.scores.founder_fit <= 10
        assert 1 <= opp.scores.whitespace <= 10
        assert 1 <= opp.scores.day1_feasibility <= 10
        assert 0.0 <= opp.scores.composite_score <= 100.0
        assert len(opp.day1_validation_plan) >= 3
        assert opp.is_high_ticket_tech is True
        assert opp.high_ticket_tech_blueprint is not None
