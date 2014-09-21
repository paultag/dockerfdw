#!/bin/bash

# little hack to bypass permissions issues
chmod 777 /run/docker.sock

/start.sh
