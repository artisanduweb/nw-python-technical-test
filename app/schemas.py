from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class SiteBase(BaseModel):
  name: str
  installation_date: date
  max_power_megawatt: float
  min_power_megawatt: float


class SiteCreate(SiteBase):
  useful_energy_at_1_megawatt: Optional[float] = None

class SiteUpdate(SiteBase):
  pass

class Site(SiteBase):
  id: int
  class Config:
    orm_mode = True


class GroupBase(BaseModel):
  name: str
  type: str

class GroupCreate(GroupBase):
  pass

class GroupUpdate(GroupBase):
  pass

class Group(GroupBase):
  id: int
  sites: List[Site] = []
  class Config:
    orm_mode = True
