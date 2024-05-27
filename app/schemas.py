from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from enum import Enum


class SiteBase(BaseModel):
  name: str
  installation_date: date
  max_power_megawatt: float
  min_power_megawatt: float


class SiteCreate(SiteBase):
  variant: str
  useful_energy_at_1_megawatt: Optional[float] = None

class SiteUpdate(SiteBase):
  pass

class Site(SiteBase):
  id: int
  variant: str
  class Config:
    orm_mode = True

class GroupType(str, Enum):
    group1 = 'group1'
    group2 = 'group2'
    group3 = 'group3'

class GroupBase(BaseModel):
  name: str
  type: GroupType

class GroupCreate(GroupBase):
  pass

class GroupUpdate(GroupBase):
  pass

class Group(GroupBase):
  id: int
  sites: List[Site] = []
  class Config:
    orm_mode = True
