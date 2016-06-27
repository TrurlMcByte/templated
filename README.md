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
This example write in folder `/etc/someconf` 2 files using template `test2.tpl` and data from `conf1.json` and `conf2.json`

* `test1.conf` with permissons 0644
* `test2.conf` with permissons 0600 and different `key` value




