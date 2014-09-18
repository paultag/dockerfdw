from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
from logging import ERROR, DEBUG, INFO, WARNING

import datetime
import docker


class ContainerFdw(ForeignDataWrapper):
    def __init__(self, fdw_options, fdw_columns):
        super(ContainerFdw, self).__init__(fdw_options, fdw_columns)
        self.host = fdw_options['host']
        self.client = docker.Client(base_url=self.host, version='1.12')
        self.spec = {
            "id": lambda x: x['Id'],
            "image": lambda x: x['Image'],
            "names": lambda x: x['Names'],
            "command": lambda x: x['Command'],
            "created": lambda x: datetime.datetime.fromtimestamp(x['Created']),
        }

    def execute(self, quals, columns):
        containers = self.client.containers(all=True)
        for container in containers:
            log_to_postgres(container)
            yield {x: self.spec[x](container) for x in columns}
