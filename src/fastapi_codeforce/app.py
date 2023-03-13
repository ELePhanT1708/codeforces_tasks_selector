import asyncio
import time
from typing import List, Union

from fastapi import FastAPI, Depends

import logging

import tables
from db import engine, Session, get_session
from router import router, update_tasks

logger = logging.getLogger(__name__)
tables.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='CodeForce tasks API',
    description='API for work with tasks from CodeForce',
    version='1.0.0',
)
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



