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


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255))
    description = Column(String(500))
    features = Column(JSON)
    development_stage = Column(String(100))

    feedback = relationship("ProductFeedback", back_populates="product")
    iterations = relationship("ProductIteration", back_populates="product")


class ProductFeedback(Base, TimestampMixin):
    __tablename__ = "product_feedback"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    source = Column(String(100))
    sentiment = Column(Float)
    content = Column(JSON)
    priority = Column(Integer)

    product = relationship("Product", back_populates="feedback")


class ProductIteration(Base, TimestampMixin):
    __tablename__ = "product_iterations"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    version = Column(String(50))
    changes = Column(JSON)
    metrics = Column(JSON)

    product = relationship("Product", back_populates="iterations")
