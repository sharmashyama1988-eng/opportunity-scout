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

GEMINI_SYSTEM_PROMPT = """You are an elite Venture Partner, Principal Systems Architect, and B2B Operational Strategist.
Your sole mission is to analyze the founder's exact background, technical capabilities, location, and unfair network advantages, against live mined market pain signals, to discover 3 highly specific, non-obvious, unsexy B2B operational opportunities.

CRITICAL ARCHITECTURAL DIRECTIVES:
1. STRICT FOUNDER GROUNDING (Zero Generic Ideas):
   - Every opportunity MUST directly weaponize the founder's specific hard skills, published utilities, hardware/software stack, and unfair advantages.
   - If the founder has Systems, Desktop, Network, C++, Go, Windows API, or Microcontroller/Edge skills: Focus on enterprise network telemetry, bandwidth abuse monitoring, desktop asset sync acceleration, edge hardware watchdog diagnostics, or resilient multi-agent backoffice pipelines.
   - If the founder has Logistics, Freight, or Transportation footholds: Focus on E-Waybill detention, fuel reconciliation, demurrage, or proof-of-delivery.
   - If the founder has Manufacturing or Industrial processing footholds: Focus on batch shade variation, machine downtime, or scrap shrinkage.
   - NEVER output generic ideas: Ban generic CRMs, simple ChatGPT wrappers, food delivery, generic todo/social apps.

2. ANTI-FREELANCING HIGH-TICKET B2B TECH:
   - Strictly prohibit hourly freelancing (Fiverr/Upwork gigs).
   - Direct the founder to build high-margin software & automation infrastructure earning ₹1,50,000 to ₹4,00,000+ / month on recurring retainers or unkillable outcome-based contracts.

3. UNSEXY OPERATIONAL FRICTION & BLEEDING-NECK PAIN:
   - Target operations where businesses lose money daily: manual data entry errors, silent edge disconnects, bandwidth siphoning, compliance fines, lost paper proofs.

4. ZERO GUESSWORK EXECUTION BLUEPRINT:
   - Target Customer Avatar: Specific job title and facility/company type.
   - The Mom Test Script: Verbatim diagnostic opening question in the founder's requested language.
   - 48-Hour Day 1-3 Plan: Concrete ground audit (Day 1), concierge proof (Day 2), pre-order close (Day 3).
   - Explicit Pricing Formula: Monthly subscription or contingency fee.

5. NATIVE LANGUAGE FIDELITY:
   - Write the ENTIRE JSON response (titles, problem_statement, target_customer, current_workarounds, founder_advantage_explanation, day1_validation_plan, and monetization) natively and fluently in '{lang}'.
   - If '{lang}' is 'Hinglish': Use crisp, professional Roman Hindi mixed with English business/tech terms.
   - If '{lang}' is 'Hindi': Use natural, high-impact Devanagari script (हिन्दी).
   - If '{lang}' is English or any other language: Write in native, articulate professional phrasing.

6. STRICT JSON ARRAY OUTPUT:
   - Respond ONLY with a valid JSON array of 3 objects conforming to the OpportunityDossier schema.
"""


class OpportunityAnalyzer:
    """Evaluates mined market signals against the user's exact profile
    to generate bespoke, non-obvious business and technology opportunities.
    """

    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "nex-agi/nex-n2.5-pro:free")
        self.gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

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

    def _normalize_dossier_dict(self, item: dict, idx: int, profile: UserProfile) -> Optional[OpportunityDossier]:
        """Defensively normalizes and validates an LLM-generated dictionary into an OpportunityDossier."""
        if not isinstance(item, dict):
            return None
        try:
            opp_id = str(item.get("id") or f"opp-0{idx+1}")
            title = str(item.get("title") or f"B2B Operational Opportunity #{idx+1}").strip()
            problem_statement = str(
                item.get("problem_statement") or item.get("problem") or "Critical operational friction causing recurring margin leakage."
            ).strip()
            target_customer = str(item.get("target_customer") or item.get("customer") or "SMB and Enterprise Operators").strip()

            why_raw = item.get("why_it_is_real") or item.get("market_signals") or []
            if isinstance(why_raw, str):
                why_it_is_real = [s.strip() for s in why_raw.split("\n") if s.strip()] or [why_raw]
            elif isinstance(why_raw, list):
                why_it_is_real = [str(x).strip() for x in why_raw if str(x).strip()]
            else:
                why_it_is_real = ["Observed repeatedly across operational field audits and industry workflows."]
            if not why_it_is_real:
                why_it_is_real = ["Direct real-world friction observed in operator workflows."]

            current_workarounds = str(
                item.get("current_workarounds") or "Manual data copying across spreadsheets and informal messaging groups."
            ).strip()

            raw_scores = item.get("scores")
            if not isinstance(raw_scores, dict):
                raw_scores = {}

            def _to_int(val, default=9):
                try:
                    return max(1, min(10, int(val)))
                except Exception:
                    return default

            pain = _to_int(raw_scores.get("pain_intensity"), 9)
            wtp = _to_int(raw_scores.get("willingness_to_pay"), 9)
            fit = _to_int(raw_scores.get("founder_fit"), 10 if profile.unfair_advantages else 9)
            white = _to_int(raw_scores.get("whitespace"), 9)
            feas = _to_int(raw_scores.get("day1_feasibility"), 9)

            try:
                comp = float(raw_scores.get("composite_score", (pain * 3.0 + wtp * 2.5 + fit * 2.5 + white * 1.0 + feas * 1.0)))
            except Exception:
                comp = round(pain * 3.0 + wtp * 2.5 + fit * 2.5 + white * 1.0 + feas * 1.0, 1)
            comp = round(min(max(comp, 0.0), 99.0), 1)

            scores = OpportunityScores(
                pain_intensity=pain,
                willingness_to_pay=wtp,
                founder_fit=fit,
                whitespace=white,
                day1_feasibility=feas,
                composite_score=comp,
            )

            founder_advantage = str(
                item.get("founder_advantage_explanation")
                or item.get("founder_advantage")
                or f"Founder's direct technical execution capability in {', '.join(profile.hard_skills[:4])} creates a defensible edge."
            ).strip()

            plan_raw = item.get("day1_validation_plan") or item.get("validation_plan") or []
            if isinstance(plan_raw, str):
                day1_validation_plan = [s.strip() for s in plan_raw.split("\n") if s.strip()] or [plan_raw]
            elif isinstance(plan_raw, list):
                day1_validation_plan = [str(x).strip() for x in plan_raw if str(x).strip()]
            else:
                day1_validation_plan = ["Conduct 5 exploratory operator interviews using The Mom Test framework."]
            if not day1_validation_plan:
                day1_validation_plan = ["Conduct 5 exploratory operator interviews using The Mom Test framework."]

            stack_raw = item.get("mvp_tech_stack") or item.get("tech_stack") or []
            if isinstance(stack_raw, str):
                mvp_tech_stack = [s.strip() for s in stack_raw.split(",") if s.strip()] or [stack_raw]
            elif isinstance(stack_raw, list):
                mvp_tech_stack = [str(x).strip() for x in stack_raw if str(x).strip()]
            else:
                mvp_tech_stack = profile.hard_skills[:4] if profile.hard_skills else ["Python", "FastAPI"]
            if not mvp_tech_stack:
                mvp_tech_stack = profile.hard_skills[:4] if profile.hard_skills else ["Python", "FastAPI"]

            monetization = str(item.get("monetization") or "B2B SaaS retainer with upfront pilot deposit.").strip()
            earning = str(item.get("earning_potential") or "₹1,50,000 - ₹3,50,000 / month with 15-20 clients").strip()

            return OpportunityDossier(
                id=opp_id,
                title=title,
                problem_statement=problem_statement,
                target_customer=target_customer,
                why_it_is_real=why_it_is_real,
                current_workarounds=current_workarounds,
                scores=scores,
                founder_advantage_explanation=founder_advantage,
                is_high_ticket_tech=item.get("is_high_ticket_tech", True),
                high_ticket_tech_blueprint=item.get("high_ticket_tech_blueprint"),
                day1_validation_plan=day1_validation_plan,
                mvp_tech_stack=mvp_tech_stack,
                monetization=monetization,
                earning_potential=earning,
            )
        except Exception as err:
            logger.debug(f"Failed normalizing dossier item: {err}")
            return None


    async def _synthesize_with_gemini_direct(
        self, profile: UserProfile, signals: List[PainPointSignal]
    ) -> Optional[List[OpportunityDossier]]:
        """Direct high-speed call to Google's official Gemini API (e.g. gemini-2.5-flash)."""
        if not self.gemini_key:
            return None

        lang = profile.language or "English"
        signals_text = "\n".join([f"- [{s.source}] {s.title}: {s.snippet}" for s in signals[:6]])

        system_prompt = GEMINI_SYSTEM_PROMPT.replace("{lang}", lang)
        user_prompt = f"""FOUNDER STRATEGIC PROFILE:
- Name: {profile.name}
- Preferred Language: {lang}
- Hard Skills: {', '.join(profile.hard_skills)}
- Location: {profile.location}
- Unfair Advantages: {', '.join(profile.unfair_advantages)}
- Target Domains & Field: {', '.join(profile.domains)}

MINED REAL-WORLD PAIN SIGNALS (FROM DDGS, REDDIT & HACKERNEWS):
{signals_text}

Generate EXACTLY 3 bespoke, high-ticket B2B operational opportunities strictly grounded in this founder's exact skills and domains.
Output ONLY a valid JSON array of 3 objects conforming to the OpportunityDossier schema."""

        models_to_try = [self.gemini_model, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        models_to_try = list(dict.fromkeys([m for m in models_to_try if m]))

        for model in models_to_try:
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_key}"
            payload = {
                "systemInstruction": {
                    "parts": [{"text": system_prompt}]
                },
                "contents": [
                    {"role": "user", "parts": [{"text": user_prompt}]}
                ],
                "generationConfig": {
                    "temperature": 0.85,
                    "responseMimeType": "application/json"
                }
            }

            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=2.5)) as client:
                    resp = await client.post(endpoint, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                            json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
                            if json_match:
                                parsed = json.loads(json_match.group(0))
                            else:
                                parsed = json.loads(content)
                            dossiers = []
                            for idx, item in enumerate(parsed):
                                norm = self._normalize_dossier_dict(item, idx, profile)
                                if norm:
                                    dossiers.append(norm)
                            if len(dossiers) >= 3:
                                logger.info(f"Successfully synthesized with native Google Gemini API ({model})")
                                return dossiers[:3]
            except Exception as e:
                logger.debug(f"Gemini model {model} attempt failed: {e}")

        return None

    async def _synthesize_with_openrouter(
        self, profile: UserProfile, signals: List[PainPointSignal]
    ) -> Optional[List[OpportunityDossier]]:
        """Queries OpenRouter API with multi-model fallback cascade."""
        if not self.openrouter_key:
            return None

        lang = profile.language or "English"
        signals_text = "\n".join([f"- [{s.source}] {s.title}: {s.snippet}" for s in signals[:6]])

        system_prompt = GEMINI_SYSTEM_PROMPT.replace("{lang}", lang)
        user_prompt = f"""FOUNDER STRATEGIC PROFILE:
- Name: {profile.name}
- Preferred Language: {lang}
- Hard Skills: {', '.join(profile.hard_skills)}
- Location: {profile.location}
- Unfair Advantages: {', '.join(profile.unfair_advantages)}
- Target Domains & Field: {', '.join(profile.domains)}

MINED REAL-WORLD PAIN SIGNALS (FROM DDGS, REDDIT & HACKERNEWS):
{signals_text}

Generate EXACTLY 3 bespoke, high-ticket B2B operational opportunities strictly grounded in this founder's exact skills, domains, and geography.
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
]"""

        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": "https://github.com/opportunity-scout",
            "X-Title": "Opportunity Scout",
            "Content-Type": "application/json"
        }

        # Multi-model resilience: Fast, high-throughput models first
        candidate_models = [
            "nex-agi/nex-n2.5-pro:free",
            "nex-agi/nex-n2.5-mini:free",
            "nvidia/nemotron-3.5-lightning:free",
            "cohere/north-mini-code:free",
            "liquid/lfm-2.5-2.6b:free",
            "z-ai/glm-5.2:free",
            "google/gemma-4-26b-a4b-it:free",
        ]
        if self.openrouter_model and self.openrouter_model not in candidate_models:
            candidate_models.insert(0, self.openrouter_model)

        for model in candidate_models:
            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(8.0, connect=2.5)) as client:
                    payload = {
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.85,
                        "max_tokens": 1500
                    }
                    resp = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=payload
                    )
                    if resp.status_code == 200:
                        content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                        json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
                        if json_match:
                            parsed = json.loads(json_match.group(0))
                            dossiers = []
                            for idx, item in enumerate(parsed):
                                norm = self._normalize_dossier_dict(item, idx, profile)
                                if norm:
                                    dossiers.append(norm)
                            if len(dossiers) >= 3:
                                logger.info(f"Successfully synthesized with OpenRouter model {model}")
                                return dossiers[:3]
            except Exception as err:
                logger.debug(f"Model {model} attempt skipped: {err}")

        return None

    async def analyze_and_synthesize(
        self, profile: UserProfile, signals: List[PainPointSignal]
    ) -> AnalysisReport:
        """Synthesizes high-conviction opportunities using Native Gemini, OpenRouter, or Algorithmic Engine."""
        from datetime import datetime

        # 1. Attempt Native Google Gemini API first (gemini-2.5-flash)
        dossiers = await self._synthesize_with_gemini_direct(profile, signals)

        # 2. Attempt OpenRouter model cascade
        if not dossiers:
            dossiers = await self._synthesize_with_openrouter(profile, signals)

        # 3. Fallback to domain-tailored algorithmic engine
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
