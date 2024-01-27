#/bin/bash
envsubst < /usr/share/nginx/html/assets/api.json > /tmp/api.json.tmp
mv /tmp/api.json.tmp /usr/share/nginx/html/assets/api.json