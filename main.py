from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from algorithm import FlagGenerator


class Payload(BaseModel):
    stars: str
    stripes: str
    changesLeft: int


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "https://main.d5g9oyj5u2wzt.amplifyapp.com",
    "http://main.d5g9oyj5u2wzt.amplifyapp.com",
    "main.d5g9oyj5u2wzt.amplifyapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"Root Request": 200}


@app.post("/generate")
async def generate_flag(data: Payload) -> dict:
    if (data.changesLeft > 0):
        generator = FlagGenerator(data.stars, data.stripes)
        generator.compile()
        return generator.upload()
    else:
        return "Error: No changes left!"
