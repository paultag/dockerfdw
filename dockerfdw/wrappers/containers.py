from multicorn.utils import log_to_postgres
from logging import ERROR, DEBUG, INFO, WARNING
from .base import BaseDockerFdw, APIProxy, nully

import datetime


class ContainerProxy(APIProxy):
    def list(self):
        self._containers = self.client.containers(all=True)
        self._container_map = {x['Id']: x for x in self._containers}
        return self._containers

    def handle(self, id_):
        ret = self.client.inspect_container(id_)
        ret['Names'] = self._container_map[id_]['Names']
        return ret


class ContainerFdw(BaseDockerFdw):
    proxy_type = ContainerProxy

    spec = {
        "id": lambda x: x['Id'],
        "image": lambda x: x['Image'],
        "name": lambda x: x['Name'],
        "names": lambda x: x['Names'],
        "command": lambda x: x['Config']['Cmd'],
        "privileged": lambda x: x['HostConfig']['Privileged'],
        "ip": lambda x: x['NetworkSettings']['IPAddress'],
        "bridge": lambda x: x['NetworkSettings']['Bridge'],
        "running": lambda x: x['State']['Running'],
        "pid": lambda x: x['State']['Pid'],
        "exit_code": lambda x: x['State']['ExitCode'],
    }

    def execute(self, quals, columns):
        for container in self.proxy.list():
            yield {x: nully(self.spec[x](self.proxy.get(container['Id'])))
                        for x in columns}
