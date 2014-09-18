from multicorn.utils import log_to_postgres
from logging import ERROR, DEBUG, INFO, WARNING
from .base import BaseDockerFdw

import datetime


class ContainerFdw(BaseDockerFdw):
    spec = {
        "id": lambda x: x['Id'],
        "image": lambda x: x['Image'],
        "names": lambda x: x['Names'],
        "command": lambda x: x['Command'],
        "created": lambda x: datetime.datetime.fromtimestamp(x['Created']),
    }

    def execute(self, quals, columns):
        containers = self.client.containers(all=True)
        for container in containers:
            yield {x: self.spec[x](container) for x in columns}
