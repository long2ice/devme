from tortoise import Model, fields

from devme.enums import DeployStatus, FrameworkType


class Project(Model):
    name = fields.CharField(max_length=100, unique=True)
    url = fields.CharField(max_length=200)
    framework = fields.CharEnumField(FrameworkType)
    image = fields.CharField(max_length=200)
    root = fields.CharField(max_length=50)
    deployment = fields.JSONField()
    env = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Deploy(Model):
    project: fields.ForeignKeyRelation["Project"] = fields.ForeignKeyField("models.Project")
    status = fields.CharEnumField(DeployStatus)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
