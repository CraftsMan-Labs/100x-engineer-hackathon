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