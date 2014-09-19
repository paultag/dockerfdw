CREATE EXTENSION multicorn;

DROP FOREIGN TABLE IF EXISTS docker_containers;
DROP FOREIGN TABLE IF EXISTS docker_images;

DROP SERVER IF EXISTS docker_containers;
DROP SERVER IF EXISTS docker_images;


CREATE SERVER docker_containers FOREIGN DATA WRAPPER multicorn options (
    wrapper 'dockerfdw.wrappers.containers.ContainerFdw');

CREATE SERVER docker_image FOREIGN DATA WRAPPER multicorn options (
    wrapper 'dockerfdw.wrappers.images.ImageFdw');


CREATE foreign table docker_containers (
    "id"          TEXT,
    "image"       TEXT,
    "name"        TEXT,
    "names"       TEXT[],
    "privileged"  BOOLEAN,
    "ip"          TEXT,
    "bridge"      TEXT,
    "running"     BOOLEAN,
    "pid"         INT,
    "exit_code"   INT,
    "command"     TEXT[]
) server docker_containers options (
    host 'unix:///run/docker.sock'
);


CREATE foreign table docker_images (
    "id"              TEXT,
    "architecture"    TEXT,
    "author"          TEXT,
    "comment"         TEXT,
    "parent"          TEXT,
    "tags"            TEXT[]
) server docker_image options (
    host 'unix:///run/docker.sock'
);


SELECT docker_containers.ip, docker_containers.names, docker_images.tags
  FROM docker_containers
  RIGHT JOIN docker_images
  ON docker_containers.image=docker_images.id;
