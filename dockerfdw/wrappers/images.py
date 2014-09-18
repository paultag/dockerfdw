from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres
from logging import ERROR, DEBUG, INFO, WARNING

import datetime
import docker
import copy


class ImageFdw(ForeignDataWrapper):
    def __init__(self, fdw_options, fdw_columns):
        super(ImageFdw, self).__init__(fdw_options, fdw_columns)
        self.host = fdw_options['host']
        self.client = docker.Client(base_url=self.host, version='1.12')
        self.spec = {
            "id": lambda x: x['Id'],
            "repo_tag": lambda x: x['RepoTag'],
            "created": lambda x: datetime.datetime.fromtimestamp(x['Created']),
        }

    def execute(self, quals, columns):
        for image in self.client.images():
            for tag in image['RepoTags']:
                d = copy.copy(image)
                d['RepoTag'] = tag
                yield {x: self.spec[x](d) for x in columns}
