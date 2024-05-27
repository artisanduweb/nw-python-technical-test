from ..site import Site
from sqlalchemy import Column, Integer, ForeignKey

class ItalianSite(Site):
  __tablename__ = 'italian_site'
  id = Column(Integer, ForeignKey('sites.id'), primary_key=True)
  efficiency = Column(Integer)
  __mapper_args__ = {
    'polymorphic_identity': 'italian_site',
    'inherit_condition': (id == Site.id)
  }


