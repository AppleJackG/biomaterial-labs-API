from enum import Enum
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...database import Base
from .schemas import LabStatus


class SummaryTableORM(Base):
    __tablename__ = "summary_table"
    
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)
    # styrol_polymerization_bulk_status: Mapped[bool] = mapped_column(default=False)
    # styrol_polymerization_bulk_mark: Mapped[float] = mapped_column(nullable=True, default=None)
    styrol_polymerization_bulk: Mapped[str] = mapped_column(nullable=True, default=LabStatus.uncompleted)
    
    user = relationship('User', foreign_keys='SummaryTableORM.user_id')


class LabNamesEn(Enum):
    styrol_polymerization_bulk = 'styrol_polymerization_bulk'


class LabNamesEnRu(Enum):
    styrol_polymerization_bulk = "Полимеризация стирола в блоке"