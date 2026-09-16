"""Model Context Protocol (MCP) Server for Opportunity Scout.
Exposes deep live market research, opportunity discovery, and technical architecture tools
to external AI agents (Claude Desktop, Antigravity, OpenRouter agents).
"""

import asyncio
import json
from mcp.server.fastmcp import FastMCP
from oppscout.analyzer import OpportunityAnalyzer
from oppscout.models import UserProfile
from oppscout.parser import extract_sections_heuristic
from oppscout.researcher import DeepMarketScraper
from oppscout.tools import generate_high_ticket_tech_blueprint, search_market_pain

mcp = FastMCP("OpportunityScout")


@mcp.tool()
async def discover_opportunities_from_markdown(markdown_content: str) -> str:
    """Discovers high-fit, unsexy, real-world business and tech opportunities from a user's markdown profile.
    Args:
        markdown_content: Freeform or structured markdown detailing skills, domain, location, and unfair advantages.
    """
    profile = extract_sections_heuristic(markdown_content)

    scraper = DeepMarketScraper()
    signals = await scraper.execute_deep_research(profile)
    await scraper.close()

    analyzer = OpportunityAnalyzer()
    report = await analyzer.analyze_and_synthesize(profile, signals)

    lines = [
        f"# Opportunity Scout Results for {profile.name} ({profile.location})",
        f"**Tech Profile:** {'Yes - High Ticket Tech Mode Activated' if profile.is_tech_user else 'No - Operational Agency/Concierge Mode'}",
        f"**Executive Summary:** {report.executive_summary}",
        "",
        "## Top Opportunities Mined:",
    ]
    for opp in report.opportunities:
        lines.append(f"### {opp.title} (Score: {opp.scores.composite_score}/100)")
        lines.append(f"- **Problem:** {opp.problem_statement}")
        lines.append(f"- **Target Customer:** {opp.target_customer}")
        lines.append(f"- **Earning Potential:** {opp.earning_potential}")
        lines.append(f"- **Founder Edge:** {opp.founder_advantage_explanation}")
        lines.append(f"- **Day-1 Validation:** {'; '.join(opp.day1_validation_plan)}")
        lines.append(f"- **Monetization:** {opp.monetization}")
        if opp.high_ticket_tech_blueprint:
            lines.append(f"- **Tech Architecture:** {opp.high_ticket_tech_blueprint}")
        lines.append("")

    return "\n".join(lines)


@mcp.tool()
async def live_research_market_pain(domain: str, query_type: str = "general") -> str:
    """Performs live scraping on Reddit, HackerNews and DuckDuckGo for authentic complaints and friction in a domain.
    Args:
        domain: Industry or sector (e.g. 'freight trucking', 'stone cutting', 'agritech cold storage').
        query_type: 'manual_workflows', 'regulatory_fines', 'cashflow_leaks', or 'general'.
    """
    signals = await search_market_pain(domain, query_type)
    if not signals:
        return f"No signals discovered for domain: {domain}"

    lines = [f"# Live Market Signals Mined for {domain} (Type: {query_type}):"]
    for s in signals:
        lines.append(f"- **[{s.get('source')}] {s.get('title')}**: {s.get('snippet')}")
        if s.get("url"):
            lines.append(f"  *URL: {s.get('url')}*")
    return "\n".join(lines)


@mcp.tool()
def get_high_ticket_tech_blueprint(problem_title: str, target_customer: str, skills: str) -> str:
    """Generates an enterprise-grade tech architecture, monthly recurring revenue plan, and acquisition playbook.
    Bans low-margin freelancing and delivers high-ticket B2B software strategy.
    Args:
        problem_title: The title of the problem being solved.
        target_customer: The exact business buyer persona.
        skills: Comma-separated list of developer's hard skills (e.g. 'Python, FastAPI, React, PostgreSQL').
    """
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    blueprint = generate_high_ticket_tech_blueprint(problem_title, target_customer, skill_list)
    return json.dumps(blueprint, indent=2)


def run_server():
    """Runs the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    run_server()
