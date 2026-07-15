import asyncio
from datetime import date
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.db.task_db import engine, init_db
from app.db.models import User,Task,Project
from app.auth.utils import generate_passwd_hash

async def seed():
    print("Creating tables if they don't exist...")
    await init_db()

    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        print("Inserting sample users...")
        u1 = User(
            username="john_doe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
            password_hash=generate_passwd_hash("password123"),
            is_verified=True
        )
        u2 = User(
            username="jane_smith",
            email="jane@example.com",
            first_name="Jane",
            last_name="Smith",
            password_hash=generate_passwd_hash("password123"),
            is_verified=True
        )
        session.add(u1)
        session.add(u2)
        await session.commit()
        await session.refresh(u1)
        await session.refresh(u2)
        
        print("Inserting sample projects...")
        p1 = Project(
            project_name="Website Redesign",
            task_ids=[],
        )
        session.add(p1)
        await session.commit()
        await session.refresh(p1)

        print("Inserting sample tasks...")
        t1 = Task(
            title="Design Mockups",
            description="Create Figma mockups for the new homepage.",
            status="In Progress",
            due_date=date(2026, 7, 1)
        )
        t2 = Task(
            title="Develop Frontend",
            description="Implement the mockups in React.",
            status="Pending",
            due_date=date(2026, 7, 15)
        )
        session.add(t1)
        session.add(t2)
        await session.commit()

        print("Database has been successfully seeded! ✅")

if __name__ == "__main__":
    asyncio.run(seed())
