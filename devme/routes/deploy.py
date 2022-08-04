from fastapi import APIRouter
from pydantic import BaseModel
from starlette.background import BackgroundTasks

from devme.enums import DeployStatus
from devme.models import Deploy, Domain, Project
from devme.utils import get_framework

router = APIRouter()


@router.get("/{deploy_id}/log")
async def deploy_log(
    deploy_id: int,
):
    d = await Deploy.get(pk=deploy_id).only("log")
    return {"log": d.log}


async def deploy(d: Deploy):
    project = d.project

    async def log_callback(log: str):
        if d.log is None:
            d.log = ""
        d.log += log
        await d.save(update_fields=["log"])

    domains = await Domain.filter(branch=d.branch, project=project).values_list("domain", flat=True)
    framework = get_framework(project.framework)
    f = framework(
        project_name=project.name,
        git_url=project.url,
        image=project.image,
        envs=project.env,
        root=project.root,
        domains=domains,
        **project.deployment,
        log_callback=log_callback,
    )
    await f.build()
    await f.deploy()
    await f.clear()


class DeployProject(BaseModel):
    branch: str


@router.post("")
async def deploy_project(background_tasks: BackgroundTasks, project_id: int, req: DeployProject):
    project = await Project.get(pk=project_id)
    d = await Deploy.create(project=project, status=DeployStatus.running, branch=req.branch)
    background_tasks.add_task(deploy, d)
    return d
