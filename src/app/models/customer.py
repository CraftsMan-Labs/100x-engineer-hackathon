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


class CustomerProfile(Base, TimestampMixin):
    __tablename__ = "customer_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    segment_name = Column(String(255))
    demographics = Column(JSON)
    behaviors = Column(JSON)
    needs = Column(JSON)
    pain_points = Column(JSON)

    user = relationship("User", back_populates="customer_profiles")
    journey_maps = relationship("CustomerJourney", back_populates="profile")


class CustomerJourney(Base, TimestampMixin):
    __tablename__ = "customer_journeys"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("customer_profiles.id"))
    stage_name = Column(String(100))
    touchpoints = Column(JSON)
    satisfaction_score = Column(Float)
    feedback = Column(JSON)

    profile = relationship("CustomerProfile", back_populates="journey_maps")
