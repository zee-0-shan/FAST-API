from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def index ():
    return {"data":{"name":"zeeshan", "home":"koderma"}}

@app.get('/about')
def about():
    return {"about":{"hello": "zeeshan"}}