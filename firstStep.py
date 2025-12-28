from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def read_root():
    return{'message': 'Hello Fastapi!'}

@app.get('/status/')
async def get_status():
    return{'status': 'ok', 'app_version': '1.0.0'}

@app.post('/create')
async def create_item():
    return {'action': 'created', 'status': 'True'}

@app.get('/info/')
async def get_info():
    return {'framework': 'fastapi', 'version': 'latest'}