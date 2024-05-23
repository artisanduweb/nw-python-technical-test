from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class GroupType(str, Enum):
  group1 = 'group1'
  group2 = 'group2'
  group3 = 'group3'
   

class Group(Base):
  __tablename__ = "groups"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, index=True)
  type = Column(SQLAlchemyEnum(GroupType), nullable=False)
  parent_group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

  sites = relationship('Site', secondary='site_group', back_populates='groups')
  subgroups = relationship('Group', backref='parent_group', remote_side=[id], cascade='all, delete-orphan')
