from multicorn import ForeignDataWrapper
import docker


class BaseDockerFdw(ForeignDataWrapper):
    def __init__(self, fdw_options, fdw_columns):
        super(BaseDockerFdw, self).__init__(fdw_options, fdw_columns)
        self.host = fdw_options['host']
        self.client = docker.Client(base_url=self.host, version='1.12')
