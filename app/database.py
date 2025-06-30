from sqlmodel import create_engine, SQLModel, Session
from fastapi import HTTPException

sqlite_url = "sqlite:///./task.db"

engine = create_engine(sqlite_url, echo=True) #Note: ensure to make 'echo = false' in production ENV

def init_db():
    SQLModel.metadata.create_all(engine) #creating all tables by scan our models and create it


def get_session():
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


                    #>>>> u need to use another DB like postgres, mysql? <<<<<<<<<<<<
                            # you need to create .env file and put username and pasword
                            # and use getenv from OS lib to load it and create engine  