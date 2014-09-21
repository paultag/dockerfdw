dockerfwd
=========

PostgreSQL Foreign Data Wrapper for Docker!

Requirements:
-------------

* PostgreSQL 9.2+
* Multicorn 1.0.4
* Fig (optional)

Quick Setup
-----------

_note_: `fig.yml` uses volume mapping, so the host must be able to volume share
to the docker host.

```bash
$ fig build pg
$ fig up -d pg
$ fig logs
```


_note_: password is `docker`

```bash
$ psql -h 127.0.0.1 -p 5432 -U docker -W docker
psql (9.3.5)
Password for user docker:
SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)
Type "help" for help.

docker=# select id, name, pid from docker_containers;
                                id                                |      name      |  pid
------------------------------------------------------------------+----------------+-------
 56995a1e1ebc4a56ffd190db7d09ee526d49e265ae38aa61f3d2d5cafa0add01 | /code_pg_1     | 13076
 0bb24aaa89af5f3cc463b29f7a4e613e0268a2f84c2d3be38941f7238603cd08 | /code_pg_run_5 |
(7 rows)
```
