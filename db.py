from sqlmodel import SQLModel, create_engine , Session, Field as SQLfield , select
from fastapi import FastAPI, Depends, HTTPException
from pydantic import Field


class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: int | None = None


class Hero(HeroBase, table=True):
    id: int | None = SQLfield(default=None, primary_key= True)


class HeroPublic(SQLModel):
    id: int
    name: str
    age: int | None = None


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

engine = create_engine ("sqlite:///heroes.db", echo=True)


print('db.py file is working correctly! - This is for test')



def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.on_event('startup')
async def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post('/heroes/', response_model=HeroPublic)
async def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero



@app.get('/heroes/', response_model= list [HeroPublic])
async def read_heroes(session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes


@app.get('/heroes/{hid}')
async def read_hero(hid: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hid)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.delete('/heroes/{hid}/')
async def delete_hero(hid: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hid)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    session.delete(hero)
    session.commit()
    return {'ok': True}


@app.put('/heroes/{hid}', response_model= HeroPublic)
async def update_hero(hid: int, hero_update: HeroUpdate, session: Session = Depends(get_session)):
    hero = session.get(Hero, hid)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero_update.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero, key, value)

    session.add(hero)    
    session.commit()
    session.refresh(hero)

    return hero













#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
# def run() -> None:
#     import uvicorn
#     from pathlib import Path

#     current_module_name = Path(__file__).name[:-3]

#     uvicorn.run(
#         f"{current_module_name}:app",
#         host="0.0.0.0",
#         port=11111,
#         reload=True,
#         forwarded_allow_ips="*",
#     )


# if __name__ == "__main__":
#     run()