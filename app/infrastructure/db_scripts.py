from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update


async def update_variant_column(session: AsyncSession):
    from .models.site import Site 
    await session.execute(
        update(Site)
        .where(Site.variant.is_(None))
        .values(variant='basic_site')
    )
    await session.commit()
