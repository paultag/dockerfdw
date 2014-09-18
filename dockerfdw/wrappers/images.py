from multicorn.utils import log_to_postgres
from logging import ERROR, DEBUG, INFO, WARNING
from .base import BaseDockerFdw

import datetime
import copy


class ImageFdw(BaseDockerFdw):
    spec = {
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
