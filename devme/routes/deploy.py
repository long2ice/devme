from fastapi import APIRouter

from devme.models import Deploy

router = APIRouter()


@router.get("/{deploy_id}/log")
async def deploy_log(
    deploy_id: int,
):
    d = await Deploy.get(pk=deploy_id).only("log")
    return {"log": d.log}
