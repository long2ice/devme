from devme.caddy import Volume

VolumeSite = {"Type": "volume", "Source": Volume.VolumeSiteName, "Target": "/srv"}
VolumeData = {"Type": "volume", "Source": Volume.VolumeDataName, "Target": "/data"}
VolumeConfig = {
    "Type": "volume",
    "Source": Volume.VolumeConfigName,
    "Target": "/config",
}


Volumes = [
    VolumeSite,
    VolumeData,
    VolumeConfig,
]
