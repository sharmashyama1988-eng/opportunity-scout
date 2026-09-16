"""Interactive Explanation & Execution Coach for Opportunity Scout.
Breaks down dossiers conversationally, coaches the founder on customer meetings,
handles objections, and explains how to extract payment before writing heavy code.
"""

import os
from typing import Optional
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from oppscout.languages import get_localized_headers
from oppscout.models import OpportunityDossier, UserProfile

console = Console()


def explain_opportunity_in_detail(opp: OpportunityDossier, profile: UserProfile):
    """Provides a comprehensive, conversational breakdown of the selected opportunity in the user's chosen language."""
    lang = profile.language or "English"
    lh = get_localized_headers(lang)

    title = f"STRATEGIC BREAKDOWN ({lang}): {opp.title}"

    content = Text()
    content.append(f"1. {lh['problem_title'].upper()}:\n", style="bold red")
    content.append(f"{opp.problem_statement}\n\n", style="white")
    content.append("Market Reality & Evidence:\n", style="bold dim")
    for ev in opp.why_it_is_real:
        content.append(f"  • {ev}\n", style="dim")
    content.append("\n")

    content.append(f"2. {lh['mom_test_title'].upper()}:\n", style="bold yellow")
    content.append(f"{lh['mom_test_intro']}\n", style="italic")
    script = lh['mom_test_question'].format(target=opp.target_customer, location=profile.location)
    content.append(f'  \"{script}\"\n\n', style="bright_yellow")

    content.append(f"3. OBJECTION HANDLING:\n", style="bold magenta")
    content.append(f"{lh['objection_intro']}\n", style="dim")
    content.append("Counter-Punch:\n", style="bold bright_white")
    content.append(f'  \"{lh["objection_counter"]}\"\n\n', style="bright_magenta")

    content.append(f"4. {lh['validation_title'].upper()}:\n", style="bold green")
    for step in opp.day1_validation_plan:
        content.append(f"  • {step}\n", style="bright_green")
    content.append("\n")

    if opp.is_high_ticket_tech and opp.high_ticket_tech_blueprint:
        content.append(f"5. {lh['tech_blueprint_title'].upper()}:\n", style="bold cyan")
        content.append(f"{lh['earning_title']}: {opp.earning_potential}\n", style="bold bright_green")
        content.append(f"{opp.high_ticket_tech_blueprint}\n\n", style="cyan")

    content.append(f"6. {lh['monetization_title'].upper()}:\n", style="bold gold1")
    content.append(f"{opp.monetization}\n", style="bright_white")

    console.print()
    console.print(Panel(content, title=f"[bold gold1]{title}[/bold gold1]", border_style="gold1"))


async def answer_founder_question(question: str, opp: OpportunityDossier, profile: UserProfile):
    """Answers any custom questions or doubts asked by the founder using OpenRouter or local intelligence."""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free")
    lang = profile.language or "English"

    console.print(f"\n[bold cyan]Consulting execution intelligence ({lang}) on:[/bold cyan] '{question}'...\n")

    if openrouter_key:
        prompt = f"""You are a master venture architect and high-ticket B2B execution mentor.
A founder is evaluating this real-world business/technology opportunity and asked a specific question.
CRITICAL LANGUAGE DIRECTIVE: Provide a crisp, battle-tested, pragmatic answer in 3-4 bullet points STRICTLY IN {lang}.
Ensure high-impact, natural, fluent phrasing in {lang}.
Focus on: Zero-budget bootstrapping, boots-on-the-ground execution, getting paid upfront, and avoiding time-wasting.

OPPORTUNITY:
- Title: {opp.title}
- Problem: {opp.problem_statement}
- Customer: {opp.target_customer}
- Current Workaround: {opp.current_workarounds}
- Founder Skills: {', '.join(profile.hard_skills)}
- Founder Advantage: {profile.unfair_advantages[0] if profile.unfair_advantages else 'Local boots on ground'}

FOUNDER QUESTION:
"{question}"
"""
        headers = {
            "Authorization": f"Bearer {openrouter_key}",
            "HTTP-Referer": "https://github.com/opportunity-scout",
            "X-Title": "Opportunity Scout",
            "Content-Type": "application/json"
        }
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                resp = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3,
                        "max_tokens": 400
                    }
                )
                if resp.status_code == 200:
                    ans = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    console.print(Panel(ans, title=f"[bold green]EXECUTIVE ADVICE ({lang})[/bold green]", border_style="green"))
                    return
        except Exception:
            pass

    # Heuristic Fallback Answer localized
    adv = profile.unfair_advantages[0] if profile.unfair_advantages else "network"
    if "hinglish" in lang.lower():
        fallback_text = (
            f"1. **Validation Pehle**: 2 mahine lagakar bina customer ke code mat likho. Apne advantage ({adv}) ka use karke 2 real letters of intent lo.\n"
            f"2. **Concierge Hack**: Day 1 par problem ko manually solve karo WhatsApp ya sheets se, jab tak customer payment na kare tab tak heavy backend mat banao.\n"
            f"3. **Payment Commitment**: Agar customer ₹5,000 ka advance commitment deposit nahi deta, toh software banne par bhi use nahi karega.\n"
            f"4. **Anti-Freelancing**: Intellectual property (IP) aapka rahega. Kabhi hourly billing mat karna."
        )
    elif "hindi" in lang.lower():
        fallback_text = (
            f"1. **सत्यापन पहले**: बिना वास्तविक ग्राहक के महीनों कोड न लिखें। अपने संपर्क लाभ ({adv}) से 2 वास्तविक सहमति पत्र प्राप्त करें।\n"
            f"2. **मैनुअल समाधान**: पहले दिन प्रक्रिया को मैन्युअल या व्हाट्सऐप से संभालें जब तक ग्राहक अग्रिम भुगतान न कर दे।\n"
            f"3. **अग्रिम प्रतिबद्धता**: यदि ग्राहक छोटा अग्रिम टोकन भी नहीं देता, तो वह बाद में भी सेवा नहीं खरीदेगा।\n"
            f"4. **नो-फ्रीलांसिंग**: बौद्धिक संपदा (IP) आपकी अपनी होगी। प्रति घंटा दर पर कभी काम न करें।"
        )
    else:
        fallback_text = (
            f"1. **Validation First**: Don't build code for 2 months without commitment. Leverage your advantage ({adv}) to secure 2 letters of intent.\n"
            f"2. **The Concierge Hack**: Solve the problem manually on day 1 with spreadsheets or WhatsApp before building backend services.\n"
            f"3. **Payment Commitment**: If a customer won't give a deposit, they won't use the software when built. Protect your time!\n"
            f"4. **Anti-Freelancing**: You own the intellectual property (IP). Never charge hourly rates."
        )
    console.print(Panel(fallback_text, title=f"[bold green]PRAGMATIC EXECUTION ADVICE ({lang})[/bold green]", border_style="green"))

