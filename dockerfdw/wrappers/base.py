from multicorn.utils import log_to_postgres
from multicorn import ForeignDataWrapper
import docker
import json


def nully(obj):
    return obj if obj else None


class APIProxy(object):
    def __init__(self, client):
        self._cache = {}
        self.client = client

    def handle(self, id_):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def get(self, id_):
        if id_ in self._cache:
            return self._cache[id_]
        ret = self.handle(id_)
        # log_to_postgres(json.dumps(ret, sort_keys=True, indent=4))
        self._cache[id_] = ret
        return ret


class BaseDockerFdw(ForeignDataWrapper):
    proxy_type = None
    proxy = None

    def __init__(self, fdw_options, fdw_columns):
        super(BaseDockerFdw, self).__init__(fdw_options, fdw_columns)
        self.host = fdw_options['host']
        self.client = docker.Client(base_url=self.host, version='1.12')
        if self.proxy_type:
            self.proxy = self.proxy_type(self.client)
