from typing import List, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class TrendVisualizationResponse(BaseModel):
    """Response model for market trend visualization"""
    
    img: str = Field(..., description="Base64 encoded image of the trend visualization")
    reason: str = Field(..., description="Detailed reasoning behind the trend visualization")
    insights: List[str] = Field(..., description="Key strategic insights derived from the visualization")

class VisualizationMetadata(BaseModel):
    """Metadata for the visualization"""
    
    title: str = Field(..., description="Title of the visualization")
    x_axis_label: str = Field(..., description="Label for the x-axis")
    y_axis_label: str = Field(..., description="Label for the y-axis")
    metrics: List[str] = Field(..., description="List of metrics visualized")
    date_generated: str = Field(..., description="Timestamp of visualization generation")

class RegionalTrendData(BaseModel):
    """Regional trend data for global analysis"""
    
    region: str = Field(..., description="Geographic region")
    trend_values: List[float] = Field(..., description="Trend values for the region")
    market_size: float = Field(..., description="Market size in billions USD")
    growth_rate: float = Field(..., description="Year-over-year growth rate")
    key_drivers: List[str] = Field(..., description="Key growth drivers for the region")

class DetailedTrendVisualization(TrendVisualizationResponse):
    """Comprehensive trend visualization response"""
    
    metadata: VisualizationMetadata = Field(..., description="Additional metadata about the visualization")
    confidence_score: float = Field(
        ..., 
        ge=0, 
        le=1, 
        description="Confidence score of the trend analysis (0-1)"
    )
    trend_breakdown: Dict[str, List[float]] = Field(
        ..., 
        description="Detailed breakdown of different trend components"
    )
    seasonality_factors: List[str] = Field(
        ..., 
        description="Identified seasonality patterns affecting the trend"
    )
    market_drivers: List[Dict[str, float]] = Field(
        ..., 
        description="Quantified impact of various market drivers"
    )
    prediction_intervals: Dict[str, List[float]] = Field(
        ..., 
        description="Upper and lower bounds for trend predictions"
    )

class GlobalTrendVisualization(DetailedTrendVisualization):
    """Global market trend visualization with regional breakdowns"""
    
    regional_data: Dict[str, RegionalTrendData] = Field(
        ..., 
        description="Regional breakdown of trend data"
    )
    global_market_size: float = Field(
        ..., 
        description="Total global market size in billions USD"
    )
    regional_growth_rates: Dict[str, float] = Field(
        ..., 
        description="Growth rates by region"
    )
    cross_regional_factors: List[Dict[str, float]] = Field(
        ..., 
        description="Factors affecting multiple regions"
    )
    future_predictions: Dict[str, Dict[str, float]] = Field(
        ..., 
        description="Predicted trends by region and timeframe"
    )
    consumer_sentiment: Dict[str, float] = Field(
        ..., 
        description="Consumer sentiment scores by region"
    )
    technology_adoption_rates: Dict[str, List[float]] = Field(
        ..., 
        description="Technology adoption curves by region"
    )
    regulatory_impact_scores: Dict[str, float] = Field(
        ..., 
        description="Impact of regulatory changes by region"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of the global trend analysis"
    )
