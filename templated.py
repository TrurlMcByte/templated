#!/usr/bin/python

import os, sys, getopt, json, urllib, ssl
from jinja2 import Environment, FileSystemLoader, contextfunction


@contextfunction
def get_context(c):
         return c

def main(argv):
    usage = """
templated.py
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
"""
    config = {}
    verbose = 0
    templateLoader = FileSystemLoader( searchpath="./" )
    templateEnv = Environment( loader=templateLoader, extensions=["jinja2.ext.do",] )
    ctemplate = 0
    sslcontext = ssl._create_unverified_context()
    permissions = 0644
    uid = -1
    gid = -1
    try:
        opts, args = getopt.gnu_getopt(argv,"hru:c:dvf:t:T:o:s:p:U:G:",["curl=","cfile=","dump","verbose","file=","templates=","turl=","out=","reset","str=","perm=","uid=","gid="])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt in ("-v", "--verbose"):
            verbose=1
        elif opt in ('-U','--suid'):
            print opt
            uid = int(arg)
        elif opt in ('-G','--sgid'):
            gid = int(arg)
        elif opt in ("-p", "--perm"):
            permissions = int(arg,8)
        elif opt in ("-t", "--templates"):
            templateLoader = FileSystemLoader( searchpath=arg )
            templateEnv = Environment( loader=templateLoader, extensions=["jinja2.ext.do",] )
        elif opt in ("-u", "--curl"):
            jsonurl = urllib.urlopen(arg);
            tconf = json.loads(jsonurl.read())
            config = {key: value for (key, value) in (config.items() + tconf.items())}
            if verbose:
                print >> sys.stderr, 'load config url', arg
        elif opt in ("-c", "--cfile"):
            tconf = json.load(open(arg, 'r'))
            config = {key: value for (key, value) in (config.items() + tconf.items())}
            if verbose:
                print >> sys.stderr, 'load config file', arg
        elif opt in ("-r", "--reset"):
            if verbose:
                print >> sys.stderr, 'reset config to zero'
            config = {}
        elif opt in ("-s", "--str"):
            tconf = json.loads(arg)
            config = {key: value for (key, value) in (config.items() + tconf.items())}
            if verbose:
                print >> sys.stderr, 'load confg from string'
        elif opt in ("-T", "--turl"):
            if verbose:
                print >> sys.stderr, 'load template from url', arg
            tplurl = urllib.urlopen(arg);
            ctemplate = templateEnv.from_string(tplurl.read())
            tplurl.close()
        elif opt in ("-f", "--file"):
            if verbose:
                print >> sys.stderr, 'load template from file', arg
            ctemplate = templateEnv.get_template(arg)
        elif opt in ("-o", "--out"):
            if ctemplate != 0:
                if verbose:
                    print >> sys.stderr, 'render template to file', arg
                fout = os.open(arg,  os.O_WRONLY|os.O_CREAT|os.O_TRUNC)
                os.fchmod(fout, permissions)
                os.fchown(fout, uid, gid)
                ctemplate.globals['context'] = get_context
                ctemplate.globals['callable'] = callable
                os.write(fout,ctemplate.render(config))
                os.close(fout);
            else:
                print >> sys.stderr, 'Error: template is not set for', arg
        elif opt in ("-d", "--dump"):
            if verbose:
                print >> sys.stderr, 'dump global config'
            print json.dumps(config)


if __name__ == "__main__":
     main(sys.argv[1:])


#payload = {'username': 'bob', 'email': 'bob@bob.com'}
#>>> r = requests.put("http://somedomain.org/endpoint", data=payload)
#r.status_code
#r.content