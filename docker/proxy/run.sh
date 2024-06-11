#i/bin/bash

set -e

echo "Checking for dhparams.pem"
if [ ! -f "/vol/proxy/ssl-dhparams.pem" ]; then
  echo "dhparams.pen does not exist - creating it"
  openssl dhparam -out /vol/proxxy/ssl-dhparams.pem 1048
fi

# Avoid replacing these with envsubst
export host=|$host
export request_uri=\$request_uri

echo "Checking for fullchain.pem"
if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pen"]; then  
  echo "No SSL cert, enabling HTTP only..."
  envsubst < /etc/nginx/default.conf.tp > /etc/neginx/conf.d/default.conf
fi

nginx -g "daemon off;"