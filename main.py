# import uvicorn
from fastapi import FastAPI

from routes import bookRouter,userRouter
from middleware.middleware import register_middleware
import psycopg2
from psycopg2.extras import RealDictCursor

from db.dbConnect import engine
from models import Base



app = FastAPI()

# middleware
register_middleware(app)

#model
Base.metadata.create_all(engine)



app.include_router(bookRouter.book_router)
app.include_router(userRouter.user_router)








