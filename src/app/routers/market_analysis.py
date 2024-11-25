from typing import List, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends

from app.llm import LiteLLMKit
from app.jina import JinaReader
from app.exa import ExaAPI
from app.schemas.llm import ChatRequest, Message
from app.config import get_settings

from app.routers.prompts import (breakdown_problem_prompt, analyze_search_results_prompt,
    compile_comprehensive_report_prompt)

router = APIRouter(prefix="/market-analysis", tags=["market_analysis"])


class ProblemBreakdown(BaseModel):
    """Represents a breakdown of a complex problem into sub-problems"""

    questions: List[str] = Field(
        ..., description="List of sub-problems derived from the main query"
    )


class MarketTrendVisualization(BaseModel):
    """Detailed market trend visualization data"""

    time_series_data: Dict[str, List[float]]
    growth_rates: Dict[str, float]
    trend_indicators: Dict[str, str]
    comparative_analysis: Dict[str, Any]
    predictive_intervals: Dict[str, Any]


class MarketAnalysisReport(BaseModel):
    """Comprehensive market analysis report"""

    original_query: str
    problem_breakdown: ProblemBreakdown
    search_results: Dict[str, Dict[str, Any]]
    comprehensive_report: str
    trend_visualization: MarketTrendVisualization


class MarketAnalyzer:
    def __init__(self, llm_model: str = "gpt-4o", temperature: float = 0.7):
        """Initialize Market Analyzer with LLM and external search APIs"""
        self.llm = LiteLLMKit(model_name=llm_model, temperature=temperature)
        self.jina = JinaReader(get_settings().JINA_API_KEY)
        self.exa = ExaAPI(get_settings().EXA_API_KEY)

        self.original_query: str = ""
        self.questions: List[str] = []
        self.search_results: Dict[str, Dict[str, Any]] = {}
        self.reports: Dict[str, str] = {}
        self.comprehensive_report: str = ""

    def breakdown_problem(self, query: str) -> ProblemBreakdown:
        """Break down the original query into multiple sub-problems"""
        messages = [
            Message(
                role="system",
                content=breakdown_problem_prompt,
            ),
            Message(
                role="user",
                content=f"Break down this query into detailed sub-problems: {query}",
            ),
        ]

        request = ChatRequest(messages=messages)
        breakdown = self.llm.generate(request, response_format=ProblemBreakdown)

        breakdown = ProblemBreakdown(**breakdown)

        self.original_query = query
        self.questions = breakdown.questions
        return breakdown

    def generate_search_query(self, question: str) -> str:
        """Generate an optimized search query for each sub-problem"""
        messages = [
            Message(
                role="system",
                content="""
            You are an expert search query generator. 
            Create precise, targeted search queries that will yield comprehensive information.
            Focus on extracting actionable insights.
            """,
            ),
            Message(
                role="user", content=f"Generate a search query to research: {question}"
            ),
        ]

        request = ChatRequest(messages=messages)
        return self.llm.generate(request)

    def search_internet(self, search_query: str, fallback: bool = True) -> List[str]:
        """Search internet with fallback mechanism"""
        try:
            # Try Exa first
            exa_results = self.exa.search(search_query)
            return [result.text for result in exa_results.results]
        except Exception as e:
            if fallback:
                try:
                    # Fallback to Jina
                    return [self.jina.search(search_query)]
                except Exception:
                    return []
            return []

    def analyze_search_results(self, question: str, search_results: List[str]) -> str:
        """Analyze search results and generate a concise report"""
        messages = [
            Message(
                role="system",
                content=analyze_search_results_prompt,
            ),
            Message(
                role="user",
                content=f"Question: {question}\nSearch Results: {search_results}",
            ),
        ]

        request = ChatRequest(messages=messages)
        return self.llm.generate(request)

    def search_market_for_year(self, year: int, question: str) -> Dict[str, Any]:
        """Perform targeted market search for a specific year and question"""
        market_year_query = f"""
        Analyze the market for {question} in the year {year} with focus on:
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
        Comprehensively analyze the search results for the market question '{question}' in {year}.
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
            "question": question,
            "analysis": year_analysis,
            "raw_search_results": search_results,
        }

    def perform_analysis(self):
        """Perform comprehensive market analysis with year-specific searches"""
        years = list(range(2019, 2025))

        for question in self.questions:
            # Perform year-specific searches
            yearly_insights = [
                self.search_market_for_year(year, question) for year in years
            ]

            self.search_results[question] = {"yearly_insights": yearly_insights}

            year_insights_analysis = [
                insight["analysis"] for insight in yearly_insights
            ]

            # Compile a comprehensive report for the question
            compilation_prompt = f"""
            Synthesize the year-by-year market insights for the question: '{question}'.
            Create a comprehensive analysis that:
            1. Identifies overarching trends
            2. Highlights key inflection points
            3. Provides predictive insights
            4. Suggests strategic recommendations
            """

            comprehensive_report = self.llm.generate(
                ChatRequest(
                    messages=[
                        Message(role="user", content=compilation_prompt),
                        Message(role="system", content=str(year_insights_analysis)),
                    ]
                )
            )

            self.reports[question] = comprehensive_report

    def generate_trend_visualization(self) -> MarketTrendVisualization:
        """Generate comprehensive trend visualization and analysis"""
        messages = [
            Message(
                role="system",
                content="""
                You are an advanced data analyst and trend visualization expert.
                Analyze the market research results and generate:
                1. Time series data for key metrics
                2. Comparative growth rates
                3. Trend indicators
                4. Predictive intervals
                5. Comparative market analysis
                Focus on extracting actionable insights and visualization-ready data.
                """,
            ),
            Message(
                role="user",
                content=f"Analyze trends from these yearly market insights: {self.search_results}",
            ),
        ]

        request = ChatRequest(messages=messages)
        trend_data = self.llm.generate(
            request, response_format=MarketTrendVisualization
        )

        return MarketTrendVisualization(**trend_data)

    def compile_comprehensive_report(self):
        """Compile individual reports into a comprehensive market analysis"""
        messages = [
            Message(
                role="system",
                content=compile_comprehensive_report_prompt
            ),
            Message(
                role="user",
                content=f"Original Query: {self.original_query}\nIndividual Reports: {self.reports}",
            ),
        ]

        request = ChatRequest(messages=messages)
        self.comprehensive_report = self.llm.generate(request)

        # Generate trend visualization
        self.trend_visualization = self.generate_trend_visualization()

        return self.comprehensive_report

    def get_report(self) -> MarketAnalysisReport:
        """Retrieve the complete market analysis report"""
        return MarketAnalysisReport(
            original_query=self.original_query,
            problem_breakdown=ProblemBreakdown(questions=self.questions),
            search_results=self.search_results,
            comprehensive_report=self.comprehensive_report,
            trend_visualization=self.trend_visualization,
        )


@router.post("/analyze")
async def market_analysis(query: str):
    """Endpoint for market analysis"""
    analyzer = MarketAnalyzer()
    analyzer.breakdown_problem(query)
    analyzer.perform_analysis()
    analyzer.compile_comprehensive_report()

    return analyzer.get_report()
