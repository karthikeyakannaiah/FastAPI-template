# fast api working
# performing CRUD operations
# for startup, enter into the directory and do this
# ~$ uvicorn working:app --reload
from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
'''an endpoint is the point of entry in a communication channel
when two systems are interacting. It refers to touch points of the communication 
between api and server.'''
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"data":"testing"}

@app.get("/about")
def about():
    return {"about":"this is made by fastapi"}

inventory = {
        1:{
            "name":"Milk",
            "price":24,
            "brand":"nandini"
        }
    }
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(default=None,description="The ID of the item",gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item does not exists")
    return inventory[item_id]
# path parameters
# query parameters
@app.get("/get-by-name/{item_id}")
def get_by_name(*,item_id: int,name: Optional[str]=None, test: int):
    for id in inventory:
        if inventory[id]["name"] == name:
            return inventory[id]
    raise HTTPException(status_code=404, detail="Item does not exists")
# /get-by-name?name=Milk
# /get-by-name?name=Milk&test=2
# we can chain both path and query parameters
# /get-by-name/1?name=Milk&test=2
class Item(BaseModel):
    name:str
    price:float
    brand:Optional[str]

@app.post("/create-item/{item_id}")
def create_item(item_id: int,item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=404,detail="Item already exists")
    inventory[item_id]={"name":item.name,"price":item.price, "brand":item.brand}
    # or just do ths -> inventory[item_id] = item
    return inventory[item_id]

class UpdateItem(BaseModel):
    name:Optional[str]=None
    price:Optional[float]=None
    brand:Optional[str]=None
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item does not exists")
    inventory[item_id].update(item)
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="id of the item to be deleted", gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item does not exists")
    del inventory[item_id]
    return {"Success":"item deleted"}
