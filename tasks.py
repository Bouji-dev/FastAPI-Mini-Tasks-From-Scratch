from sqlmodel import Session
from models import ActivityLog
from datetime import datetime, timezone
from db2 import  get_session, engine
import time



def save_log( endpoint: str, method: str):
    
    
    with Session(engine) as session:
        log = ActivityLog(endpoint=endpoint, method=method)
        session.add(log)
        session.commit()
        print('LOG SAVED:', endpoint, method, datetime.now(timezone.utc))


def send_welcome_email(email: str):
    
    print(f"Sending welcome email to {email}...")
    time.sleep(3)
    print("Email sent!")


def write_log(message: str):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")
