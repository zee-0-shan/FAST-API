'''
minimal API written using FastAPI
'''

from fastapi import Depends, FastAPI, status, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from .database import SessionLocal, engine



app=FastAPI()

# Migrating all the tables into the database
models.Base.metadata.create_all(bind=engine)

def get_db():
    '''
    getting the database for current session
    '''
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    """
    Displays the minimal Landing Page.
    """
    return "Welcome to the API. For more details, refer to /docs."


@app.post("/address", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Address, db: Session = Depends(get_db)):
    #creating address with longitude and latitude
    location=request.location
    longitude=request.longitude
    latitude=request.latitude
    new_address=models.address(location,longitude,latitude)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


@app.put("/address/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_address(id,request:schemas.Address,db: Session = Depends(get_db)):
    '''
    updating an address which is present in database
    '''
    address=db.query(models.address).filter(models.address.id==id)
    if not address.first():
        detail=f"Address with id {id} is not present in the database"
        status_code=status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code,detail)
    value={"location": request.location,"longitude":request.longitude,"latitude":request.latitude}
    address.update(value)
    db.commit()
    return request


@app.delete("/address/{id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy_address(id,db: Session = Depends(get_db)):
    '''
    deleting address of a particular id
    '''
    address=db.query(models.address).filter(models.address.id==id)
    if not address.first():
        status_code=status.HTTP_404_NOT_FOUND
        detail=f"Address with id {id} is not present in the database"
        raise HTTPException(status_code,detail)
    address.delete(synchronize_session=False)
    db.commit()
    return f"address with id {id} deleted successfully"


@app.get("/address/{id}", status_code=status.HTTP_202_ACCEPTED)
def show_address(id, db: Session = Depends(get_db)):
    '''
    getting an address from the database using id
    '''
    address=db.query(models.address).filter(models.address.id==id).first()
    if not address:
        status_code=status.HTTP_404_NOT_FOUND
        detail=f"Address with id {id} doesn't exists"
        raise HTTPException(status_code,detail)
    return address


@app.get("/address", status_code=status.HTTP_202_ACCEPTED)
def all_addresses(db: Session = Depends(get_db)):
    '''
    getting all the address from the database
    '''
    addresses= db.query(models.address).all()
    return addresses


@app.get("/getclosest",status_code=status.HTTP_202_ACCEPTED)
def get_closest_address(lat:int, lng:int, dst:int,db: Session = Depends(get_db)):
    """
    Endpoint to get closest addresses to
    given address and distance
    """
    address= db.query(models.address).all()
    res =[]
    for adr in address:
        if (int(adr.latitude)-lat)**2 + (int(adr.longitude)-lng)**2 <= dst*2:
            res.append(adr)
    return res
