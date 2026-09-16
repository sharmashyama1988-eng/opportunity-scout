"""Data models for Opportunity Scout.
Defines schemas for UserProfile, PainPointSignal, OpportunityDossier, and AnalysisReport.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    name: Optional[str] = Field(default="Entrepreneur", description="User name or identifier")
    hard_skills: List[str] = Field(default_factory=list, description="Technical and domain-specific hard skills")
    soft_skills: List[str] = Field(default_factory=list, description="Interpersonal skills, negotiation, sales")
    domains: List[str] = Field(default_factory=list, description="Target industries, sectors, or domains")
    location: str = Field(default="Global", description="Geographic location or local market context")
    unfair_advantages: List[str] = Field(
        default_factory=list,
        description="Proprietary access, family business, industry connections, local proximity"
    )
    capital: str = Field(default="Bootstrapped / Low Capital", description="Available capital or financial constraints")
    time_commitment: str = Field(default="Full-time / Flexible", description="Available time per week")
    interests_and_notes: str = Field(default="", description="Additional unstructured observations and notes")
    raw_text: str = Field(default="", description="Original raw markdown/text input")
    is_tech_user: bool = Field(default=False, description="Whether the user possesses software, engineering, or IoT skills")
    language: str = Field(default="English", description="Target language for discovery, reports, and coaching")


class PainPointSignal(BaseModel):
    source: str = Field(..., description="Source platform (Reddit, HackerNews, DuckDuckGo, Forum)")
    title: str = Field(..., description="Thread title or document heading")
    url: str = Field(default="", description="Source link or URL")
    snippet: str = Field(..., description="Pain point excerpt or customer quote")
    pain_category: str = Field(default="Operational Bottleneck", description="Category of the friction")


class OpportunityScores(BaseModel):
    pain_intensity: int = Field(..., ge=1, le=10, description="1=Mild annoyance, 10=Bleeding neck disaster")
    willingness_to_pay: int = Field(..., ge=1, le=10, description="1=Expects free, 10=High commercial urgency")
    founder_fit: int = Field(..., ge=1, le=10, description="1=No relevant skills, 10=Unfair personal advantage")
    whitespace: int = Field(..., ge=1, le=10, description="1=Red ocean monopoly, 10=Underserved blue ocean")
    day1_feasibility: int = Field(..., ge=1, le=10, description="1=Requires $1M lab, 10=Can validate in 48 hours")
    composite_score: float = Field(..., ge=0.0, le=100.0, description="Weighted composite score (0-100)")


class OpportunityDossier(BaseModel):
    id: str = Field(..., description="Unique opportunity identifier")
    title: str = Field(..., description="Crisp opportunity title")
    problem_statement: str = Field(..., description="Exact real-world problem being suffered")
    target_customer: str = Field(..., description="Specific customer persona with purchasing power")
    why_it_is_real: List[str] = Field(default_factory=list, description="Ground truth market signals & evidence")
    current_workarounds: str = Field(..., description="Messy spreadsheets, WhatsApp chains, manual labor currently used")
    scores: OpportunityScores
    founder_advantage_explanation: str = Field(
        ..., description="Why the user's specific skills and network give them an unfair edge"
    )
    is_high_ticket_tech: bool = Field(
        default=True,
        description="True if this is a high-margin technology/SaaS product rather than low-end freelancing"
    )
    high_ticket_tech_blueprint: Optional[str] = Field(
        default=None,
        description="Deep product architecture, API flow, and scaling roadmap for tech founders to earn serious recurring revenue"
    )
    day1_validation_plan: List[str] = Field(
        default_factory=list, description="48-hour step-by-step validation without building heavy code"
    )
    mvp_tech_stack: List[str] = Field(
        default_factory=list, description="Lean tech stack tailored directly to user's hard skills"
    )
    monetization: str = Field(..., description="Pricing model and revenue mechanism")
    earning_potential: str = Field(
        default="₹1,00,000 - ₹2,50,000 / month with 10-15 clients",
        description="Realistic monthly recurring revenue potential"
    )


class AnalysisReport(BaseModel):
    profile: UserProfile
    generated_at: str
    total_signals_mined: int
    signals: List[PainPointSignal]
    opportunities: List[OpportunityDossier]
    executive_summary: str
