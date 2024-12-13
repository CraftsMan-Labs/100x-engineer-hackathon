from src.app.models import Base, TimestampMixin
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    company_name = Column(String(255))
    industry = Column(String(100))
    is_active = Column(Boolean, default=True)

    # Relationships
    market_analyses = relationship("MarketAnalysis", back_populates="user")
    customer_profiles = relationship("CustomerProfile", back_populates="user")
    competitor_analyses = relationship("CompetitorAnalysis", back_populates="user")
