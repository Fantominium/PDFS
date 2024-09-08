from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class Investor(BaseModel):
    investor_name: str
    investor_type: str
    investor_country: str
    investor_date_added: datetime
    investor_last_updated: datetime
    commitment_asset_class: str
    commitment_amount: float
    commitment_currenc: str