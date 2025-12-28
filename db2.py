from sqlmodel import create_engine, SQLModel, Session

engine = create_engine("sqlite:///./logs.db", echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
