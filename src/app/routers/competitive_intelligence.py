import logging
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel
from time import perf_counter
from src.app.pinecone_client import PineconeRAG
from src.app.llm import LiteLLMKit
from src.app.jina import JinaReader
from src.app.exa import ExaAPI
from src.app.config import get_settings
from src.app.schemas.llm import ChatRequest, Message
from src.app.routers.customer_discovery import CustomerDiscoverer
from fastapi import APIRouter
import asyncio
from datetime import datetime


class CompetitorProfile(BaseModel):
    """Basic competitor profile"""

    name: str
    description: str
    main_products: List[str]
    target_market: str
    key_differentiators: List[str]


class ListCompetitorProfile(BaseModel):
    """List of competitor profiles"""

    competitors: List[CompetitorProfile]


class ProductDerivative(BaseModel):
    """Simple product derivative info"""

    name: str
    description: str
    target_market: str


class ListProductDerivative(BaseModel):
    """List of product derivatives"""

    derivatives: List[ProductDerivative]


class CompetitiveAnalysisReport(BaseModel):
    """Simple competitive analysis report"""

    product_name: str
    competitors: List[CompetitorProfile]
    derivatives: List[ProductDerivative]


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class CompetitiveAnalyzer:
    """Simple competitive analysis tool"""

    def __init__(
        self,
        product_name: str,
        product_description: str,
        llm_model: str = "gpt-4o",
        temperature: float = 0.7,
    ):
        self.settings = get_settings()
        self.llm = LiteLLMKit(model_name=llm_model, temperature=temperature)
        self.exa = ExaAPI(self.settings.EXA_API_KEY)
        self.pinecone = PineconeRAG()
        self.product_name = product_name
        self.product_description = product_description

    async def get_competitors(
        self, product_name: str = None, product_description: str = None
    ) -> List[CompetitorProfile]:
        """Search for competitors and structure the data for a specific product"""
        start_time = perf_counter()

        # Use provided parameters or fall back to class attributes
        target_product = product_name or self.product_name
        target_description = product_description or self.product_description

        logger.info(f"Searching competitors for {target_product}")

        # Construct a more targeted search query
        search_query = f"""You are an intelligent system tasked with generating optimized search queries to identify and analyze competitors for a specific product. Follow the instructions below to construct an effective search query.

**Input Variables:**
- `{target_product}`: The exact name of the product you want to analyze.
- `{target_description}`: A concise description of the target product.

**Instructions:**

1. **Exact Product Name Match:**
   - Include the exact product name to ensure precision in search results.
   - Format: `"{target_product}"`

2. **Product Description Context:**
   - Incorporate the product description to provide context and refine the search scope.
   - Format: `("{target_description}")`

3. **Competitor Identification Keywords:**
   - Use keywords that indicate competitor-related content.
   - Include variations to capture different ways competitors might be referenced.
   - Suggested Keywords: `competitor`, `alternative`, `"market leader"`, `"similar product"`
   - Format: `(competitor OR alternative OR "market leader" OR "similar product")`

4. **Feature and Comparison Focus:**
   - Add terms that focus on features, pricing, comparisons, and reviews to gather detailed competitor information.
   - Suggested Terms: `features`, `pricing`, `comparison`, `review`
   - Format: `(features OR pricing OR comparison OR review)`

5. **Exclude Irrelevant Content:**
   - Remove search results related to job postings and career opportunities to maintain relevance.
   - Exclude Terms: `-job`, `-careers`
   - Format: `-job -careers`

6. **Combine All Elements:**
   - Concatenate all the above components to form a comprehensive search query.
   - Ensure proper spacing and syntax for optimal search engine performance.

**Output Format:**
- The final search query should be a single string that combines all the elements as specified.

**Example Output:**

```python
search_query = (
    f'"{target_product}" '  # Exact product name match
    f'("{target_description}") '  # Description in context
    f'(competitor OR alternative OR "market leader" OR "similar product") '
    f'(features OR pricing OR comparison OR review) '
    f'-job -careers'  # Exclude job postings
)
        """

        try:
            search_results = await asyncio.to_thread(
                self.exa.search_and_contents, search_query
            )
            competitor_data = "\n".join(
                result.text for result in search_results.results
            )
            logger.info(f"Found {len(search_results.results)} search results")
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

        analysis_prompt = f"""
You are an intelligent system tasked with analyzing the competition for a specific product. Follow the instructions below to identify and evaluate the top competitors.

**Input Variables:**
- `{self.product_name}`: The name of your product.
- `{self.product_description}`: A brief description of your product.

**Instructions:**

1. **Identify Competitors:**
   - Based on the search results, identify companies that directly compete with `{self.product_name}`.
   - Focus on companies that offer products or services similar to `{self.product_description}`.

2. **Analyze Competitors:**
   - For each identified competitor, gather the following information:
     - **Name**: The official name of the company.
     - **Description**: A brief overview of the company and its offerings.
     - **Main Products**: A list of the competitor's main products that overlap with yours.
     - **Target Market**: The primary audience or market segment the competitor is aiming for.
     - **Key Differentiators**: Unique features or aspects that set the competitor apart from others.

3. **Verification:**
   - Ensure that each competitor listed has a clear and direct overlap with your product.
   - Include only verified competitors with substantial evidence of competition.

4. **Output Format:**
   - Present the analysis as a JSON array of competitor profiles.
   - Each competitor profile should include the following fields:
     - `name`: *String* — Company name.
     - `description`: *String* — Brief company description.
     - `main_products`: *Array of Strings* — List of their main competing products.
     - `target_market`: *String* — Their primary target market.
     - `key_differentiators`: *Array of Strings* — List of what makes them unique.

        """

        competitors = await self.llm.agenerate(
            ChatRequest(
                messages=[
                    Message(role="system", content=analysis_prompt),
                    Message(role="user", content=competitor_data),
                ]
            ),
            response_format=ListCompetitorProfile,
        )

        elapsed = perf_counter() - start_time
        logger.info(f"Analyzed {len(competitors)} competitors in {elapsed:.2f} seconds")
        return competitors["competitors"]

    async def get_derivatives(self) -> List[ProductDerivative]:
        """Identify potential product derivatives and their competitors"""
        logger.info(f"Identifying derivatives for {self.product_name}")

        # First, get potential derivatives
        derivatives_prompt = f"""
        For the product {self.product_name} ({self.product_description}),
        suggest 2-3 potential product derivatives or variations.
        
        Return the analysis as a JSON array with these fields:
        - name: Name of the derivative product
        - description: Brief description of how it differs
        - target_market: Specific market segment it targets
        
        Focus on meaningful variations that serve different use cases or markets.
        """

        derivatives_result = await self.llm.agenerate(
            ChatRequest(messages=[Message(role="user", content=derivatives_prompt)]),
            response_format=ListProductDerivative,
        )

        derivatives = derivatives_result["derivatives"]

        # For each derivative, find its competitors
        for derivative in derivatives:
            # Get competitors specific to this derivative
            derivative_competitors = await self.get_competitors(
                derivative["name"], derivative["description"]
            )

            # Add competitor insights to derivative description
            if derivative_competitors:
                competitor_insights = ", ".join(
                    [
                        f"""{comp["name"]} ({comp["key_differentiators"][0] if comp["key_differentiators"] else 'N/A'})"""
                        for comp in derivative_competitors[:2]
                    ]
                )
                derivative["description"] += f"\nKey competitors: {competitor_insights}"

        logger.info(
            f"Identified {len(derivatives)} product derivatives with competitor analysis"
        )
        return derivatives

    async def analyze(self) -> CompetitiveAnalysisReport:
        """Comprehensive competitive analysis workflow"""
        total_start_time = perf_counter()
        logger.info(f"Starting analysis for: {self.product_name}")

        # Get main product competitors
        competitors = await self.get_competitors()
        derivatives = await self.get_derivatives()

        total_elapsed = perf_counter() - total_start_time
        logger.info(f"Completed analysis in {total_elapsed:.2f} seconds")

        report = CompetitiveAnalysisReport(
            product_name=self.product_name,
            competitors=competitors,
            derivatives=derivatives,
        )

        # Store the report in Pinecone
        await self.pinecone.aupsert_documents(
            documents=[report.model_dump_json()],
            metadata=[
                {
                    "type": "competitive_analysis",
                    "product_name": self.product_name,
                    "timestamp": datetime.now().isoformat(),
                }
            ],
        )

        logger.info(
            f"Successfully stored competitive analysis report for {self.product_name} in Pinecone"
        )

        return report


router = APIRouter(
    prefix="/competitive-intelligence", tags=["competitive_intelligence"]
)


@router.post("/analyze")
async def competitive_analysis_endpoint(
    product_name: str, product_description: str
) -> CompetitiveAnalysisReport:
    """FastAPI endpoint for competitive analysis"""
    analyzer = CompetitiveAnalyzer(product_name, product_description)
    return await analyzer.analyze()
