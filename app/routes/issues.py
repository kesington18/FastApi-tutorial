from fastapi import APIRouter

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.get("/")
async def get_issues():
    return []