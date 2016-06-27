# templated
Dockerized (but not only) simple config generator from templates and JSON data using Jinja2

May collect (and merge) configuration data from JSON URL (including webdis, http://firebase.com or local `etcd`, for example), files, strings and generate config (but not only) files from template files/URLs.

## Simple example
```
docker run --rm \
    -v /etc/someconf:/data \
    $IMG_NAME \
    /templated.py -v \
        -u http://myfirebase.com/conf/conf1.json \
        -u http://myfirebase.com/conf/conf2.json \
        -T http://myfirebase.com/tpl/test2.tpl \
        -s '{"key":"mysecretkey1"}' \
        -o test1.conf \
        -p 0600 \
        -s '{"key":"mysecretkey2"}' \
        -o test2.conf
```
will write 2 in folder `/etc/someconf` files:
`test1.conf` (with permissons 0644)
and `test2.conf` (perms 0600)
with different `key` value

