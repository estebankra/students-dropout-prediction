from typing import Dict

from pydantic import BaseModel


class RiskSummary(BaseModel):
    count: int
    percentage: float


class RiskSummaryResponse(BaseModel):
    high_risk: RiskSummary
    medium_risk: RiskSummary
    low_risk: RiskSummary


class DropoutDistributionResponse(BaseModel):
    total_students: int
    distribution: Dict[str, int]
    distribution_percentages: Dict[str, float]
    risk_summary: RiskSummaryResponse


class FacultyDropoutDistributionResponse(BaseModel):
    faculty_distributions: Dict[str, Dict[str, int]]


class FactorImpactItem(BaseModel):
    factor: str
    impact_score: float
    description: str


class DropoutFactorsImpactResponse(BaseModel):
    factors: list[FactorImpactItem]
    total_students_analyzed: int
