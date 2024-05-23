from sqlalchemy import Column, Integer, ForeignKey
from ..db import Base

class SiteGroup(Base):
    __tablename__ = 'site_group'
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
