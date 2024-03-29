from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from ...database import Base


class StyrolPolymerizationBulkORM(Base):
    __tablename__ = 'styrol_polymerization_bulk'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=True, default=None)
    load_monomer_g: Mapped[float] = mapped_column(nullable=True, default=None)
    load_monomer_mole: Mapped[float] = mapped_column(nullable=True, default=None)
    load_monomer_mole_g: Mapped[float] = mapped_column(nullable=True, default=None)
    load_initiator_g: Mapped[float] = mapped_column(nullable=True, default=None)
    load_initiator_mole: Mapped[float] = mapped_column(nullable=True, default=None)
    load_initiator_mole_g: Mapped[float] = mapped_column(nullable=True, default=None)
    temperature: Mapped[float] = mapped_column(nullable=True, default=None)
    time: Mapped[float] = mapped_column(nullable=True, default=None)
    polymer_yield_g: Mapped[float] = mapped_column(nullable=True, default=None)
    polymer_yield_percent: Mapped[float] = mapped_column(nullable=True, default=None)
    polymerization_rate_percent: Mapped[float] = mapped_column(nullable=True, default=None)
    polymerization_rate_mole: Mapped[float] = mapped_column(nullable=True, default=None)
    polymer_characteristics_viscosity: Mapped[float] = mapped_column(nullable=True, default=None)
    polymer_characteristics_mol_mass: Mapped[float] = mapped_column(nullable=True, default=None)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped["User"] = relationship(back_populates="styrol_polymerization_bulk")