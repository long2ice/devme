from fastapi import APIRouter

router = APIRouter()


@router.get("/repo")
async def get_git_repos():
    pass


@router.post("/repo/import")
async def import_repo():
    pass
