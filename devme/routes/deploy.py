from fastapi import APIRouter
from pydantic import BaseModel, constr
from starlette.background import BackgroundTasks
from starlette.requests import Request

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
    url = project.url
    if project.git_provider:
        git_provider = project.git_provider
        url = url.replace("://", f"://{git_provider.token}@")
    f = framework(
        project_name=project.name,
        git_url=url,
        image=project.image,
        envs=project.env,  # type:ignore
        root=project.root,
        domains=domains,
        branch=d.branch,
        log_callback=log_callback,
        **project.deployment,  # type:ignore
    )
    await f.build()
    await f.deploy()
    await f.clear()
    d.status = DeployStatus.success
    await d.save(update_fields=["status"])


class DeployProject(BaseModel):
    branch: constr(min_length=1, strip_whitespace=True)


@router.post("")
async def deploy_project(background_tasks: BackgroundTasks, project_id: int, req: DeployProject):
    project = await Project.get(pk=project_id).select_related("git_provider")
    d = await Deploy.create(project=project, status=DeployStatus.running, branch=req.branch)
    background_tasks.add_task(deploy, d)
    return d


@router.get("/webhook")
async def deploy_webhook(background_tasks: BackgroundTasks, project_id: int, request: Request):
    body = await request.json()
    ref = body["ref"]
    branch = ref.split("/")[-1]
    project = await Project.get(pk=project_id).select_related("git_provider")
    d = await Deploy.create(project=project, status=DeployStatus.running, branch=branch)
    background_tasks.add_task(deploy, d)
    return d
