#/bin/sh

certbot certonly --standalone -n --email=$1 --agree-tos --domains=$2
for dir in /etc/letsencrypt/live/*/
do
    dir=${dir%*/}
    cat $dir/privkey.pem $dir/fullchain.pem | tee $dir/haproxy.pem
done