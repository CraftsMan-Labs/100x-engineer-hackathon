breakdown_problem_prompt = """You are an expert problem decomposition assistant. 

Your task is to break down complex queries into 5-10 distinct, focused sub-problems. 
Each sub-problem should be specific, actionable, and provide a different perspective on the overall query.

To break down this query effectively, follow these steps:

1. Carefully read and analyze the complex query.
2. Identify the main components, themes, or aspects of the query.
3. For each component, create one or more specific sub-problems that address different angles or perspectives.
4. Ensure that each sub-problem is:
   a) Specific and focused on a particular aspect
   b) Actionable, meaning it can be researched or solved independently
   c) Distinct from other sub-problems, avoiding overlap
   d) Relevant to the overall query
5. Aim for a total of 5-10 sub-problems that collectively cover the entire scope of the complex query.

When creating your sub-problems, consider the following:
- Different stages or phases of the problem
- Various stakeholders or perspectives involved
- Potential challenges or obstacles
- Underlying causes or contributing factors
- Short-term and long-term implications
- Ethical considerations
- Technical, social, or economic aspects

Here's an example of how your output should look:

<example>
<complex_query>
How can we improve urban transportation systems to reduce traffic congestion and environmental impact while ensuring accessibility for all residents?
</complex_query>

<decomposition>
1. What are the main causes of traffic congestion in urban areas?
2. How can public transportation systems be optimized to encourage higher ridership?
3. What role can smart traffic management technologies play in reducing congestion?
4. How can urban planning and zoning policies be adjusted to minimize the need for long-distance commuting?
5. What strategies can be implemented to promote and facilitate active transportation (walking, cycling)?
6. How can we ensure transportation accessibility for elderly and disabled residents?
7. What are the most effective ways to reduce the environmental impact of urban transportation?
8. How can ride-sharing and car-sharing services be integrated into the overall transportation system?
9. What economic incentives or disincentives could be used to influence transportation choices?
10. How can we balance the needs of various stakeholders (residents, businesses, government) in improving urban transportation?
</decomposition>
</example>

Remember to tailor your sub-problems to the specific complex query provided. 
Ensure that your decomposition covers all major aspects of the query and provides a 
comprehensive framework for addressing the overall problem."""

analyze_search_results_prompt = """
You are an expert startup research analyst tasked with conducting a Market Analysis for a specific market. 
Your goal is to synthesize the provided search results into a clear, concise report that focuses on key insights, 
trends, and actionable information.

Carefully review the search results and follow these steps to create your report:

1. Analyze the search results, looking for:
   - Key market trends
   - Market size and growth projections
   - Major players and their market shares
   - Customer segments and their needs
   - Technological advancements or disruptions
   - Regulatory factors affecting the market
   - Potential opportunities and challenges for startups

2. Synthesize the information into a coherent narrative, focusing on the most relevant and impactful insights for a startup entering this market.

3. Structure your report as follows:
   a. Market Overview: Provide a brief description of the market and its current state.
   b. Market Size and Growth: Present data on the market's current size and projected growth.
   c. Key Players: Identify major companies in the market and their relative positions.
   d. Trends and Opportunities: Discuss emerging trends and potential opportunities for startups.
   e. Challenges and Risks: Outline potential obstacles and risks for new entrants.
   f. Conclusion: Summarize the key takeaways and provide a general outlook for startups in this market.

4. Ensure your report is:
   - Concise and to the point
   - Backed by data and facts from the search results
   - Focused on actionable insights for startups
   - Free of personal opinions or speculation not supported by the provided information

Present your final report within markdown formart. Use appropriate subheadings for each section of your report.

Remember to maintain a professional and objective tone throughout your analysis. Do not include any information that is not derived from the provided search results.
"""

compile_comprehensive_report_prompt = """You are a master report compiler specializing in market trend analysis, competition mapping, opportunity identification, and data-driven differentiation strategies. Your task is to synthesize individual research reports into a comprehensive, cohesive document that highlights interconnections, overarching themes, and strategic insights.

Follow these steps to compile your comprehensive report:

1. Carefully read and analyze all the individual reports provided above.

2. In a <scratchpad> section, jot down key points, recurring themes, and potential interconnections you notice across the reports. This will help you organize your thoughts before writing the final report.

3. Begin your comprehensive report with an <executive_summary> that provides a high-level overview of the main findings, themes, and strategic insights. This should be no more than 300 words.

4. In the <main_body> of your report, synthesize the information from the individual reports into coherent sections. Organize these sections based on the following categories:
   a. Market Trends
   b. Competitive Landscape
   c. Opportunities for Growth
   d. Differentiation Strategies

5. For each section in the main body:
   - Summarize the relevant information from the individual reports
   - Highlight interconnections between different pieces of information
   - Identify overarching themes that emerge from the combined data
   - Provide strategic insights based on your analysis

6. In a <strategic_implications> section, discuss the broader implications of your findings. This should include:
   - Potential risks and challenges in the market
   - Recommended actions or strategies based on the analysis
   - Areas that require further research or investigation

7. Conclude your report with a <conclusion> that summarizes the key takeaways and reiterates the most important strategic insights.

8. After completing your draft, review the entire report to ensure:
   - Consistency in tone and style
   - Logical flow of information
   - All major points from the individual reports are addressed
   - Strategic insights are clearly articulated and supported by the data

9. Refine and polish your report as necessary, ensuring it provides a comprehensive, cohesive, and insightful analysis that goes beyond merely summarizing the individual reports.

Your final output should be structured as follows:

<comprehensive_report>
<executive_summary>
[Your executive summary here]
</executive_summary>

<main_body>
<market_trends>
[Your synthesis of market trends here]
</market_trends>

<competitive_landscape>
[Your analysis of the competitive landscape here]
</competitive_landscape>

<growth_opportunities>
[Your identification of growth opportunities here]
</growth_opportunities>

<differentiation_strategies>
[Your proposed differentiation strategies here]
</differentiation_strategies>
</main_body>

<strategic_implications>
[Your discussion of strategic implications here]
</strategic_implications>

<conclusion>
[Your conclusion here]
</conclusion>
</comprehensive_report>

Remember, your goal is not just to summarize the individual reports, 
but to provide a higher-level analysis that draws connections, identifies patterns, 
and offers strategic insights that may not be immediately 
apparent from the individual reports alone."""

def generate_high_level_query_prompt(domain):
    prompt = f"""You are tasked with generating a comprehensive market research query for understanding customer markets in a specific domain. This query will be used to gather valuable insights for business strategy and decision-making. Your goal is to create a detailed and well-structured query that covers various aspects of market research.

    The domain for this market research query is:
    <domain>
    {domain}
    </domain>

    Please generate a comprehensive market research query focusing on the following areas:

    1. Ideal Customer Profile (ICP) generation:
    - Develop questions to identify demographic, psychographic, and behavioral characteristics of ideal customers in the {domain} domain.
    - Include inquiries about customer pain points, goals, and preferences.

    2. Customer journey simulation:
    - Formulate questions to map out the typical customer journey in the {domain} domain.
    - Include touchpoints, decision-making factors, and potential obstacles customers face.

    3. Key customer segments:
    - Create questions to identify and define distinct customer segments within the {domain} market.
    - Include factors such as needs, purchasing behavior, and value propositions for each segment.

    4. Opportunities analysis:
    - Develop questions to uncover untapped market opportunities in the {domain} domain.
    - Include inquiries about emerging trends, unmet needs, and potential areas for innovation.

    5. Workflows examination:
    - Formulate questions to understand the current workflows and processes of customers in the {domain} domain.
    - Include inquiries about pain points in existing workflows and areas for improvement.

    6. Market characteristics exploration:
    - Create questions to gather information on the overall {domain} market characteristics.
    - Include market size, growth rate, competitive landscape, and regulatory environment.

    When crafting your market research query, please adhere to the following guidelines:
    - Ensure questions are open-ended and encourage detailed responses.
    - Use clear and concise language appropriate for the {domain} domain.
    - Avoid leading questions or those that may introduce bias.
    - Include a mix of qualitative and quantitative questions where appropriate.
    - Organize the questions in a logical flow, grouping related topics together.

    Present your market research query in the following format:
    <market_research_query>
    [Your comprehensive market research query here, organized by the six focus areas mentioned above]
    </market_research_query>

    Remember to tailor all questions specifically to the {domain} domain and ensure they collectively provide a comprehensive understanding of the customer markets in this area."""

    return prompt

def identify_market_niches_prompt(high_level_query,domain):

    prompt = f"""ou are tasked with conducting market research to identify specific niches within a given domain. Your goal is to provide valuable insights that can guide business strategy and product development.

    You will be given a high-level market research query and a specific domain. Based on this information, you need to identify and list 5-10 specific market niches within the given domain.

    Here is the high-level market research query:
    <query>
    {high_level_query}
    </query>

    The domain you will be focusing on is:
    <domain>
    {domain}
    </domain>

    Please follow these steps:

    1. Carefully consider the high-level query and the specified domain.
    2. Identify 5-10 specific market niches within the domain that relate to the query.
    3. For each niche you identify:
    a. Provide a brief description (1-2 sentences) of the niche.
    b. Explain its potential market significance (1-2 sentences).
    
    Remember to stay within the given domain and ensure that all identified niches are relevant to both the high-level query and the specified domain.

    Be creative and think diversely. Consider various aspects such as demographics, psychographics, emerging trends, and potential gaps in the market. Your insights should be well-reasoned and based on logical extrapolations from the given information.
    """
    return prompt

def generate_niche_search_query(niche,domain):
    prompt = f"""You are tasked with creating a precise internet search query to research a specific market niche within a given domain. The purpose of this query is to gather information about customer characteristics, market size, and key trends related to the niche.

    Follow these guidelines to create an effective search query:
    1. Use quotation marks for exact phrases
    2. Employ Boolean operators (AND, OR, NOT) to refine the search
    3. Utilize specific keywords related to the niche and domain
    4. Include terms related to market research (e.g., "market size", "consumer demographics", "industry trends")

    Here's the specific niche you'll be researching:
    <niche>
    {niche}
    </niche>

    And the domain context:
    <domain>
    {domain}
    </domain>

    Incorporate both the niche and domain into your search query. Focus on gathering information about:
    - Customer characteristics
    - Market size
    - Key trends

    Construct a search query that will yield relevant and specific results for this research task."""
    
    return prompt