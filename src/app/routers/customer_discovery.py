from typing import List, Dict, Any
from pydantic import BaseModel
from app.llm import LiteLLMKit
from app.jina import JinaReader
from app.exa import ExaAPI
from app.config import get_settings
from app.schemas.llm import ChatRequest, Message
from app.routers.prompts import generate_high_level_query_prompt, identify_market_niches_prompt,generate_niche_search_query

from fastapi import APIRouter


class CustomerNiche(BaseModel):
    """Represents a specific customer niche"""

    name: str
    description: str
    search_query: str
    search_results: List[str]
    market_size: int = 0
    growth_potential: float = 0.0
    key_characteristics: List[str] = []


class MarketTrendAnalysis(BaseModel):
    """Detailed market trend analysis"""
    
    historical_data: Dict[str, Any]
    growth_trajectory: Dict[str, float]
    key_inflection_points: List[Dict[str, Any]]
    predictive_insights: Dict[str, Any]
    visualization_data: Dict[str, Any]

class CustomerDiscoveryReport(BaseModel):
    """Comprehensive customer discovery report"""

    primary_domain: str
    total_market_size: int
    niches: List[CustomerNiche]
    ideal_customer_profile: Dict[str, Any]
    market_trends: MarketTrendAnalysis
    investor_sentiment: Dict[str, Any]


class IdentifyMarketNiche(BaseModel):
    niches: List[str]


class CustomerDiscoverer:
    """Advanced customer discovery and market segmentation tool"""

    def __init__(
        self, domain: str, llm_model: str = "gpt-4o", temperature: float = 0.7
    ):
        """Initialize Customer Discoverer with LLM and external search APIs"""
        self.settings = get_settings()
        self.llm = LiteLLMKit(model_name=llm_model, temperature=temperature)
        self.jina = JinaReader(self.settings.JINA_API_KEY)
        self.exa = ExaAPI(self.settings.EXA_API_KEY)

        self.domain = domain
        self.niches: List[CustomerNiche] = []
        self.comprehensive_report: CustomerDiscoveryReport | None

    def generate_high_level_query(self) -> str:
        """Generate a high-level market research query"""
        prompt = generate_high_level_query_prompt(self.domain)
        return self.llm.generate(
            ChatRequest(messages=[Message(role="user", content=prompt)])
        )

    def identify_market_niches(self, high_level_query: str) -> List[str]:
        """Identify potential market niches within the domain"""
        prompt = identify_market_niches_prompt(high_level_query, self.domain)
        niches_response = self.llm.generate(
            ChatRequest(
                messages=[Message(role="user", content=prompt)],
            ),
            response_format=IdentifyMarketNiche,
        )
        niches = IdentifyMarketNiche(**niches_response).niches
        return niches

    def generate_niche_search_query(self, niche: str) -> str:
        """Generate a targeted search query for a specific niche"""
        prompt = generate_niche_search_query(niche,self.domain)
        return self.llm.generate(
            ChatRequest(messages=[Message(role="user", content=prompt)])
        )

    def search_niche_market(self, niche: str, search_query: str) -> CustomerNiche:
        """Perform comprehensive market research for a specific niche"""
        # Use Exa and Jina for diverse internet search
        try:
            search_contents = self.exa.search_and_contents(search_query)
            search_results = [
                search_contents.results[i].text
                for i in range(len(search_contents.results))
            ]
            search_results_str = " \n".join(search_results)

        except Exception as e:
            print(f"Exa search failed: {e}, falling back to Jina")
            search_results_str = self.jina.search(search_query)

        # Analyze search results
        analysis_prompt = f"""
        Analyze the search results for the niche '{niche}' in the {self.domain} domain.
        Provide insights on:
        1. Market size
        2. Growth potential
        3. Key customer characteristics
        4. Emerging trends
        """
        niche_analysis = self.llm.generate(
            ChatRequest(
                messages=[
                    Message(role="user", content=analysis_prompt),
                    Message(role="system", content=search_results_str),
                ]
            )
        )

        return CustomerNiche(
            name=niche,
            description=niche_analysis,
            search_query=search_query,
            search_results=[search_results_str],
        )

    def search_market_for_year(self, year: int) -> Dict[str, Any]:
        """Perform targeted market search for a specific year"""
        market_year_query = f"""
        Analyze the {self.domain} market for the year {year} with focus on:
        1. Market size and economic indicators
        2. Technological innovations
        3. Key market disruptions
        4. Regulatory landscape
        5. Investment and funding trends
        6. Competitive dynamics
        """
        
        # Perform search using multiple sources
        try:
            search_contents = self.exa.search_and_contents(market_year_query)
            search_results = [
                search_contents.results[i].text
                for i in range(len(search_contents.results))
            ]
            search_results_str = " \n".join(search_results)
        except Exception as e:
            print(f"Exa search failed for {year}: {e}, falling back to Jina")
            search_results_str = self.jina.search(market_year_query)

        # Analyze and structure the search results
        analysis_prompt = f"""
        Comprehensively analyze the search results for the {self.domain} market in {year}.
        Provide a structured analysis covering:
        - Market size and growth
        - Key technological developments
        - Major market events
        - Investment trends
        - Competitive landscape shifts
        """
        
        year_analysis = self.llm.generate(
            ChatRequest(
                messages=[
                    Message(role="user", content=analysis_prompt),
                    Message(role="system", content=search_results_str),
                ]
            )
        )

        return {
            "year": year,
            "analysis": year_analysis,
            "raw_search_results": search_results
        }

    def compile_comprehensive_report(self):
        """Compile a comprehensive customer discovery report with year-by-year analysis"""
        # Perform year-specific market searches
        years = list(range(2019, 2025))
        yearly_market_insights = [self.search_market_for_year(year) for year in years]

        # Generate investor sentiment
        investor_sentiment_query = f"""
        Research investor sentiment and future outlook for the {self.domain} domain.
        Include perspectives from top consulting firms like McKinsey, BCG, and Bain.
        """
        investor_insights = self.llm.generate(
            ChatRequest(
                messages=[Message(role="user", content=investor_sentiment_query)]
            )
        )

        # Generate ideal customer profile
        ideal_customer_profile_query = f"""
        Based on the market research for the {self.domain} domain, 
        develop a comprehensive ideal customer profile. 
        Include:
        1. Demographic characteristics
        2. Psychographic traits
        3. Pain points and challenges
        4. Buying behaviors
        5. Technology adoption levels
        6. Decision-making process
        """
        ideal_customer_insights = self.llm.generate(
            ChatRequest(
                messages=[Message(role="user", content=ideal_customer_profile_query)]
            )
        )

        # Compile comprehensive market trends analysis
        market_trends_compilation_query = f"""
        Synthesize the year-by-year market insights for the {self.domain} domain.
        Create a comprehensive analysis that:
        1. Identifies overarching trends
        2. Highlights key inflection points
        3. Provides predictive insights
        4. Suggests visualization strategies
        """
        
        market_trends_insights = self.llm.generate(
            ChatRequest(
                messages=[
                    Message(role="user", content=market_trends_compilation_query),
                    Message(role="system", content=str(yearly_market_insights))
                ]
            )
        )

        # Parse the market trends insights
        try:
            parsed_trends = self.llm.generate(
                ChatRequest(messages=[
                    Message(role="system", content="Parse the following market trends into a structured JSON format"),
                    Message(role="user", content=market_trends_insights)
                ]),
                response_format=MarketTrendAnalysis
            )
        except Exception as e:
            # Fallback to a basic structure if parsing fails
            parsed_trends = MarketTrendAnalysis(
                historical_data={year_insight['year']: year_insight['analysis'] for year_insight in yearly_market_insights},
                growth_trajectory={},
                key_inflection_points=[],
                predictive_insights={},
                visualization_data={}
            )

        self.comprehensive_report = CustomerDiscoveryReport(
            primary_domain=self.domain,
            total_market_size=sum(niche.market_size for niche in self.niches),
            niches=self.niches,
            investor_sentiment={"insights": investor_insights},
            ideal_customer_profile={"insights": ideal_customer_insights},
            market_trends=parsed_trends,
        )

    def discover(self):
        """Execute full customer discovery workflow"""
        print(f"Initiating customer discovery for domain: {self.domain}...")
        high_level_query = self.generate_high_level_query()
        print(f"High-level query: {high_level_query}")
        niches = self.identify_market_niches(high_level_query)
        print(f"Identified niches: {niches}")

        for niche in niches[:10]:  # Limit to 10 niches
            search_query = self.generate_niche_search_query(niche)
            print(f"Search query for '{niche}': {search_query}")
            niche_details = self.search_niche_market(niche, search_query)
            print(f"Details for '{niche}': {niche_details}")
            self.niches.append(niche_details)

        print("Compiling comprehensive report...")

        self.compile_comprehensive_report()
        return self.comprehensive_report


router = APIRouter(prefix="/customer-discovery", tags=["customer_discovery"])


@router.post("/discover")
def customer_discovery_endpoint(domain: str):
    """FastAPI endpoint for customer discovery"""
    discoverer = CustomerDiscoverer(domain)
    return discoverer.discover()
