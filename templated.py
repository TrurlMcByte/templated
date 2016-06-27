#!/usr/bin/python

import os, sys, getopt, json, urllib
from jinja2 import Environment, FileSystemLoader

def main(argv):
    usage = """
templated.py
! All the arguments used in the order of declaration
   -t, --templates {DIR}        reset template search path (default is "./")
   -u, --curl {URL}             JSON config urls (multiple)
   -s, --str {JSON-string}      JSON config from string (multiple)
   -c, --cfile {FILE}           JSON config filepath (multiple)
   -f, --file {FILE}            load template from file, render to stdout and exit
   -o, --out {FILE}             write loaded template to file (multiple)
   -p, --perm {PERM}            set permissions for created files (octal integer, default 0644)
   -r, --reset                  reset global config
   --uid {UID}                  set gid for created files (default -1, unchanged)
   --gid {GID}                  set gid for created files (default -1, unchanged)
   -d, --dump                   dump current config and exit
   -v, --verbose                verbose output (to stderr)
"""
    config = {}
    verbose = 0
    templateLoader = FileSystemLoader( searchpath="./" )
    templateEnv = Environment( loader=templateLoader )
    ctemplate = 0
    permissions = 0644
    uid = -1
    gid = -1
    try:
        opts, args = getopt.gnu_getopt(argv,"hru:c:dvf:t:T:o:s:p:",["curl=","cfile=","dump","verbose","file=","templates=","turl=","out=","reset","str=","perm=","uid=","gid="])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt in ("-v", "--verbose"):
            verbose=1
        elif opt in ("--uid"):
             uid = int(arg)
        elif opt in ("--gid"):
             gid = int(arg)
        elif opt in ("-p", "--perm"):
            permissions = int(arg,8)
        elif opt in ("-t", "--templates"):
            templateLoader = FileSystemLoader( searchpath=arg )
            templateEnv = Environment( loader=templateLoader )
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
        elif opt in ("-f", "--file"):
            if verbose:
                print >> sys.stderr, 'render template file', arg
            template = templateEnv.get_template(arg)
            print template.render(config)
            sys.exit()
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
        elif opt in ("-o", "--out"):
            if ctemplate != 0:
                if verbose:
                    print >> sys.stderr, 'render template to file', arg
                fout = os.open(arg, os.O_RDWR|os.O_CREAT)
                os.fchmod(fout, permissions)
                os.fchown(fout, uid, gid)
                os.write(fout,ctemplate.render(config))
                os.close(fout);
            else:
                print >> sys.stderr, 'Error: template is not set for', arg
        elif opt in ("-d", "--dump"):
            if verbose:
                print >> sys.stderr, 'dump global config'
            print json.dumps(config)
            sys.exit()


if __name__ == "__main__":
     main(sys.argv[1:])


#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#
#THIS_DIR = os.path.dirname(os.path.abspath(__file__))
#
#j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
#
#jsonurl = urllib.urlopen('http://home.mcbyte.net/core/conf/conf2.json')
#conf1 = json.loads(jsonurl.read())
#conf2 = json.load(open('conf.json', 'r'))
#total_conf = {key: value for (key, value) in (conf1.items() + conf2.items())}
#
#print j2_env.get_template('test2.conf').render( total_conf )

