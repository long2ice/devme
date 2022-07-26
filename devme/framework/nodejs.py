from typing import Callable, List, Optional

from devme.enums import FrameworkType
from devme.framework.html import Html
from devme.schema import Env


class NodeJS(Html):
    type = FrameworkType.nodejs
    install_command = "npm i"
    build_command = "npm run build"
    output_dir = "build"

    def __init__(
        self,
        project_name: str,
        git_url: str,
        domains: List[str],
        log_callback: Callable = None,
        image: Optional[str] = None,
        root: str = ".",
        ssl: bool = False,
        output_dir: Optional[str] = None,
        envs: Optional[List[Env]] = None,
        install_command: Optional[str] = None,
        build_command: Optional[str] = None,
    ):
        super().__init__(project_name, git_url, domains, log_callback, image, envs, root, ssl)

        if output_dir:
            self.output_dir = output_dir
        if build_command:
            self.build_command = build_command
        if install_command:
            self.install_command = install_command

    def get_cmds(self):
        return [
            f"git clone {self.git_url} {self.project_name}",
            f"cd {self.source_dir}",
            self.install_command,
            self.build_command,
            f"rm -rf /srv/{self.project_name}",
            f"mv {self.output_dir} /srv/{self.project_name}",
        ]
