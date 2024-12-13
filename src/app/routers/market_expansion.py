from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from datetime import datetime
import logging
from pydantic import BaseModel, Field
from time import perf_counter
from app.pinecone_client import PineconeRAG
from app.routers.customer_discovery import CustomerDiscoverer, CustomerDiscoveryReport
from app.routers.market_analysis import MarketAnalyzer, MarketAnalysisReport
from app.llm import LiteLLMKit
from app.schemas.llm import ChatRequest, Message
from app.exa import ExaAPI
from app.jina import JinaReader
from app.config import get_settings

router = APIRouter(prefix="/market-expansion", tags=["market_expansion"])


class MarketExpansionStrategy(BaseModel):
    """Comprehensive market expansion strategy"""

    primary_domain: str
    expansion_domains: List[str] = Field(
        ...,
        description="Potential adjacent or complementary market domains for expansion",
    )
    strategic_rationale: Dict[str, str] = Field(
        ..., description="Detailed reasoning for each potential expansion domain"
    )
    competitive_landscape: Dict[str, Any] = Field(
        ...,
        description="Analysis of competitive dynamics in potential expansion domains",
    )
    investment_requirements: Dict[str, float] = Field(
        ..., description="Estimated investment needs for each expansion domain"
    )
    risk_assessment: Dict[str, float] = Field(
        ..., description="Risk levels associated with each expansion domain"
    )
    potential_synergies: List[str] = Field(
        ..., description="Potential synergies between current and expansion domains"
    )


class MarketExpander:
    """Advanced market expansion analysis tool"""

    def __init__(
        self,
        customer_discovery_report: CustomerDiscoveryReport,
        market_analysis_report: MarketAnalysisReport,
        llm_model: str = "gemini-1.5-flash",
        temperature: float = 0.7,
    ):
        """Initialize Market Expander with pre-generated reports"""
        self.settings = get_settings()
        self.llm = LiteLLMKit(model_name=llm_model, temperature=temperature)
        self.jina = JinaReader(self.settings.JINA_API_KEY)
        self.exa = ExaAPI(self.settings.EXA_API_KEY)
        self.pinecone = PineconeRAG()

        self.primary_domain = customer_discovery_report.primary_domain
        self.customer_discovery_report = customer_discovery_report
        self.market_analysis_report = market_analysis_report
        self.expansion_strategy: Optional[MarketExpansionStrategy] = None

    def generate_expansion_domains(self) -> List[str]:
        """Generate potential market expansion domains"""

        expansion_query = f"""
        Based on the market analysis and customer discovery for the {self.primary_domain} domain, 
        identify 5-7 potential adjacent or complementary market domains for strategic expansion.

        Considerations:
        1. Technological adjacencies
        2. Customer base overlap
        3. Skill and resource transferability
        4. Market growth potential
        5. Competitive landscape
        6. Investment requirements
        7. Potential synergies

        Provide a ranked list of expansion domains with brief rationale.
        """

        messages = [
            Message(
                role="system",
                content="You are an expert market strategist specializing in business expansion.",
            ),
            Message(
                role="assistant",
                content="Customer Discovery Report:\n\n"
                + str(self.customer_discovery_report),
            ),
            Message(
                role="assistant",
                content="Market Analysis Report:\n\n"
                + str(self.market_analysis_report.comprehensive_report)
                + "\n\n"
                + str(self.market_analysis_report.problem_breakdown),
            ),
            Message(role="user", content=expansion_query),
        ]

        request = ChatRequest(messages=messages)
        expansion_domains_response = self.llm.generate(request)

        # Parse the response into a list of domains
        expansion_domains = [
            domain.strip()
            for domain in expansion_domains_response.split("\n")
            if domain.strip()
        ]

        return expansion_domains[:7]  # Limit to top 7 domains

    def analyze_expansion_domains(
        self, expansion_domains: List[str]
    ) -> MarketExpansionStrategy:
        """Perform comprehensive analysis of potential expansion domains"""
        strategic_rationale = {}
        competitive_landscape = {}
        investment_requirements = {}
        risk_assessment = {}
        potential_synergies = []

        for domain in expansion_domains:
            # Perform targeted search and analysis for each domain
            try:
                search_query = f"Market expansion opportunities in {domain} related to {self.primary_domain}"

                # Use Exa and Jina for comprehensive search
                try:
                    search_contents = self.exa.search_and_contents(
                        search_query, num_results=2
                    )
                    search_results = [result.text for result in search_contents.results]
                except Exception:
                    search_results = [self.jina.search(search_query)]

                search_results_str = " \n".join(search_results)

                # Analyze expansion domain
                expansion_analysis_prompt = f"""
                Comprehensively analyze the potential for expanding from {self.primary_domain} into {domain}.

                Provide detailed insights on:
                1. Strategic Rationale
                2. Competitive Landscape
                3. Investment Requirements
                4. Risk Assessment
                5. Potential Synergies

                Context from search results:
                {search_results_str}
                """

                messages = [
                    Message(
                        role="system",
                        content="You are an expert market expansion strategist.",
                    ),
                    Message(role="user", content=expansion_analysis_prompt),
                ]

                request = ChatRequest(messages=messages)
                domain_analysis = self.llm.generate(request)

                # Parse and structure the analysis
                strategic_rationale[domain] = domain_analysis
                competitive_landscape[domain] = f"Competitive analysis for {domain}"
                investment_requirements[domain] = 1000000.0  # Default placeholder
                risk_assessment[domain] = 0.5  # Default moderate risk
                potential_synergies.append(
                    f"Potential synergy between {self.primary_domain} and {domain}"
                )

            except Exception as e:
                print(f"Error analyzing expansion domain {domain}: {e}")

        self.expansion_strategy = MarketExpansionStrategy(
            primary_domain=self.primary_domain,
            expansion_domains=expansion_domains,
            strategic_rationale=strategic_rationale,
            competitive_landscape=competitive_landscape,
            investment_requirements=investment_requirements,
            risk_assessment=risk_assessment,
            potential_synergies=potential_synergies,
        )

        return self.expansion_strategy

    def expand_market(self) -> MarketExpansionStrategy:
        """Execute full market expansion workflow"""
        print(f"Initiating market expansion analysis for domain: {self.primary_domain}")

        # Generate potential expansion domains
        expansion_domains = self.generate_expansion_domains()
        print(f"Potential expansion domains: {expansion_domains}")

        # Analyze expansion domains
        expansion_strategy = self.analyze_expansion_domains(expansion_domains)

        return expansion_strategy


@router.post("/expand", response_model=MarketExpansionStrategy)
async def market_expansion_endpoint(
    domain: str,
    customer_report: Optional[CustomerDiscoveryReport] = None,
    market_report: Optional[MarketAnalysisReport] = None,
) -> MarketExpansionStrategy:
    """
    FastAPI endpoint for market expansion analysis

    Args:
        domain: Target domain for expansion
        customer_report: Optional pre-generated customer discovery report
        market_report: Optional pre-generated market analysis report

    Returns:
        MarketExpansionStrategy: Comprehensive expansion strategy
    """
    start_time = perf_counter()
    # Generate customer discovery report if not provided
    if not customer_report:
        discoverer = CustomerDiscoverer(domain)
        customer_report = discoverer.discover()

    # Generate market analysis report if not provided
    if not market_report:
        analyzer = MarketAnalyzer()
        analyzer.breakdown_problem(domain)
        analyzer.perform_analysis()
        analyzer.compile_comprehensive_report()
        market_report = analyzer.get_report()

    # Generate expansion strategy
    expander = MarketExpander(customer_report, market_report)
    expansion_strategy = expander.expand_market()

    # Store expansion strategy in Pinecone
    await expander.pinecone.aupsert_documents(
        documents=[expansion_strategy.model_dump_json()],
        metadata=[
            {
                "type": "market_expansion",
                "domain": domain,
                "timestamp": datetime.now().isoformat(),
            }
        ],
    )

    logging.info(
        f"Successfully stored market expansion strategy for domain '{domain}' in Pinecone"
    )

    print(
        f"Market expansion analysis completed in {perf_counter() - start_time:.2f} seconds"
    )
    return expansion_strategy
