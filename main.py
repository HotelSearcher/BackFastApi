import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from api.handlers import user_router

app = FastAPI(title="HotelSearcher")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix='/user', tags=['user'])
app.include_router(main_api_router)
class Hotel(BaseModel):
    name: str
    link: list[str]
    min_price: tuple[int, str]

    class Config:
        orm_mode = True

@app.get("/")
async def root():
    hotel = Hotel(name="Hotel", link=["https://nometa.xyz"], min_price=(1337, "https://nometa.xyz"))
    return {"hotels": [hotel]}


@app.post("/test")
async def get_test_10(city_name: str, check_in_date: str, check_out_date: str, visitors_cnt: int):
    res = []
    for i in range(10):
        hotel = Hotel(name=f"{city_name}_Hotel_{i}", link=[f"https://rt.pornhub.com/video?page={i}", f"https://rt.pornhub.com/video?page={i+1}"], min_price=(1488, f"https://rt.pornhub.com/video?page={i}"))
        res.append(hotel)
    return {"hotels": res}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)