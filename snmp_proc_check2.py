#!/usr/bin/python

import netsnmp
import sys
import argparse

#oid = netsnmp.Varbind('sysDescr')
oid = netsnmp.Varbind('HOST-RESOURCES-MIB::hrSWRunName')

def parseargs():
    parser = argparse.ArgumentParser(description='Check process over snmp v2')
    parser.add_argument('-w' '--warning', dest='warning', type=int, help='max or min <nr> amount of procs')
    parser.add_argument('-c' '--critical', dest='critical', type=int, help='max or min <nr> amount of procs || if critical is the lower we assume that lower is worse || if critical is the higher we assume that lower is better || if only warning we assume we only warn if lower || if only critical we assume we are if below critical || we have not set warning or critical (assume we want more than one)')
    parser.add_argument('-H' '--host', dest='host', help='host or ip to query', required=True)
    parser.add_argument('-C' '--community', dest='community', default='public', help='host or ip to query')
    parser.add_argument('-n' '--name', dest='name', help='name of process', required=True)
    args = parser.parse_args()
    return args

def process_result(result, args):
    nr = 0
    for proc in result:
        if proc == args.name:
            nr +=1

    # we have not set warning or critical (assume we want more than one)
    if not args.warning and not args.critical:
        if nr == 0:
            print '"%s" not fount' % args.name
            sys.exit(2)
        if nr > 0:
            print 'Found %s instances of "%s"' % (nr, args.name)
            sys.exit(0)

    #if critical is the lower we assume that lower is worse
    if args.critical and args.warning and args.critical < args.warning:
        if nr < args.critical:
            print 'Found %s instances of "%s"' %  (nr, args.name)
            sys.exit(2)
        if nr < args.warning:
            print 'Found %s instances of "%s"' %  (nr, args.name)
            sys.exit(1)
        print 'Found %s instances of "%s"' %  (nr, args.name)
        sys.exit(0)

    #if critical is the higher we assume that lower is better
    if args.critical and args.warning and args.critical > args.warning:
        print "we test"
        if nr > args.critical:
            print 'Found %s instances of "%s"' %  (nr, args.name)
            sys.exit(2)
        if nr > args.warning:
            print 'Found %s instances of "%s"' %  (nr, args.name)
            sys.exit(1)
        print 'Found %s instances of "%s"' %  (nr, args.name)
        sys.exit(0)

    #if only warning we assume we only warn if lower
    if args.warning and not args.critical:
        if nr < args.warning:
            print 'Found %s instances of "%s"' %  (nr, args.name)
            sys.exit(1)
        print 'Found %s instances of "%s"' %  (nr, args.name)
        sys.exit(0)
    #if only critical we assume we are if below critical
    if args.critical and not args.warning:
        if nr < args.critical:
            print 'Found %s instances of "%s"' %  (nr, args.name)
            sys.exit(2)
        print 'Found %s instances of "%s"' %  (nr, args.name)
        sys.exit(0)

def get_data(args):
    result = netsnmp.snmpwalk(oid, Version = 2, DestHost=args.host, Community=args.community)
    if not result:
        print '\nError getting data from %s' % (args.host)
        sys.exit(2)
    return result

def main():
    args = parseargs()
    data = get_data(args)
    process_result(data,args)
    print "unknown error"
    sys.exit(2)

if __name__ in '__main__':
    main()
