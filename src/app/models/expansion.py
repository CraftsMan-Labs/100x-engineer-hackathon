from src.app.models import Base, TimestampMixin
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
    JSON,
)
from sqlalchemy.orm import relationship

class MarketExpansion(Base, TimestampMixin):
    __tablename__ = 'market_expansions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    target_market = Column(String(255))
    market_size = Column(Float)
    entry_strategy = Column(JSON)
    risks = Column(JSON)
    regulations = Column(JSON)
    cultural_factors = Column(JSON)
    
    milestones = relationship("ExpansionMilestone", back_populates="expansion")

class ExpansionMilestone(Base, TimestampMixin):
    __tablename__ = 'expansion_milestones'
    
    id = Column(Integer, primary_key=True)
    expansion_id = Column(Integer, ForeignKey('market_expansions.id'))
    name = Column(String(255))
    status = Column(String(50))
    metrics = Column(JSON)
    completion_date = Column(DateTime)
    
    expansion = relationship("MarketExpansion", back_populates="milestones")