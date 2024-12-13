from typing import List, Dict, Any
from pydantic import BaseModel

class SampleCustomerDiscoveryResponse(BaseModel):
    """Sample response structure for customer discovery endpoint"""
    
    primary_domain: str = "Enterprise Software"
    total_market_size: int = 150000000000  # $150B
    niches: List[Dict[str, Any]] = [
        {
            "name": "Healthcare IT Solutions",
            "description": "Market niche in Enterprise Software domain",
            "market_size": 45000000000,  # $45B
            "growth_potential": 0.15,  # 15% annual growth
            "key_characteristics": [
                "Strict regulatory compliance requirements",
                "High security and privacy standards",
                "Integration with legacy systems",
                "24/7 operational requirements"
            ]
        },
        {
            "name": "Financial Services Software",
            "description": "Market niche in Enterprise Software domain",
            "market_size": 65000000000,  # $65B
            "growth_potential": 0.12,  # 12% annual growth
            "key_characteristics": [
                "Real-time processing capabilities",
                "Multi-currency support",
                "Advanced security features",
                "Regulatory compliance"
            ]
        }
    ]
    investor_sentiment: Dict[str, Any] = {
        "insights": """
        The Enterprise Software market shows strong growth potential through 2025.
        Key investment areas include AI/ML integration, cloud-native solutions,
        and cybersecurity. Venture capital funding remains robust with particular
        interest in SaaS platforms targeting specific vertical markets.
        """
    }
    ideal_customer_profile: Dict[str, Any] = {
        "insights": """
        Typical customer is a mid to large enterprise (1000+ employees)
        with a dedicated IT department, annual technology budget >$5M,
        and a digital transformation initiative in progress. Decision makers
        include CTO, CIO, and department heads with 6-12 month sales cycles.
        """
    }

class SampleCompetitiveAnalysisResponse(BaseModel):
    """Sample response structure for competitive analysis endpoint"""
    
    product_name: str = "Enterprise CRM Solution"
    competitors: List[Dict[str, Any]] = [
        {
            "name": "Market Leader CRM",
            "description": "Global leader in enterprise CRM solutions",
            "main_products": ["Sales Cloud", "Service Cloud", "Marketing Hub"],
            "target_market": "Large Enterprises",
            "key_differentiators": [
                "Extensive ecosystem",
                "Advanced AI capabilities",
                "Global presence"
            ]
        },
        {
            "name": "Innovative CRM",
            "description": "Cloud-native CRM for modern businesses",
            "main_products": ["Sales Suite", "Customer 360"],
            "target_market": "Mid-market companies",
            "key_differentiators": [
                "Modern UI/UX",
                "Quick implementation",
                "Competitive pricing"
            ]
        }
    ]
    derivatives: List[Dict[str, Any]] = [
        {
            "name": "Industry-Specific CRM",
            "description": "Specialized CRM for healthcare sector\nKey competitors: HealthCRM (HIPAA Compliance), MedicalSuite (Integration capabilities)",
            "target_market": "Healthcare providers"
        },
        {
            "name": "Mobile-First CRM",
            "description": "Lightweight CRM optimized for mobile teams\nKey competitors: MobileSales (Offline capabilities), FieldForce (GPS integration)",
            "target_market": "Field sales teams"
        }
    ]
