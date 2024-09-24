import uvicorn
from fastapi import FastAPI

from app.database import Base, engine
from products_router import products_router
from orders_router import orders_router


app = FastAPI()
app.include_router(products_router)
app.include_router(orders_router)


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)