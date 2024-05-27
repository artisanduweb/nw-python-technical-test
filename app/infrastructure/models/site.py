from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from ..db import Base

class Site(Base):
  __tablename__ = 'sites'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  installation_date = Column(Date)
  max_power_megawatt = Column(Float)
  min_power_megawatt = Column(Float)
  useful_energy_at_1_megawatt = Column(Float)
  groups = relationship('Group', secondary='site_group', back_populates='sites')
  
  # kind/type of the site
  variant = Column(String, index=True, default='basic_site')
  __mapper_args__ = {
    'polymorphic_on': variant,
    'polymorphic_identity': 'basic_site' # Default identifier
  }

