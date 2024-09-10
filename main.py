from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from Investors.InvestorService import *
from fastapi.middleware.cors import CORSMiddleware

from typing import List

app = FastAPI()

origins = [
    "https://localhost:3000",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/investors/investorList")
def get_investor_names_and_commitments():
    return sort_by_investor_name();

@app.get("/investors")
def get_investor_commitments(investor_name:str):
    return get_investor_commitment_list(investor_name)

@app.post("/investors/commitmentsByClass")
def read_commitments_by_asset_class(asset_class: str, investor_name: str):
    return filter_commitments_by_asset_class(asset_class, investor_name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)