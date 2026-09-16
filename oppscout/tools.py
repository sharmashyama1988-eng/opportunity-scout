"""Modular Research & Analysis Toolset.
These functions can be executed directly by CLI commands, automated pipelines,
or invoked as callable tools by AI agents (OpenRouter, Gemini, Claude Desktop via MCP).
"""

import asyncio
import logging
import re
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
import httpx
from oppscout.models import PainPointSignal, UserProfile

logger = logging.getLogger("oppscout.tools")


async def search_market_pain(domain: str, query_type: str = "general") -> List[Dict[str, Any]]:
    """Searches real-world forums and web results for painful operational bottlenecks in a domain.
    Args:
        domain: Industry or sector (e.g. 'trucking', 'marble manufacturing', 'retail pharmacy').
        query_type: 'manual_workflows', 'regulatory_fines', 'cashflow_leaks', or 'general'.
    """
    from oppscout.researcher import DeepMarketScraper
    scraper = DeepMarketScraper()

    try:
        if query_type == "manual_workflows":
            q = f'"{domain}" manual spreadsheet nightmare OR bottleneck'
        elif query_type == "regulatory_fines":
            q = f'"{domain}" penalty fine seizure compliance issue'
        elif query_type == "cashflow_leaks":
            q = f'"{domain}" invoice dispute payment delay theft loss'
        else:
            q = f'"{domain}" problem headache why is there no software'

        tasks = [
            scraper.scrape_reddit_discussions(domain, limit=3),
            scraper.scrape_hackernews_discussions(domain, limit=3),
            scraper.scrape_duckduckgo_deep(q, limit=3)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        signals = []
        for res in results:
            if isinstance(res, list):
                signals.extend(res)

        return [s.model_dump() for s in signals]
    finally:
        await scraper.close()


async def scrape_webpage_details(url: str) -> Dict[str, Any]:
    """Fetches a URL and extracts core pain point paragraphs, quotes, and metrics.
    Args:
        url: The web URL to crawl and inspect.
    """
    from oppscout.researcher import DeepMarketScraper
    scraper = DeepMarketScraper()
    try:
        content = await scraper.scrape_webpage_content(url)
        return {
            "url": url,
            "extracted_pain_content": content,
            "has_verifiable_quote": bool(content and len(content) > 50)
        }
    finally:
        await scraper.close()


def generate_high_ticket_tech_blueprint(
    problem_title: str,
    target_customer: str,
    skills: List[str]
) -> Dict[str, Any]:
    """Generates an enterprise-grade technical architecture and high-ticket pricing model
    specifically designed for developers/engineers to make serious recurring income (no freelancing).
    """
    skills_clean = [s.lower() for s in skills]

    # Detect stack capabilities
    has_python = any("python" in s for s in skills_clean) or any("fastapi" in s for s in skills_clean)
    has_js = any("react" in s or "next" in s or "node" in s or "typescript" in s for s in skills_clean)
    has_iot = any("iot" in s or "hardware" in s or "embedded" in s for s in skills_clean)

    if has_python and has_iot:
        arch_type = "Edge-to-Cloud Telemetry & Automation Hub"
        components = [
            "Hardware/Edge: ESP32 / GSM cellular telemetry unit logging sensors (temp, vibration, GPS) every 30s.",
            "Ingestion API: FastAPI async ingestion endpoints validating cryptographic signatures.",
            "Queue & Worker: Redis Streams + Celery workers processing anomaly thresholds in real-time.",
            "Alert Dispatcher: WhatsApp Cloud API webhook triggering alerts to operations heads within 2 seconds of anomaly.",
            "Storage: TimescaleDB / PostgreSQL for time-series operational audit logs."
        ]
    elif has_python:
        arch_type = "Autonomous Workflow & Reconciliation Pipeline"
        components = [
            "Data Ingestion: Python OCR service (Tesseract / Cloud Vision API) parsing WhatsApp receipt photos & PDFs.",
            "Reconciliation Engine: Polars / Pandas matching engine cross-referencing invoice amounts against bank & GST returns.",
            "API Layer: FastAPI REST/GraphQL service with role-based access control.",
            "Async Scheduler: APScheduler running nightly discrepancy sweeps at 11:30 PM.",
            "Storage: PostgreSQL with JSONB columns for flexible vendor invoice schemas."
        ]
    else:
        arch_type = "Cloud B2B Micro-SaaS Portal"
        components = [
            "Frontend: Next.js 15 App Router with Tailwind CSS & Shadcn UI.",
            "Backend: Node.js / Serverless Edge functions for instant latency.",
            "Database: Supabase (PostgreSQL + Row-Level Security).",
            "Notification Hub: Twilio / Meta WhatsApp Business API integration."
        ]

    pricing_models = [
        "Fixed Monthly Retainer: ₹9,999 to ₹24,999 / month per client facility.",
        "Usage Tier: ₹299 / month per active vehicle, machine, or warehouse dispatch desk.",
        "Value Contingency: 15% of caught fraudulent diesel slips or recovered disputed invoice claims."
    ]

    revenue_projections = {
        "5 Clients": "₹50,000 - ₹1,25,000 / month recurring",
        "15 Clients": "₹1,50,000 - ₹3,75,000 / month recurring",
        "30 Clients": "₹3,00,000 - ₹7,50,000 / month recurring"
    }

    acquisition_playbook = [
        f"Step 1: Do NOT launch on ProductHunt or Twitter. Your buyers ({target_customer}) are NOT on Twitter.",
        "Step 2: Physically visit their office or yard during non-peak hours (11:00 AM - 1:00 PM).",
        "Step 3: Ask to audit their last 1 week of manual slips for free as a trial pilot.",
        "Step 4: Show them the detected errors on your laptop screen and lock in a 6-month contract with 50% upfront."
    ]

    return {
        "architecture_name": arch_type,
        "system_components": components,
        "pricing_structures": pricing_models,
        "monthly_recurring_revenue": revenue_projections,
        "customer_acquisition_playbook": acquisition_playbook,
        "anti_freelancing_rule": "NEVER bill hourly. Always sell an unkillable business outcome."
    }
