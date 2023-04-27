from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from algorithm import FlagGenerator


class Payload(BaseModel):
    id: int
    starsUrl: str
    stripesUrl: str
    starsBase64: str
    stripesBase64: str
    starsTitle: str
    stripesTitle: str
    starsSummary: str
    stripesSummary: str
    name: str
    description: str
    lastChanged: int
    changesLeft: int


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "https://americans-flags-nft.herokuapp.com",
    "http://americans-flags-nft.herokuapp.com",
    "americans-flags-nft.herokuapp.com",
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
        generator = FlagGenerator(
            data.id, data.starsUrl, data.stripesUrl, data.starsBase64, data.stripesBase64, data.starsTitle, data.stripesTitle, data.starsSummary, data.stripesSummary, data.name, data.description, data.lastChanged, data.changesLeft)
        generator.compile()
        return generator.upload()
    else:
        return "Error: No changes left!"
