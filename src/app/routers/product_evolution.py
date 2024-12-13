from typing import List, Dict, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
import io
import base64
import logging
from time import perf_counter
from app.pinecone_client import PineconeRAG
from app.routers.customer_discovery import CustomerDiscoveryReport
from app.routers.market_analysis import MarketAnalysisReport
from app.routers.market_expansion import MarketExpansionStrategy
from app.llm import LiteLLMKit
from app.schemas.llm import ChatRequest, Message

router = APIRouter(prefix="/product-evolution", tags=["product_evolution"])

plt.switch_backend('Agg') 
class ProductEvolutionPhase(BaseModel):
    """Detailed product evolution phase"""

    phase_number: int
    name: str
    description: str
    target_customer_segments: List[str]
    key_features: List[str]
    value_proposition: str
    expected_market_reaction: str
    success_metrics: list[str]
    risk_mitigation_strategies: List[str]


class UserAdoptionTrend(BaseModel):
    """User adoption trend visualization data"""

    x_axis_labels: list[str]
    y_axis_labels: list[str]
    x_axis_data: list[float]
    y_axis_data: list[float]
    x_axis_name: str
    y_axis_name: str
    reasoning: str
    key_insights: List[str]


class EvolutionVisuals(BaseModel):
    img: str
    reason: str
    insights: List[str]


class ProductEvolutionStrategy(BaseModel):
    """Comprehensive product evolution roadmap"""

    primary_domain: str
    phases: list[ProductEvolutionPhase]
    overall_vision: str = Field(description="Long-term product vision")
    long_term_goals: List[str]
    competitive_differentiation: list[str]
    user_adoption_trend: UserAdoptionTrend = Field(
        description="Generate a hypothetical User adoption trend"
    )


class EvolutionStrategy(BaseModel):
    """Comprehensive product evolution roadmap"""

    primary_domain: str
    overall_vision: str = Field(description="Long-term product vision")
    long_term_goals: List[str]
    competitive_differentiation: list[str]


class FinalEvolutionStrategy(BaseModel):
    strategy: ProductEvolutionStrategy
    visuals: EvolutionVisuals


class ProductEvolver:
    """Advanced product evolution strategy generator"""

    def __init__(
        self,
        customer_discovery: CustomerDiscoveryReport,
        market_analysis: MarketAnalysisReport,
        market_expansion: MarketExpansionStrategy,
        llm_model: str = "gpt-4o",
        temperature: float = 0.7,
    ):
        """Initialize Product Evolver with comprehensive market insights"""
        self.llm = LiteLLMKit(model_name=llm_model, temperature=temperature)

        self.customer_discovery = customer_discovery
        self.market_analysis = market_analysis
        self.market_expansion = market_expansion

        self.primary_domain = customer_discovery.primary_domain
        self.evolution_strategy: Optional[ProductEvolutionStrategy] = None

    def _extract_key_insights(self):
        """Extract most valuable and clear data points from reports"""
        # Customer Discovery Insights
        key_niches = [
            niche
            for niche in self.customer_discovery.niches[:3]
            if niche.market_size > 0
        ]
        ideal_customer_profile = self.customer_discovery.ideal_customer_profile.get(
            "insights", ""
        )

        # Market Analysis Insights
        market_trends = self.market_analysis.comprehensive_report

        # Market Expansion Insights
        expansion_domains = self.market_expansion.expansion_domains
        strategic_rationale = self.market_expansion.strategic_rationale

        return {
            "key_niches": key_niches,
            "ideal_customer_profile": ideal_customer_profile,
            "market_trends": market_trends,
            "expansion_domains": expansion_domains,
            "strategic_rationale": strategic_rationale,
        }

    def _generate_phase_one(self, insights: dict) -> ProductEvolutionPhase:
        """Generate MVP phase strategy"""
        mvp_prompt = f"""
        Design the MVP (Minimum Viable Product) phase for {self.primary_domain}.
        
        Context:
        - Primary Target Niche: {insights['key_niches'][0]}
        - Ideal Customer: {insights['ideal_customer_profile']}
        
        Focus on:
        1. Core feature set that solves immediate pain points
        2. Quick market entry and validation
        3. Early adopter engagement
        4. Feedback collection mechanisms
        """

        messages = [
            Message(
                role="system",
                content="You are a product strategy expert focused on MVP development.",
            ),
            Message(role="user", content=mvp_prompt),
        ]

        request = ChatRequest(messages=messages)
        phase_one = self.llm.generate(request, response_format=ProductEvolutionPhase)
        return ProductEvolutionPhase(**phase_one)

    def _generate_phase_two(
        self, insights: dict, phase_one: ProductEvolutionPhase
    ) -> ProductEvolutionPhase:
        """Generate market expansion phase strategy"""
        expansion_prompt = f"""
        Design the market expansion phase for {self.primary_domain}.
        
        Previous Phase Achievements:
        {phase_one.key_features}
        
        Context:
        - Additional Target Niches: {insights['key_niches'][1:]}
        - Market Trends: {insights['market_trends']}
        
        Focus on:
        1. Feature expansion based on MVP learnings
        2. Market share growth
        3. Enhanced value proposition
        4. Scaling operations
        """

        messages = [
            Message(
                role="system",
                content="You are a product strategy expert focused on market expansion.",
            ),
            Message(role="user", content=expansion_prompt),
        ]

        request = ChatRequest(messages=messages)
        phase_two = self.llm.generate(request, response_format=ProductEvolutionPhase)
        return ProductEvolutionPhase(**phase_two)

    def _generate_phase_three(
        self, insights: dict, phase_two: ProductEvolutionPhase
    ) -> ProductEvolutionPhase:
        """Generate maturity and innovation phase strategy"""
        maturity_prompt = f"""
        Design the maturity and innovation phase for {self.primary_domain}.
        
        Previous Phase Achievements:
        {phase_two.key_features}
        
        Context:
        - Expansion Domains: {insights['expansion_domains']}
        - Strategic Rationale: {insights['strategic_rationale']}
        
        Focus on:
        1. Innovation and differentiation
        2. Market leadership
        3. New market opportunities
        4. Long-term sustainability
        """

        messages = [
            Message(
                role="system",
                content="You are a product strategy expert focused on market leadership and innovation.",
            ),
            Message(role="user", content=maturity_prompt),
        ]

        request = ChatRequest(messages=messages)
        phase_three = self.llm.generate(request, response_format=ProductEvolutionPhase)
        return ProductEvolutionPhase(**phase_three)

    def generate_product_evolution_strategy(self) -> ProductEvolutionStrategy:
        """Generate a comprehensive product evolution strategy"""
        insights = self._extract_key_insights()

        # Generate phases sequentially
        phase_one = self._generate_phase_one(insights)
        phase_two = self._generate_phase_two(insights, phase_one)
        phase_three = self._generate_phase_three(insights, phase_two)

        # Generate overall strategy prompt
        strategy_prompt = f"""
        Create an overall product evolution strategy for {self.primary_domain} based on the following phases:
        
        Phase 1 (MVP): {phase_one.description}
        Phase 2 (Expansion): {phase_two.description}
        Phase 3 (Maturity): {phase_three.description}
        
        Provide:
        1. Overall vision connecting all phases
        2. Long-term strategic goals
        3. Competitive differentiation strategy
        """

        messages = [
            Message(
                role="system",
                content="You are a strategic product evolution expert. Create a cohesive strategy that connects all phases.",
            ),
            Message(role="user", content=strategy_prompt),
        ]

        request = ChatRequest(messages=messages)
        strategy_response = self.llm.generate(
            request, response_format=EvolutionStrategy
        )

        print(f"strategy_response: {strategy_response} type: {type(strategy_response)}")

        # Assemble complete strategy
        self.evolution_strategy = ProductEvolutionStrategy(
            primary_domain=self.primary_domain,
            phases=[phase_one, phase_two, phase_three],
            overall_vision=strategy_response.get("overall_vision", ""),
            long_term_goals=strategy_response.get("long_term_goals", []),
            competitive_differentiation=strategy_response.get(
                "competitive_differentiation", []
            ),
            user_adoption_trend=self._generate_user_adoption_trend(
                [phase_one, phase_two, phase_three]
            ),
        )

        return self.evolution_strategy

    def _generate_user_adoption_trend(
        self, phases: List[ProductEvolutionPhase]
    ) -> UserAdoptionTrend:
        """Generate phase-aware user adoption trend visualization"""
        user_adoption_query = f"""
        Generate a user adoption trend visualization for {self.primary_domain} across these phases:
        
        Phase 1 (MVP): 
        - Features: {phases[0].key_features}
        - Target Segments: {phases[0].target_customer_segments}
        
        Phase 2 (Expansion):
        - Features: {phases[1].key_features}
        - Target Segments: {phases[1].target_customer_segments}
        
        Phase 3 (Maturity):
        - Features: {phases[2].key_features}
        - Target Segments: {phases[2].target_customer_segments}
        
        Requirements:
        1. Show adoption curves for:
           - Beta Users
           - Paying Users
           - Total Users
        2. Highlight phase transition points
        3. Explain adoption patterns for each phase
        4. Provide data-driven insights
        """

        messages = [
            Message(
                role="system",
                content="You are an expert in user adoption trend analysis. Generate realistic, strategic user growth data.",
            ),
            Message(role="user", content=user_adoption_query),
        ]

        request = ChatRequest(messages=messages)
        user_adoption_response = self.llm.generate(
            request, response_format=UserAdoptionTrend
        )

        return UserAdoptionTrend(**user_adoption_response)

    def visualize_user_adoption_trend(
        self, trend_data: UserAdoptionTrend
    ) -> EvolutionVisuals:
        """
        Visualize user adoption trend data using matplotlib

        Args:
            trend_data (UserAdoptionTrend): User adoption trend visualization data

        Returns:
            TrendVisualizationResponse: Visualization with image and insights
        """
        plt.figure(figsize=(12, 6))
        print(f"trend_data: {trend_data}")

        # Plot the trend line
        plt.plot(
            trend_data.x_axis_data,
            trend_data.y_axis_data,
            label=trend_data.y_axis_labels[0],
            marker="o",
        )

        plt.title(f"User Adoption Trend: {trend_data.y_axis_name}")
        plt.xlabel(trend_data.x_axis_name)
        plt.ylabel(trend_data.y_axis_name)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save plot to a base64 encoded image
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()
        return EvolutionVisuals(
            img=image_base64,
            reason=trend_data.reasoning,
            insights=trend_data.key_insights,
        )


@router.post("/evolve")
def product_evolution_endpoint(
    customer_report: CustomerDiscoveryReport,
    market_report: MarketAnalysisReport,
    market_expansion: MarketExpansionStrategy,
):
    """FastAPI endpoint for product evolution strategy generation"""
    start_time = perf_counter()
    evolver = ProductEvolver(customer_report, market_report, market_expansion)

    evolution_strategy = evolver.generate_product_evolution_strategy()
    visuals = {}
    if evolution_strategy.user_adoption_trend:
        visuals = evolver.visualize_user_adoption_trend(
            evolution_strategy.user_adoption_trend
        )
    
    # Create final strategy response
    final_strategy = FinalEvolutionStrategy(strategy=evolution_strategy, visuals=visuals)
    
    # Upload to Pinecone
    try:
        pinecone_client = PineconeRAG()
        # Convert the strategy to a string representation for storage
        strategy_text = f"""
        Product Evolution Strategy for {evolution_strategy.primary_domain}
        Overall Vision: {evolution_strategy.overall_vision}
        Long Term Goals: {', '.join(evolution_strategy.long_term_goals)}
        Competitive Differentiation: {', '.join(evolution_strategy.competitive_differentiation)}
        """
        
        # Upload with metadata
        pinecone_client.upsert_documents(
            documents=[strategy_text],
            metadata=[{
                "type": "product_evolution",
                "domain": evolution_strategy.primary_domain,
                "timestamp": str(perf_counter())
            }]
        )
        logging.info(f"Successfully uploaded product evolution strategy for {evolution_strategy.primary_domain} to Pinecone")
    except Exception as e:
        logging.error(f"Failed to upload to Pinecone: {str(e)}")
    
    print(
        f"Completed product evolution analysis in {perf_counter() - start_time:.2f} seconds"
    )
    return final_strategy
