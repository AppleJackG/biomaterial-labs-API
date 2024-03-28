from pydantic import BaseModel, ConfigDict


class StyrolPolymerizationBulkDTO(BaseModel):
    number: int
    load_monomer_g: float
    load_monomer_mole: float
    load_monomer_mole_g: float
    load_initiator_g: float
    load_initiator_mole: float
    load_initiator_mole_g: float
    temperature: float
    time: float
    polymer_yield_g: float
    polymer_yield_percent: float
    polymerization_rate_percent: float
    polymerization_rate_mole: float
    polymer_characteristics_viscosity: float
    polymer_characteristics_mol_mass: float
    
    model_config = ConfigDict(from_attributes=True)