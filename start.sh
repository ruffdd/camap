#!/bin/bash
uwsgi --uid nginx -s /tmp/camap.sock --manage-script-name --mount /=server-main:app --plugin python3 &
nginx -g "daemon off;"