from typing import List
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean

Base = declarative_base()


class Exchanger(Base):
    __tablename__ = 'exchangers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(75), nullable=False)
    in_work: Mapped[bool] = mapped_column(Boolean, nullable=False)
    automated_bot: Mapped[bool] = mapped_column(Boolean, nullable=False)
    making_orders: Mapped[bool] = mapped_column(Boolean, nullable=False)
    plan_best_ru: Mapped[int] = mapped_column(Integer, nullable=False)
    plan_best_eng: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String(150), nullable=True)

    which_exchangers: Mapped[List["Monitoring"]] = relationship(
        back_populates="exchanger", cascade="all, delete-orphan"
    )

    plans: Mapped[List["Plan"]] = relationship(
        back_populates="exchanger", cascade="all, delete-orphan"
    )


class Monitoring(Base):
    __tablename__ = 'monitorings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(75), nullable=False)
    link: Mapped[str] = mapped_column(String(75), nullable=False)
    can_do: Mapped[bool] = mapped_column(Boolean, nullable=False)
    description: Mapped[str | None] = mapped_column(String(150), nullable=True)

    exchanger_id: Mapped[int] = mapped_column(Integer, ForeignKey("exchangers.id"))
    exchanger: Mapped["Exchanger"] = relationship(back_populates="which_exchangers")

    plans: Mapped[List["Plan"]] = relationship(
        back_populates="monitoring", cascade="all, delete-orphan"
    )


class Plan(Base):
    __tablename__ = 'plans'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    exchanger_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("exchangers.id"), nullable=False
    )
    exchanger: Mapped["Exchanger"] = relationship(back_populates="plans")

    monitoring_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("monitorings.id"), nullable=False
    )
    monitoring: Mapped["Monitoring"] = relationship(back_populates="plans")

    plan_per_day: Mapped[int] = mapped_column(Integer, nullable=False)
