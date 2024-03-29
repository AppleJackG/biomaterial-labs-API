from pydantic import BaseModel, ConfigDict


class StyrolPolymerizationBulkDTO(BaseModel):
    number: int | None
    load_monomer_g: float | None
    load_monomer_mole: float | None
    load_monomer_mole_g: float | None
    load_initiator_g: float | None
    load_initiator_mole: float | None
    load_initiator_mole_g: float | None
    temperature: float | None
    time: float | None
    polymer_yield_g: float | None
    polymer_yield_percent: float | None
    polymerization_rate_percent: float | None
    polymerization_rate_mole: float | None
    polymer_characteristics_viscosity: float | None
    polymer_characteristics_mol_mass: float | None
    
    model_config = ConfigDict(from_attributes=True)