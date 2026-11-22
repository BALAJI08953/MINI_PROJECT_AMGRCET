from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class GenerationCompany(Base):
    __tablename__ = "generation_companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    location: Mapped[str] = mapped_column(String(120))
    plants: Mapped[list["Plant"]] = relationship(back_populates="company", cascade="all, delete-orphan")


class Plant(Base):
    __tablename__ = "plants"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("generation_companies.id"))
    name: Mapped[str] = mapped_column(String(120))
    location: Mapped[str] = mapped_column(String(120))
    generation_type: Mapped[str] = mapped_column(String(30))
    capacity_mw: Mapped[float] = mapped_column(Float)
    current_generation_mw: Mapped[float] = mapped_column(Float)
    daily_generation_mwh: Mapped[float] = mapped_column(Float)
    availability_pct: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30))
    renewable: Mapped[bool] = mapped_column(Boolean)
    reading_at: Mapped[str] = mapped_column(String(40))
    company: Mapped[GenerationCompany] = relationship(back_populates="plants")


class Utility(Base):
    __tablename__ = "utilities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    region: Mapped[str] = mapped_column(String(120))
    demand_mw: Mapped[float] = mapped_column(Float)
    received_mw: Mapped[float] = mapped_column(Float)
    supplied_mw: Mapped[float] = mapped_column(Float)
    losses_mw: Mapped[float] = mapped_column(Float)
    losses_pct: Mapped[float] = mapped_column(Float)
    active_outages: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30))
    reading_at: Mapped[str] = mapped_column(String(40))
    substations: Mapped[list["Substation"]] = relationship(back_populates="utility", cascade="all, delete-orphan")


class Substation(Base):
    __tablename__ = "substations"
    id: Mapped[int] = mapped_column(primary_key=True)
    utility_id: Mapped[int] = mapped_column(ForeignKey("utilities.id"))
    name: Mapped[str] = mapped_column(String(120))
    location: Mapped[str] = mapped_column(String(120))
    utility: Mapped[Utility] = relationship(back_populates="substations")
    feeders: Mapped[list["Feeder"]] = relationship(back_populates="substation", cascade="all, delete-orphan")


class Feeder(Base):
    __tablename__ = "feeders"
    id: Mapped[int] = mapped_column(primary_key=True)
    substation_id: Mapped[int] = mapped_column(ForeignKey("substations.id"))
    name: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(30))
    substation: Mapped[Substation] = relationship(back_populates="feeders")
    transformers: Mapped[list["Transformer"]] = relationship(back_populates="feeder", cascade="all, delete-orphan")


class Transformer(Base):
    __tablename__ = "transformers"
    id: Mapped[int] = mapped_column(primary_key=True)
    feeder_id: Mapped[int] = mapped_column(ForeignKey("feeders.id"))
    name: Mapped[str] = mapped_column(String(120))
    capacity_kva: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30))
    feeder: Mapped[Feeder] = relationship(back_populates="transformers")
