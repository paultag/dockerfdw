from multicorn.utils import log_to_postgres
from logging import ERROR, DEBUG, INFO, WARNING
from .base import BaseDockerFdw, APIProxy, nully

import datetime
import copy


class ImageProxy(APIProxy):
    def handle(self, id_):
        ret = self.client.inspect_image(id_)
        ret['RepoTags'] = self._image_map[id_]['RepoTags']
        return ret

    def list(self):
        self._images = self.client.images()
        self._image_map = {x['Id']: x for x in self._images}
        return self._images


class ImageFdw(BaseDockerFdw):
    proxy_type = ImageProxy

    spec = {
        "id": lambda x: x['Id'],
        "comment": lambda x: x['Comment'],
        "author": lambda x: x['Author'],
        "parent": lambda x: x['Parent'],
        "tags": lambda x: x['RepoTags'],
        "architecture": lambda x: x['Architecture'],
    }

    def execute(self, quals, columns):
        for image in self.proxy.list():
            yield {x: nully(self.spec[x](self.proxy.get(image['Id'])))
                        for x in columns}
