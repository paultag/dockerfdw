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
    rowid_column = 'id'

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

    def delete(self, id_):
        self.client.stop(id_, timeout=10)
        self.client.remove_container(id_)

    def insert(self, new_values):
        required = ['image']
        blacklist = ['bridge', 'ip', 'pid', 'exit_code', 'id',
                     'running', 'names']
        default = {'privileged': False,
                   'command': None,
                   'name': None,}
        config = {}

        for el in blacklist:
            if el in new_values:
                if new_values[el] is not None:
                    raise ValueError("Error: Can not handle column `%s`" % (el))
                new_values.pop(el)

        for el in required:
            if el not in new_values:
                raise ValueError("Required column `%s' missing." % (el))
            config[el] = new_values.pop(el)

        for el in default:
            if el in new_values:
                config[el] = new_values.pop(el)
            else:
                config[el] = default[el]

        privileged = config.pop("privileged")
        client = self.client.create_container(
            stdin_open=True,
            tty=True,
            detach=False,
            **config
        )
        id_ = client.pop("Id")
        self.client.start(id_, privileged=privileged)

        assert new_values == {}
        return {"id": id_}

    def execute(self, quals, columns):
        for container in self.proxy.list():
            yield {x: nully(self.spec[x](self.proxy.get(container['Id'])))
                        for x in columns}
