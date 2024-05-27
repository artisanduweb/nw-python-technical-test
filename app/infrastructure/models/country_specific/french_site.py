from ..site import Site
from sqlalchemy import Column, Integer, ForeignKey

class FrenchSite(Site):
  __tablename__ = 'french_site'
  id = Column(Integer, ForeignKey('sites.id'), primary_key=True)
  useful_energy_at_1_megawatt = Column(Integer)
  __mapper_args__ = {
    'polymorphic_identity': 'french_site',
    'inherit_condition': (id == Site.id)
  }


