# snmp_check_process_icinga2
very simple crap to check nr of processes running over snmp
To be used with icinga2 / icinga or nagios or .. to make coffee

```
usage: snmp_proc_check2.py [-h] [-w--warning WARNING] [-c--critical CRITICAL]
                           -H--host HOST [-C--community COMMUNITY] -n--name
                           NAME

Check process over snmp v2

optional arguments:
  -h, --help            show this help message and exit
  -w--warning WARNING   max or min <nr> amount of procs
  -c--critical CRITICAL
                        max or min <nr> amount of procs || if critical is the
                        lower we assume that lower is worse || if critical is
                        the higher we assume that lower is better || if only
                        warning we assume we only warn if lower || if only
                        critical we assume we are if below critical || we have
                        not set warning or critical (assume we want more than
                        one)
  -H--host HOST         host or ip to query
  -C--community COMMUNITY
                        host or ip to query
  -n--name NAME         name of process
```
