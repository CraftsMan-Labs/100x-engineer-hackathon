from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class CompetitorData(BaseModel):
    """Structured competitor information"""
    name: str
    description: str
    key_differentiators: List[str]

class DerivativeData(BaseModel):
    """Structured derivative product information"""
    name: str
    description: str
    target_market: str

class CustomerData(BaseModel):
    """Structured customer discovery data"""
    primary_domain: str
    total_market_size: int
    ideal_customer_profile: Dict[str, Any]
    niches: List[Dict[str, str]]

class MarketData(BaseModel):
    """Structured market analysis data"""
    original_query: str
    comprehensive_report: str

class ExpansionData(BaseModel):
    """Structured market expansion data"""
    expansion_domains: List[str]
    strategic_rationale: Dict[str, str]
    potential_synergies: List[str]

class CompetitiveData(BaseModel):
    """Structured competitive intelligence data"""
    product_name: str
    competitors: List[CompetitorData]
    derivatives: List[DerivativeData]

class ProductPhase(BaseModel):
    """Structured product evolution phase"""
    name: str
    description: str
    key_features: List[str]
    value_proposition: str

class EvolutionData(BaseModel):
    """Structured product evolution data"""
    overall_vision: str
    long_term_goals: List[str]
    phases: List[ProductPhase]
    visuals: Optional[Dict[str, Any]] = None

class UnifiedResults(BaseModel):
    """Complete unified analysis results"""
    status: str = "completed"
    sections: Dict[str, Any]
    domain: str
    unified_report: Optional[Dict[str, Any]] = None
