from typing import List
from datetime import date
from fastapi import FastAPI, HTTPException, status, Depends
from infrastructure.models import Site, Group, ItalianSite, FrenchSite
from infrastructure.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from sqlalchemy.orm import selectinload
import schemas

app = FastAPI(title="NW Python technical test")

async def can_install_french_site(installation_date: date, db: AsyncSession):
  count = await db.scalar(select(func.count()).where(and_(Site.variant == "french_site", Site.installation_date == installation_date)))
  return count == 0

def is_weekend(date: date):
  return date.weekday() in [5, 6]

async def check_group_types(db: AsyncSession, group_ids: List[int], group_type: str) -> bool:
  count = await db.scalar(
    select(func.count(Group.id)).where(and_(Group.id.in_(group_ids), Group.type == group_type))
  )
  return count == 0

@app.post('/sites', response_model=schemas.Site)
async def create_sites(site: schemas.SiteCreate, db: AsyncSession = Depends(get_db)):
  model_classes = {
    'basic_site': Site,
    'italian_site': ItalianSite,
    'french_site': FrenchSite,
  }

  site_model = model_classes.get(site.variant)
  if not site_model:
      raise HTTPException(status_code=400, detail="Invalid site type specified.")

  if site.variant == 'french_site' and not await can_install_french_site(site.installation_date, db):
    raise HTTPException(status_code=400, detail="Only one French site can be installed per day.")

  if site.variant == 'italian_site' and not is_weekend(site.installation_date):
    raise HTTPException(status_code=400, detail="Italian sites must be installed on weekends.")
  

  if site.group_ids:
    if not await check_group_types(db, site.group_ids, 'group3'):
      raise HTTPException(status_code=400, detail="No site can be associated with `group.type == 'group3'`.")
    groups = await db.execute(select(Group).where(Group.id.in_(site.group_ids)).options(selectinload(Group.sites)))
    groups = list(groups)
    
  new_site = site_model(**site.dict(exclude={'variant', 'group_ids'}))
  db.add(new_site)
  await db.commit()
  await db.refresh(new_site)

  # Add groups to the site
  if site.group_ids:
    new_site.groups = groups
    await db.commit()
    await db.refresh(new_site)
  
  return new_site

@app.post('/groups', response_model=schemas.Group)
async def create_groups(group: schemas.GroupCreate, db: AsyncSession=Depends(get_db)):
  new_group = Group(**group.dict())
  db.add(new_group)
  await db.commit()
  await db.refresh(new_group)
  return new_group

@app.get('/sites', response_model=List[schemas.Site])
async def list_sites(skip: int= 0, limit: int=100,  db: AsyncSession =Depends(get_db)):
  result = await db.execute(select(Site).offset(skip).limit(limit))
  sites = result.scalars().all()
  return sites


@app.get('/groups', response_model=List[schemas.Group])
async def list_groups(skip: int= 0, limit: int=100, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(Group).offset(skip).limit(limit))
  groups = result.scalars().all()
  return groups


@app.patch("/sites/{site_id}", response_model=schemas.Site)
async def update_site(site_id: int, site: schemas.SiteUpdate, db: AsyncSession=Depends(get_db)):
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
async def update_group(group_id: int, group: schemas.GroupUpdate, db: AsyncSession=Depends(get_db)):
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
async def delete_site(site_id: int, db: AsyncSession = Depends(get_db)):
  query = select(Site).filter_by(id=site_id)
  result = await db.execute(query)
  site = result.scalar()
  if site is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site non trouvé")
  await db.delete(site)
  await db.commit()
  return { "ok": True }

@app.delete("/groups/{group_id}")
async def delete_group(group_id: int, db: AsyncSession=Depends(get_db)):
  query = select(Group).filter_by(id=group_id)
  result = await db.execute(query)
  group = result.scalar()
  if group is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
  await db.delete(group)
  await db.commit() 
  return { "ok": True}

