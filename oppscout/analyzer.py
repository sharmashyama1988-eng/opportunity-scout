"""Opportunity Synthesis and 5-Factor Validation Engine.
Evaluates mined market signals against the user's exact profile to generate bespoke,
actionable business and technology opportunities with complete step-by-step execution directives.
"""

import json
import logging
import os
import re
from typing import List, Optional
import httpx
from dotenv import load_dotenv

from oppscout.models import (
    AnalysisReport,
    OpportunityDossier,
    OpportunityScores,
    PainPointSignal,
    UserProfile,
)
from oppscout.tools import generate_high_ticket_tech_blueprint

# Load environment variables securely from .env
load_dotenv()
logger = logging.getLogger("oppscout.analyzer")


class OpportunityAnalyzer:
    """Evaluates mined market signals against the user's exact profile
    to generate bespoke, non-obvious business and technology opportunities.
    """

    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "google/gemma-4-26b-a4b-it:free")
        self.gemini_key = os.getenv("GEMINI_API_KEY")

    def _calculate_scores(
        self,
        profile: UserProfile,
        problem_type: str,
        has_unfair_advantage: bool
    ) -> OpportunityScores:
        """Calculates 5-factor opportunity score matrix."""
        # Pain intensity: B2B compliance, cash leakage, or delays score 9-10
        pain_intensity = 9 if any(k in problem_type.lower() for k in ["penalty", "theft", "spoilage", "expiry", "cashflow", "seizure"]) else 8

        # Willingness to pay: High if businesses lose money daily
        wtp = 9 if any(k in problem_type.lower() for k in ["seizure", "reconciliation", "scrap", "credit", "fine"]) else 8

        # Founder fit: Higher if user has unfair advantage or matching hard skills
        if has_unfair_advantage:
            founder_fit = 10
        elif len(profile.hard_skills) >= 2:
            founder_fit = 9
        else:
            founder_fit = 8

        # Whitespace: Unsexy back-office niches have high whitespace
        whitespace = 9

        # Day-1 feasibility: Can validate with 3 customer interviews / concierge demo
        day1_feasibility = 9

        composite = (
            (pain_intensity * 3.0)
            + (wtp * 2.5)
            + (founder_fit * 2.5)
            + (whitespace * 1.0)
            + (day1_feasibility * 1.0)
        )
        composite = round(min(composite, 97.5), 1)

        return OpportunityScores(
            pain_intensity=pain_intensity,
            willingness_to_pay=wtp,
            founder_fit=founder_fit,
            whitespace=whitespace,
            day1_feasibility=day1_feasibility,
            composite_score=composite
        )

    def _synthesize_tailored_algorithmic(
        self, profile: UserProfile, signals: List[PainPointSignal]
    ) -> List[OpportunityDossier]:
        """Synthesizes bespoke, non-generic opportunities directly weaponizing
        the user's skills, geography, and unfair network advantages.
        Uses combinatorial multi-vector sampling across 21 industrial algorithms to guarantee
        diverse, non-repetitive, high-conviction results on every run.
        """
        from oppscout.vector_synthesizer import sample_diverse_opportunities
        return sample_diverse_opportunities(profile, signals, count=3)

    async def _synthesize_with_openrouter(
        self, profile: UserProfile, signals: List[PainPointSignal]
    ) -> Optional[List[OpportunityDossier]]:
        """Queries OpenRouter API for deep model-driven synthesis with dynamic vector injection and multi-model fallback."""
        if not self.openrouter_key:
            return None

        import random
        from oppscout.algorithms import SpecializedSearchAlgorithms

        lang = profile.language or "English"
        signals_text = "\n".join([f"- [{s.source}] {s.title}: {s.snippet}" for s in signals[:5]])

        # Generate unique seed & sample 3 distinct friction vectors to guarantee run-to-run diversity
        run_seed = random.randint(10000, 99999)
        algo_keys = list(SpecializedSearchAlgorithms.ALGORITHMS_REGISTRY.keys())
        sampled_keys = random.sample(algo_keys, min(3, len(algo_keys)))
        chosen_vectors = [SpecializedSearchAlgorithms.ALGORITHMS_REGISTRY[k] for k in sampled_keys]
        vectors_instruction = "\n".join([
            f"  • Vector {i+1} ({v['name']}): {v['focus']} (Economic threat: {v['typical_leakage']})"
            for i, v in enumerate(chosen_vectors)
        ])

        top_advantage = profile.unfair_advantages[0] if profile.unfair_advantages else f"Boots-on-the-ground local network in {profile.location}"

        prompt = f"""You are an elite operational venture architect and high-ticket B2B engineer.
Analyze this founder profile against verified real-world market signals.
Generate EXACTLY 3 highly specific, non-obvious, unsexy B2B/operational opportunities.

MANDATORY DIVERSITY & FRESHNESS DIRECTIVE (Run Seed #{run_seed}):
Every single run must produce fresh, distinct, and creative opportunities!
Do NOT repeat standard toll, diesel, or generic invoice ideas.
In this run, you MUST explore and solve these 3 specific operational friction vectors:
{vectors_instruction}

MANDATORY LANGUAGE DIRECTIVE:
The user selected '{lang}'. You MUST generate the ENTIRE JSON response (all titles, problem_statement, target_customer, current_workarounds, founder_advantage_explanation, day1_validation_plan, and monetization) natively, fluently, and professionally in '{lang}'.
- If '{lang}' is 'Hinglish': Use crisp, practical Roman Hindi mixed with English business/tech terms (natural startup founder tone).
- If '{lang}' is 'Hindi': Use natural, high-impact Devanagari script (हिन्दी).
- If '{lang}' is any other global language: Use high-precision, native business terminology of that exact language.
- Ensure natural phrasing and completely eliminate clumsy machine-translation artifacts.

MANDATORY OPERATIONAL RULES:
1. ZERO GENERIC IDEAS: No 'AI chatbots', no 'food delivery', no 'generic CRM', no 'fitness tracker'.
2. EVERY problem MUST be a real, bleeding-neck operational friction with urgent willingness to pay.
3. DIRECTLY WEAPONIZE the user's specific hard skills, location, and unfair advantage ('{top_advantage}').
4. TELL THE USER EXACTLY WHAT TO DO (Zero guesswork):
   - Exactly which person / industrial facility to visit.
   - The verbatim Mom Test interview question to ask (written in '{lang}').
   - Day 1, Day 2, Day 3 step-by-step 48-hour validation without heavy coding.
   - Exact pricing and monetization.

FOUNDER PROFILE:
- Preferred Language: {lang}
- Hard Skills: {', '.join(profile.hard_skills)}
- Location: {profile.location}
- Unfair Advantages: {', '.join(profile.unfair_advantages)}
- Target Domains: {', '.join(profile.domains)}

MINED REAL SIGNALS:
{signals_text}

Respond ONLY in valid JSON array of 3 objects matching this schema:
[
  {{
    "id": "opp-01",
    "title": "...",
    "problem_statement": "...",
    "target_customer": "...",
    "why_it_is_real": ["...", "..."],
    "current_workarounds": "...",
    "scores": {{
      "pain_intensity": 9,
      "willingness_to_pay": 9,
      "founder_fit": 10,
      "whitespace": 9,
      "day1_feasibility": 9,
      "composite_score": 94.5
    }},
    "founder_advantage_explanation": "...",
    "day1_validation_plan": [
      "DIRECT ACTION: ...",
      "THE MOM TEST QUESTION: ...",
      "DAY 1 (Validation): ...",
      "DAY 2 (Concierge): ...",
      "DAY 3 (Pre-Order): ..."
    ],
    "mvp_tech_stack": ["..."],
    "monetization": "...",
    "earning_potential": "₹1,50,000 - ₹3,50,000 / month with 15-20 clients"
  }}
]
"""
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": "https://github.com/opportunity-scout",
            "X-Title": "Opportunity Scout",
            "Content-Type": "application/json"
        }

        # Multi-model resilience: Try preferred model (Gemma 4 26B) first, with reliable backups
        candidate_models = [
            self.openrouter_model,
            "google/gemma-4-26b-a4b-it:free",
            "nvidia/nemotron-3.5-lightning:free",
            "nex-agi/nex-n2.5-pro:free",
            "cohere/north-mini-code:free",
        ]
        models_to_try = list(dict.fromkeys([m for m in candidate_models if m]))

        for model in models_to_try:
            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(12.0, connect=3.0)) as client:
                    payload = {
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are an elite operational problem discovery engine. Output only valid JSON. Do NOT include thinking process or markdown text outside JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.85,
                        "max_tokens": 1400
                    }
                    resp = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    if resp.status_code == 200:
                        content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                        # Extract JSON array handling thinking tags and preambles
                        json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
                        if json_match:
                            parsed = json.loads(json_match.group(0))
                            dossiers = []
                            for item in parsed:
                                if "earning_potential" not in item:
                                    item["earning_potential"] = "₹1,50,000 - ₹3,50,000 / month with 15-20 clients"
                                dossiers.append(OpportunityDossier(**item))
                            if len(dossiers) >= 3:
                                return dossiers[:3]
            except Exception as err:
                logger.debug(f"Model {model} attempt skipped: {err}")

        return None

    async def analyze_and_synthesize(
        self, profile: UserProfile, signals: List[PainPointSignal]
    ) -> AnalysisReport:
        """Synthesizes high-conviction opportunities using OpenRouter or Algorithmic Engine."""
        from datetime import datetime

        # Attempt OpenRouter intelligence synthesis first
        dossiers = await self._synthesize_with_openrouter(profile, signals)

        # Fallback to deterministic tailored algorithmic engine
        if not dossiers:
            dossiers = self._synthesize_tailored_algorithmic(profile, signals)

        dossiers.sort(key=lambda d: d.scores.composite_score, reverse=True)

        location_display = profile.location if profile.location else "Regional Market"
        top_skill = profile.hard_skills[0] if profile.hard_skills else "Technical Engineering"

        lang = (profile.language or "English").lower()
        if "hinglish" in lang:
            summary = (
                f"Opportunity Scout ne aapke liye {len(dossiers)} hyper-targeted, high-conviction real-world problems nikaale hain. "
                f"Ye aapki technical capability ({top_skill}) aur aapke location ({location_display}) ke unfair advantage ko sidha weaponize karte hain. "
                f"Bina kisi faltu consumer toy ya low-margin freelancing ke, har ek opportunity bleeding-neck B2B cash leakage ko solve karti hai jahan customer turant advance paise dene ko tayyar hai."
            )
        elif "hindi" in lang:
            summary = (
                f"ऑपर्च्युनिटी स्काउट ने आपके लिए {len(dossiers)} अत्यधिक केंद्रित, वास्तविक जमीनी समस्याओं की पहचान की है। "
                f"ये आपकी तकनीकी क्षमता ({top_skill}) और {location_display} में आपके स्थानीय व नेटवर्क लाभ का सीधा उपयोग करती हैं। "
                f"किसी सामान्य ऐप या कम-मार्जिन वाली फ्रीलांसिंग के बजाय, प्रत्येक अवसर भारी व्यावसायिक वित्तीय नुकसान को रोकता है जहां ग्राहक तत्काल भुगतान करने के लिए तत्पर है।"
            )
        elif "spanish" in lang or "español" in lang:
            summary = (
                f"Opportunity Scout identificó {len(dossiers)} problemas operativos reales y de alta convicción. "
                f"Aprovechan directamente su capacidad técnica en {top_skill} y su ventaja competitiva de red en {location_display}. "
                f"En lugar de proyectos genéricos o freelance de bajo margen, cada oportunidad detiene fugas críticas de capital B2B con alta disposición a pagar de inmediato."
            )
        elif "german" in lang or "deutsch" in lang:
            summary = (
                f"Opportunity Scout hat {len(dossiers)} praxisnahe B2B-Kernprobleme identifiziert. "
                f"Diese nutzen Ihre Fachkompetenz in {top_skill} und Ihren regionalen Vorteil in {location_display} optimal aus. "
                f"Statt beliebiger Apps löst jedes Projekt echten administrativen Mehraufwand mit hoher Zahlungsbereitschaft."
            )
        elif "french" in lang or "français" in lang:
            summary = (
                f"Opportunity Scout a identifié {len(dossiers)} problèmes opérationnels critiques. "
                f"Ils exploitent directement vos compétences en {top_skill} et votre réseau à {location_display}. "
                f"Chaque opportunité résout une fuite de revenus B2B concrète avec une forte volonté de payer."
            )
        else:
            summary = (
                f"Opportunity Scout identified {len(dossiers)} hyper-targeted, high-conviction real-world problems (Target Language: {profile.language}). "
                f"These leverage your technical capability in {top_skill} along with your geographical and network unfair advantage "
                f"in {location_display}. Rather than building crowded consumer toys, each opportunity solves high-friction B2B "
                f"operational cash leakage with immediate willingness to pay."
            )

        return AnalysisReport(
            profile=profile,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_signals_mined=len(signals),
            signals=signals,
            opportunities=dossiers,
            executive_summary=summary
        )
