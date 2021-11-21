from fastapi import APIRouter

from app.quotes.core import get_quotes
from app.quotes.schemas import SearchQuery, SearchResponse

router = APIRouter()


@router.post("/search/", response_model=SearchResponse)
async def search(data: SearchQuery):
    data = await get_quotes(data=data)
    status, message = (True, "Success") if data else (False, "There are no results")

    return SearchResponse(status=status, message=message, data=data)
