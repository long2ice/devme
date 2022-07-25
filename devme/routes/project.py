from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_projects():
    pass


@router.post("")
async def create_project():
    pass


@router.post("/{project_id}/deploy")
async def deploy_project():
    pass
