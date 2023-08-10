#/bin/sh

certbot certonly --standalone -n --email=tb@mi4.fr --agree-tos --domains=test.sso.mi4.fr
cat /etc/letsencrypt/live/test.sso.mi4.fr-0001/privkey.pem /etc/letsencrypt/live/test.sso.mi4.fr-0001/fullchain.pem | tee /etc/letsencrypt/live/test.sso.mi4.fr-0001/haproxy.pem