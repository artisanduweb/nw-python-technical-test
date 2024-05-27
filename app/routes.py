from typing import List
from fastapi import FastAPI, HTTPException, status, Depends
from infrastructure.models import Site, Group, ItalianSite
from infrastructure.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import schemas

app = FastAPI(title="NW Python technical test")

@app.post('/sites', response_model=schemas.Site)
async def create_sites(site: schemas.SiteCreate, db: AsyncSession = Depends(get_session)):
  model_classes = {
    'basic_site': Site,
    'italian_site': ItalianSite,
    'french_site': Site,
  }

  site_model = model_classes.get(site.variant)
  if not site_model:
      raise HTTPException(status_code=400, detail="Invalid site type specified.")

  new_site = Site(**site.dict(exclude={'variant'}))
  db.add(new_site)
  await db.commit()
  await db.refresh(new_site)
  return new_site

@app.post('/groups', response_model=schemas.Group)
async def create_groups(group: schemas.GroupCreate, db: AsyncSession=Depends(get_session)):
  new_group = Group(**group.dict())
  db.add(new_group)
  await db.commit()
  await db.refresh(new_group)
  return new_group

@app.get('/sites', response_model=List[schemas.Site])
async def list_sites(skip: int= 0, limit: int=100,  db: AsyncSession =Depends(get_session)):
  result = await db.execute(select(Site).offset(skip).limit(limit))
  sites = result.scalars().all()
  return sites


@app.get('/groups', response_model=List[schemas.Group])
async def list_groups(skip: int= 0, limit: int=100, db: AsyncSession = Depends(get_session)):
  result = await db.execute(select(Group).offset(skip).limit(limit))
  groups = result.scalars().all()
  return groups


@app.patch("/sites/{site_id}", response_model=schemas.Site)
async def update_site(site_id: int, site: schemas.SiteUpdate, db: AsyncSession=Depends(get_session)):
  query = select(Site).filter_by(id=site_id) 
  result = await db.execute(query)
  existing_site = result.scalar()
  if existing_site is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site non trouvé.")

  for var, value in site.dict(exclude_unset=True).items():
    setattr(existing_site, var, value) 
  
  await db.commit()
  await db.refresh(existing_site)
  return existing_site

@app.patch("/groups/{group_id}", response_model=schemas.Group)
async def update_group(group_id: int, group: schemas.GroupUpdate, db: AsyncSession=Depends(get_session)):
  query = select(Group).filter_by(id=group_id)
  result = await db.execute(query)
  existing_group = result.scalar()
  if existing_group is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Groupe non trouvé")
  
  for var, value in group.dict(exclude_unset=True).items():
    setattr(existing_group, var, value)

  await db.commit()
  await db.refresh(existing_group)
  return existing_group


@app.delete("/sites/{site_id}")
async def delete_site(site_id: int, db: AsyncSession = Depends(get_session)):
  query = select(Site).filter_by(id=site_id)
  result = await db.execute(query)
  site = result.scalar()
  if site is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site non trouvé")
  await db.delete(site)
  await db.commit()
  return { "ok": True }

@app.delete("/groups/{group_id}")
async def delete_group(group_id: int, db: AsyncSession=Depends(get_session)):
  query = select(Group).filter_by(id=group_id)
  result = await db.execute(query)
  group = result.scalar()
  if group is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
  await db.delete(group)
  await db.commit() 
  return { "ok": True}

