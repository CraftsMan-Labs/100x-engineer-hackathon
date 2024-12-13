from typing import List, Dict, Any
from pydantic import BaseModel, Field
from src.app.llm import LiteLLMKit
from src.app.jina import JinaReader
from src.app.exa import ExaAPI
from src.app.config import get_settings
from src.app.pinecone_client import PineconeRAG
from datetime import datetime
import logging
from src.app.schemas.llm import ChatRequest, Message
from fastapi import APIRouter
from time import perf_counter


class CustomerNiche(BaseModel):
    """Represents a specific customer niche"""

    name: str
    description: str
    market_size: int = Field(..., description="Total market size in USD")
    growth_potential: float
    key_characteristics: List[str]


class CustomerDiscoveryReport(BaseModel):
    """Comprehensive customer discovery report"""

    primary_domain: str
    total_market_size: int
    niches: List[CustomerNiche]
    ideal_customer_profile: Dict[str, Any]
    investor_sentiment: Dict[str, Any]


class IdentifyMarketNiche(BaseModel):
    niches: List[str]


class NicheAnalysis(BaseModel):
    """Structure for niche market analysis results"""

    market_size: int
    growth_potential: float
    key_characteristics: List[str]


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
        self.pinecone = PineconeRAG()

        self.domain = domain
        self.niches: List[CustomerNiche] = []
        self.comprehensive_report: CustomerDiscoveryReport | None

    def generate_high_level_query(self) -> str:
        """Generate a high-level market research query"""
        prompt = f"""
        Generate a comprehensive market research query for understanding customer markets in the {self.domain} domain.
        Focus on identifying key customer segments, workflows, and market characteristics.
        """
        return self.llm.generate(
            ChatRequest(messages=[Message(role="user", content=prompt)])
        )

    def identify_market_niches(self, high_level_query: str) -> List[str]:
        """Identify potential market niches within the domain"""
        prompt = f"""
        Based on the high-level market research query: '{high_level_query}'
        Identify and list 5~10 specific market niches/subdomains of maeket within the {self.domain} domain.
        For each niche, provide a brief description and potential market significance.
        If there is no niche, create a new one.
        """
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
        prompt = f"""
        Create a precise internet search query to research the following market niche: '{niche}'
        in the context of the {self.domain} domain. 
        Focus on customer characteristics, market size, and key trends.
        """
        return self.llm.generate(
            ChatRequest(messages=[Message(role="user", content=prompt)])
        )

    def search_niche_market(self, niche: str, search_query: str) -> CustomerNiche:
        """Analyze market size, growth, and characteristics for a specific niche"""
        try:
            # Get market research data
            search_contents = self.exa.search_and_contents(search_query, num_results=2)
            market_data = "\n".join(result.text for result in search_contents.results)
        except Exception as e:
            print(f"Exa search failed: {e}, falling back to Jina")
            market_data = self.jina.search(search_query)

        # Structured analysis prompt
        analysis_prompt = f"""
        Analyze the market data for the '{niche}' niche in {self.domain}.
        Return a JSON object with these fields:
        - market_size: Total market size in USD (integer)
        - growth_potential: Annual growth rate as decimal (e.g., 0.15 for 15%)
        - key_characteristics: List of 3-5 key customer characteristics
        
        Base your analysis on concrete market data and trends.
        If exact numbers aren't available, provide conservative estimates.
        """

        # Get structured analysis
        niche_analysis = self.llm.generate(
            ChatRequest(
                messages=[
                    Message(role="system", content=analysis_prompt),
                    Message(role="user", content=market_data),
                ]
            ),
            response_format=NicheAnalysis,
        )

        # Create customer niche with analyzed data
        return CustomerNiche(
            name=niche,
            description=f"Market niche in {self.domain} domain",
            market_size=niche_analysis["market_size"],
            growth_potential=niche_analysis["growth_potential"],
            key_characteristics=niche_analysis["key_characteristics"],
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
            search_contents = self.exa.search_and_contents(
                market_year_query, num_results=2
            )
            search_results = [
                search_contents.results[i].text
                for i in range(len(search_contents.results[:2]))
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
        }

    def compile_comprehensive_report(self):
        """Compile a comprehensive customer discovery report with year-by-year analysis"""

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

        print("Investor insights:", investor_insights)

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

        print("Ideal customer profile:", ideal_customer_insights)

        self.comprehensive_report = CustomerDiscoveryReport(
            primary_domain=self.domain,
            total_market_size=sum(niche.market_size for niche in self.niches),
            niches=self.niches,
            investor_sentiment={"insights": investor_insights},
            ideal_customer_profile={"insights": ideal_customer_insights},
        )

    async def discover(self)-> CustomerDiscoveryReport:
        """Execute full customer discovery workflow"""
        start_time = perf_counter()
        print(f"Initiating customer discovery for domain: {self.domain}...")
        high_level_query = self.generate_high_level_query()
        print(f"High-level query: {high_level_query}")
        niches = self.identify_market_niches(high_level_query)
        print(f"Identified niches: {niches}")

        for niche in niches[:4]:  # Limit to 10 niches
            search_query = self.generate_niche_search_query(niche)
            print(f"Search query for '{niche}': {search_query}")
            niche_details = self.search_niche_market(niche, search_query)
            print(f"Details for '{niche}': {niche_details}")
            self.niches.append(niche_details)

        print("Compiling comprehensive report...")
        self.compile_comprehensive_report()
        print(f"Total time taken: {perf_counter() - start_time:.2f} seconds")
        
        # Store the report in Pinecone
        await self.pinecone.aupsert_documents(
            documents=[self.comprehensive_report.model_dump_json()],
            metadata=[{
                "type": "customer_discovery",
                "domain": self.domain,
                "timestamp": datetime.now().isoformat()
            }]
        )
        
        logging.info(f"Successfully stored customer discovery report for domain {self.domain} in Pinecone")
        
        return self.comprehensive_report


router = APIRouter(prefix="/customer-discovery", tags=["customer_discovery"])


@router.post("/discover")
async def customer_discovery_endpoint(
    domain: str, product_description: str, product_name: str, offerings: str
) -> CustomerDiscoveryReport:
    """FastAPI endpoint for customer discovery"""
    final_query = f" Product: {product_name} Description: {product_description} Offerings: {offerings} in the domain of {domain}"
    discoverer = CustomerDiscoverer(final_query)
    return await discoverer.discover()
