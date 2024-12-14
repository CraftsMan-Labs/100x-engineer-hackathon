import requests
import json
import io
import base64
from PIL import Image

product_name = "100 x Engineers"
product_description = "GenAI edutech"
domain = "Edutech and GenAI"
offerings = "education placements upskilling in GenAI and image disccuioon models"


def chat(messages: list[dict]):
    url = "http://localhost:8000/chat/"
    payload = {"messages": messages}
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return response.text


def competition_analyse(product_name, product_description):
    url = "http://localhost:8000/competitive-intelligence/analyze"
    querystring = {
        "product_name": product_name,
        "product_description": product_description,
    }
    headers = {"accept": "application/json"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    """
    {
  "product_name": "string",
  "competitors": [
    {
      "name": "string",
      "description": "string",
      "main_products": [
        "string"
      ],
      "target_market": "string",
      "key_differentiators": [
        "string"
      ]
    }
  ],
  "derivatives": [
    {
      "name": "string",
      "description": "string",
      "target_market": "string"
    }
  ]
}
    """
    return response.text


def customer_discovery(product_name, product_description, domain, offerings):
    url = "http://localhost:8000/customer-discovery/discover"
    querystring = {
        "product_name": product_name,
        "product_description": product_description,
        "domain": domain,
        "offerings": offerings,
    }
    headers = {"accept": "application/json"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    """
    SAMPLE OUTPUT
    
    {
  "primary_domain": "string",
  "total_market_size": 0,
  "niches": [
    {
      "name": "string",
      "description": "string",
      "market_size": 0,
      "growth_potential": 0,
      "key_characteristics": [
        "string"
      ]
    }
  ],
  "ideal_customer_profile": {},
  "investor_sentiment": {}
}
    """
    return response.text


def market_analysis_visualise(offerings, domain):
    url = "http://localhost:8000/market-analysis/visualize-trend"
    querystring = {"query": f"Product Domain: {domain}  Offerings: {offerings}"}
    headers = {"accept": "application/json"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    """
    SAMPLE OUTPUT:

   {
  "img": "string",
  "reason": "string",
  "insights": [
    "string"
  ],
  "metadata": {
    "title": "string",
    "x_axis_label": "string",
    "y_axis_label": "string",
    "metrics": [
      "string"
    ],
    "date_generated": "string"
  },
  "confidence_score": 1,
  "trend_breakdown": {
    "additionalProp1": [
      0
    ],
    "additionalProp2": [
      0
    ],
    "additionalProp3": [
      0
    ]
  },
  "seasonality_factors": [
    "string"
  ],
  "market_drivers": [
    {
      "additionalProp1": 0,
      "additionalProp2": 0,
      "additionalProp3": 0
    }
  ],
  "prediction_intervals": {
    "additionalProp1": [
      0
    ],
    "additionalProp2": [
      0
    ],
    "additionalProp3": [
      0
    ]
  }
}
    """
    return response.text


def market_analysis(offerings, domain):
    url = "http://localhost:8000/market-analysis/analyze"
    querystring = {"query": f"Product Domain: {domain}  Offerings: {offerings}"}
    headers = {"accept": "application/json"}
    response = requests.request("POST", url, headers=headers, params=querystring)
    """
    SAMPLE OUTPUT:

    {
  "original_query": "string",
  "problem_breakdown": {
    "questions": [
      "string"
    ]
  },
  "search_results": {
    "additionalProp1": {},
    "additionalProp2": {},
    "additionalProp3": {}
  },
  "comprehensive_report": "string"
}

    """
    return response.text


def market_expansion(domain: str, market_report: dict, customer_report: dict):
    url = "http://localhost:8000/market-expansion/expand"
    querystring = {"domain": domain}
    payload = {"customer_report": customer_report, "market_report": market_report}
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.request(
        "POST", url, headers=headers, params=querystring, data=json.dumps(payload)
    )
    """
    SAMPLE OUTPUT: 

    {
  "customer_report": {
    "primary_domain": "string",
    "total_market_size": 0,
    "niches": [
      {
        "name": "string",
        "description": "string",
        "market_size": 0,
        "growth_potential": 0,
        "key_characteristics": [
          "string"
        ]
      }
    ],
    "ideal_customer_profile": {},
    "investor_sentiment": {}
  },
  "market_report": {
    "original_query": "string",
    "problem_breakdown": {
      "questions": [
        "string"
      ]
    },
    "search_results": {
      "additionalProp1": {},
      "additionalProp2": {},
      "additionalProp3": {}
    },
    "comprehensive_report": "string"
  }
}
"""
    return response.text


def product_evolution(
    market_report: dict, customer_report: dict, market_expansion: dict
):
    url = "http://localhost:8000/product-evolution/evolve"
    payload = {
        "customer_report": customer_report,
        "market_report": market_report,
        "market_expansion": market_expansion,
    }
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    """
    SAMPLE OUTPUT

    {
  "customer_report": {
    "primary_domain": "string",
    "total_market_size": 0,
    "niches": [
      {
        "name": "string",
        "description": "string",
        "market_size": 0,
        "growth_potential": 0,
        "key_characteristics": [
          "string"
        ]
      }
    ],
    "ideal_customer_profile": {},
    "investor_sentiment": {}
  },
  "market_report": {
    "original_query": "string",
    "problem_breakdown": {
      "questions": [
        "string"
      ]
    },
    "search_results": {
      "additionalProp1": {},
      "additionalProp2": {},
      "additionalProp3": {}
    },
    "comprehensive_report": "string"
  },
  "market_expansion": {
    "primary_domain": "string",
    "expansion_domains": [
      "string"
    ],
    "strategic_rationale": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "competitive_landscape": {},
    "investment_requirements": {
      "additionalProp1": 0,
      "additionalProp2": 0,
      "additionalProp3": 0
    },
    "risk_assessment": {
      "additionalProp1": 0,
      "additionalProp2": 0,
      "additionalProp3": 0
    },
    "potential_synergies": [
      "string"
    ]
  }
}

    """
    return response.text


def img_b64_str_to_pil_image(img_b64_str):
    image_data = base64.b64decode(img_b64_str)
    image = Image.open(io.BytesIO(image_data))
    return image


def chat_pro_mode(messages: list[dict]):
    url = "http://localhost:8000/chat/god_mode"
    """
    SAMPLE INPUT

    {
  "messages": [
    {
      "role": "user",
      "content": "Can you project the overall user base for Bonsen AI in USA and UK and extraplate possible customer base accouting for wars as well and climate change"
    },
    {
      "role": "assistant",
      "content": "To project the overall user base for Bonsen AI in the USA and UK and account for factors like wars and climate change, we need to consider multiple variables including current market trends, potential impacts of geopolitical events, and environmental changes. Here's a structured approach:\n\n### Current User Base Estimation\n1. **Market Analysis**: \n   - **USA**: The AI market in the USA is large and diverse, with a strong emphasis on automation, data analytics, and cybersecurity. Bonsen AI can target sectors such as finance, healthcare, and manufacturing.\n   - **UK**: The UK market also shows strong demand for AI in similar sectors, with additional focus on AI for regulatory compliance and fintech solutions.\n\n2. **Current User Base**: Estimate the current user base by analyzing Bonsen AI's customer acquisition rate, market penetration, and existing contracts or partnerships.\n\n### Future Projections\n1. **Market Growth Rate**:\n   - Assume a conservative growth rate based on historical data and industry projections. For AI services, a CAGR (Compound Annual Growth Rate) of around 20-30% might be realistic given the rapid adoption of AI technologies.\n\n2. **Geopolitical Factors**:\n   - **Wars**: Conflicts can disrupt markets but also increase demand for specific AI applications like cybersecurity or supply chain management. For instance, tensions could lead to higher investments in defense-related AI applications.\n   - **Climate Change**: This could drive demand for AI in environmental monitoring, disaster response, and sustainable resource management. It might open new sectors for AI applications, increasing the potential user base.\n\n3. **Extrapolation Method**:\n   - Use the current user base and apply the estimated growth rate while adjusting for geopolitical and environmental impacts. For instance, if Bonsen AI currently has 1,000 users in the USA and 500 in the UK, and you expect a 25% growth rate with an additional 10% increase due to climate-related demand:\n     - **USA**: 1,000 * (1 + 0.25 + 0.10) = 1,350 users projected for the next year.\n     - **UK**: 500 * (1 + 0.25 + 0.10) = 675 users projected for the next year.\n\n### Strategic Considerations\n- **Diversification**: Bonsen AI should consider diversifying its offerings to include AI solutions for climate resilience and geopolitical stability.\n- **Partnerships**: Form strategic partnerships with organizations in sectors likely to be affected by these factors.\n\n### Conclusion\nBy considering historical growth rates, market trends, and external factors like geopolitical events and climate change, Bonsen AI can strategically plan for an increased user base in both the USA and UK, potentially reaching 1,350 users in the USA and 675 in the UK over the next year."
    },
    {
      "role": "user",
      "content": "Can you plot the in a gepah strucure assuming I had 120 cusstomers and got 30 new customers last month using out AI prodict accleartor product over the next 3 years in USA and UK and all the BRICS nations . Show potential customer base from all these different nations"
    }
  ]
}


    """
    payload = {"messages": messages}
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    """
    SAMPLE OUTPUT:
    {
  "response": "To visualize the projected customer base growth for Bonsen AI in the USA, UK, and BRICS nations over the next three years, we'll plot the growth assuming a steady monthly acquisition rate and compounding growth. We'll assume the following:\n\n1. **Initial Customer Base**: 120 customers\n2. **Monthly New Customers**: 30 new customers\n3. **Growth Rate**: We'll assume a conservative growth rate of 15% per annum for simplicity.\n\n**BRICS Nations**: Brazil, Russia, India, China, South Africa.\n\nLet's plot the potential growth for each region.",
  "img_bool": true,
  "x_labels": [
    "Year 1",
    "Year 2",
    "Year 3"
  ],
  "y_labels": [
    "USA",
    "UK",
    "Brazil",
    "Russia",
    "India",
    "China",
    "South Africa"
  ],
  "x_values": [
    1,
    2,
    3
  ],
  "y_values": [
    150,
    180,
    210,
    240,
    270,
    300,
    330
  ],
  "title": "Projected Customer Base Growth for Bonsen AI",
  "x_axis_name": "Year",
  "y_axis_name": "Customer Count"
}
    """
    return response.text


# competition_analyse_response = competition_analyse(product_name, product_description)
# competition_analyse_response = json.loads(competition_analyse_response)

# customer_discovery_response = customer_discovery(
#     product_name, product_description, domain, offerings
# )
# customer_discovery_response = json.loads(customer_discovery_response)

# market_analysis_visual_response = market_analysis_visualise(offerings, domain)
# market_analysis_visual_response = json.loads(market_analysis_visual_response)

# img_b64_str_to_pil_image(market_analysis_visual_response["img"])

# market_analysis_response = market_analysis(offerings, domain)
# market_analysis_response = json.loads(market_analysis_response)

# market_expansion_response = market_expansion(
#     domain, market_analysis_response, customer_discovery_response
# )
# market_expansion_response = json.loads(market_expansion_response)

# product_evolution_response = product_evolution(
#     market_analysis_response, customer_discovery_response, market_expansion_response
# )
# product_evolution_response = json.loads(product_evolution_response)

# img_b64_str_to_pil_image(product_evolution_response["visuals"]["img"])

# chat_response = chat(messages=[{"role": "user", "content": "What is the market analysis for Edutech?"}])
