from fastapi import FastAPI, UploadFile, BackgroundTasks, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from tasks import save_log, send_welcome_email, write_log
from db2 import create_db, get_session
import time


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

create_db()
templates = Jinja2Templates(directory='templates')

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)
        print(f'Temporary file removed: {path}')

    else:
        print('File does not exist.')   


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post('/upload')
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):

    file_location = f"temp_{file.filename}"

    with open(file_location, 'wb') as f:
        content = await file.read()
        f.write(content)


    background_tasks.add_task(remove_file, file_location)

    return{
        'status': 'uploaded',
        'temp_path': file_location,
        'message': 'File saved temporaroly. It will be removed in background.'
    }    

@app.get("/products")
async def get_products(background_tasks: BackgroundTasks):
    
    background_tasks.add_task(
        save_log,   
        "/products",
        "GET"
    )

    return {"products": ["Laptop", "Mouse"]}


@app.post('/register')
async def register(user_email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_welcome_email, user_email)
    return {"message": "User registered! Email will be sent soon."}


def write_log_to_file(message: str):
    time.sleep(2)
    with open('log.txt', 'a', encoding= 'utf-8') as f:
        f.write(message + '\n')


@app.get('/', response_class=HTMLResponse)        
async def home(request: Request, background_task: BackgroundTasks):
    background_task.add_task(write_log_to_file, 'User visited home page')

    return templates.TemplateResponse(
        'index.html',
        {'request': request, 'message': 'Welcome to home page!'}
    )


def log_user_action(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, 'User accessed protected route')
    return 'dependency done'

@app.get('/dashboard')
def dashboard(dep=Depends(log_user_action)):
    return{'msg': 'Dashboard loaded!'}


def save_username_to_file(username: str):
    with open('users.log', 'a', encoding= 'utf-8') as f:
        f.write(username + '\n')
    print(f'Saved username: {username}')    

@app.post('/register/')
def register_user(username: str, backgroun_tasks: BackgroundTasks):
    backgroun_tasks.add_task(save_username_to_file, username)
    return {'message': 'User registered successfully!', 'usernaem': username}


@app.get("/items", tags=["Items"], summary="لیست آیتم‌ها", description="این مسیر تمام آیتم‌ها را برمی‌گرداند")
def get_items():
    return [{"item_id": 1, "name": "Apple"}, {"item_id": 2, "name": "Banana"}]

@app.post("/items", tags=["Items"], summary="ایجاد آیتم جدید", description="با ارسال اطلاعات آیتم، یک آیتم جدید ایجاد می‌شود")
def create_item(name: str):
    return {"item_id": 3, "name": name}

@app.get("/users", tags=["Users"], summary="لیست کاربران", description="تمام کاربران موجود در سیستم را برمی‌گرداند")
def get_users():
    return [{"user_id": 1, "name": "Ehsan"}, {"user_id": 2, "name": "Ali"}]



















#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
def run() -> None:
    import uvicorn
    from pathlib import Path

    current_module_name = Path(__file__).name[:-3]

    uvicorn.run(
        f"{current_module_name}:app",
        host="0.0.0.0",
        port=11111,
        reload=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    run()