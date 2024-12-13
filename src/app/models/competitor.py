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


class CompetitorAnalysis(Base, TimestampMixin):
    __tablename__ = "competitor_analyses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    competitor_name = Column(String(255))
    market_share = Column(Float)
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    products = Column(JSON)
    pricing_strategy = Column(JSON)

    user = relationship("User", back_populates="competitor_analyses")
    market_positions = relationship("MarketPosition", back_populates="analysis")


class MarketPosition(Base, TimestampMixin):
    __tablename__ = "market_positions"

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey("competitor_analyses.id"))
    dimension = Column(String(100))
    score = Column(Float)
    evidence = Column(JSON)

    analysis = relationship("CompetitorAnalysis", back_populates="market_positions")
