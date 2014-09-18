CREATE EXTENSION multicorn;

DROP FOREIGN TABLE IF EXISTS docker_containers;
DROP SERVER IF EXISTS docker_containers;


CREATE SERVER docker_containers FOREIGN DATA WRAPPER multicorn options (
    wrapper 'dockerfdw.wrappers.containers.ContainerFdw'
);

CREATE foreign table docker_containers (
    "id"       TEXT,
    "image"    TEXT,
    "names"    TEXT[],
    "command"  TEXT,
    "created"  TIMESTAMP WITH TIME ZONE
) server docker_containers options (
    host 'unix:///run/docker.sock'
);

SELECT * FROM docker_containers;
