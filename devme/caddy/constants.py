from enum import Enum

ContainerName = "devme-caddy"
ImageName = "caddy:devme"


class Volume(str, Enum):
    VolumeSiteName = f"{ContainerName}-site"
    VolumeDataName = f"{ContainerName}-data"
    VolumeConfigName = f"{ContainerName}-config"
