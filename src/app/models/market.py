from src.app.models import Base, TimestampMixin
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    JSON,
)
from sqlalchemy.orm import relationship


class MarketAnalysis(Base, TimestampMixin):
    __tablename__ = "market_analyses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    market_size = Column(Float)
    growth_rate = Column(Float)
    market_trends = Column(JSON)
    opportunities = Column(JSON)
    risks = Column(JSON)

    # Relationships
    user = relationship("User", back_populates="market_analyses")
    trend_data = relationship("MarketTrend", back_populates="analysis")


class MarketTrend(Base, TimestampMixin):
    __tablename__ = "market_trends"

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey("market_analyses.id"))
    trend_type = Column(String(100))
    description = Column(String(500))
    confidence_score = Column(Float)
    data_points = Column(JSON)

    analysis = relationship("MarketAnalysis", back_populates="trend_data")
