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

## Limitation
Any JSON data must be object (not string or bare array)

## All parametrs
```
All the arguments used in the order of declaration and can be called multiple times
   -t, --templates {DIR}        reset template search path (default is "./")
   -u, --curl {URL}             JSON config urls
   -s, --str {JSON-string}      JSON config from string
   -c, --cfile {FILE}           JSON config filepath
   -f, --file {FILE}            load template from file
   -T, --turl {URL}             load template from URL
   -o, --out {FILE}             write last loaded template to file
   -p, --perm {PERM}            set permissions for created files (octal integer, default 0644)
   -r, --reset                  reset global config
   -U, --uid {UID}              set uid for created files (default -1, unchanged)
   -G, --gid {GID}              set gid for created files (default -1, unchanged)
   -d, --dump                   dump global config to stdout
   -v, --verbose                verbose output (to stderr)
```
