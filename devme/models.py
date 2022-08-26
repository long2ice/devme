from tortoise import Model, fields

from devme.enums import DeployStatus, FrameworkType, GitType


class Project(Model):
    name = fields.CharField(max_length=100, unique=True)
    url = fields.CharField(max_length=200)
    framework = fields.CharEnumField(FrameworkType)
    image = fields.CharField(max_length=200, null=True)
    root = fields.CharField(max_length=50, null=True)
    deployment = fields.JSONField(null=True)
    env = fields.JSONField(null=True)
    git_provider: fields.ForeignKeyNullableRelation["GitProvider"] = fields.ForeignKeyField(
        "models.GitProvider", null=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Domain(Model):
    project: fields.ForeignKeyRelation[Project] = fields.ForeignKeyField("models.Project")
    branch = fields.CharField(max_length=200, default="main")
    domain = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Deploy(Model):
    project: fields.ForeignKeyRelation[Project] = fields.ForeignKeyField("models.Project")
    branch = fields.CharField(max_length=200, default="main")
    log = fields.TextField(null=True)
    status = fields.CharEnumField(DeployStatus)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class GitProvider(Model):
    name = fields.CharField(max_length=200)
    type = fields.CharEnumField(GitType, default=GitType.github)
    token = fields.CharField(max_length=200)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = [("type", "token")]
