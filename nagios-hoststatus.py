#!/usr/bin/python
################################################################################
#
#	Program:	nagios-hoststatus.py
#
#	Author:		Tim Schaefer, tim@asystemarchitect.com
#
#	Description:	Walks through Nagios' status.dat and displays
#			information similar to the display in Nagios' 
#			web-browser interface.
#
#			This program lists host-status information only.
#
#	License:	This program is shareware. I own it but I'm sharing.
#
################################################################################
#
# Field Reference
#
# hoststatus {
# host_name=monarch-000.atob.me
# modified_attributes=0
# check_command=check-host-alive
# check_period=24x7
# notification_period=workhours
# check_interval=5.000000
# retry_interval=1.000000
# event_handler=
# has_been_checked=1
# should_be_scheduled=1
# check_execution_time=4.016
# check_latency=0.244
# check_type=0
# current_state=0
# last_hard_state=0
# last_event_id=628
# current_event_id=634
# current_problem_id=0
# last_problem_id=275
# plugin_output=PING OK - Packet loss = 0%, RTA = 0.31 ms
# long_plugin_output=
# performance_data=rta=0.307000ms;3000.000000;5000.000000;0.000000 pl=0%;80;100;0
# last_check=1350362683
# next_check=1350362993
# check_options=0
# current_attempt=1
# max_attempts=10
# state_type=1
# last_state_change=1347173854
# last_hard_state_change=1347173854
# last_time_up=1350362693
# last_time_down=1347173727
# last_time_unreachable=0
# last_notification=0
# next_notification=0
# no_more_notifications=0
# current_notification_number=0
# current_notification_id=0
# notifications_enabled=1
# problem_has_been_acknowledged=0
# acknowledgement_type=0
# active_checks_enabled=1
# passive_checks_enabled=1
# event_handler_enabled=1
# flap_detection_enabled=1
# failure_prediction_enabled=1
# process_performance_data=1
# obsess_over_host=1
# last_update=1350362903
# is_flapping=0
# percent_state_change=0.00
# scheduled_downtime_depth=0
#
################################################################################

def prt_help():

    global timestamp

    help="""
--------------------------------------------------------------------------------
nagios-hostatus.py 
Copyright (c) 2012 Tim Schaefer All Rights Reserved - tim@asystemarchitect.com

Usage : ./nagios-hoststatus.py [D] [--help]

Options:

	D - produces detailed information on each host
"""

    print timestamp
    print help

    return 0

################################################################################

def prt_heading():
    global timestamp
    print "%7s %-30s %-10s %-24s %-24s %-24s %s" % ( "Checked" ,"Host Name", "State", "Last Check", "Next Check", "Check Command", "Plugin Output" )
    return 0

################################################################################

def prt_host_info():
    global timestamp
    global rows
    printflag = 0

    if details != 'D':
       prt_heading()

    for line in rows:
        if "}" in line:
           if printflag == 1:
              printflag = 0
              # print line

        if "hoststatus {" in line:
           printflag = 1

        if printflag == 1:
           words  = line.split("=")

           if 'host_name' in line:
              host_name = words[1]

           if 'has_been_checked' in line:
              has_been_checked = words[1]

           if 'check_command' in line:
              check_command = words[1]

           if 'current_state' in line:
              current_state = int(words[1])
              if current_state == 0: 
                 p_current_state = "OK" 
              if current_state == 1: 
                 p_current_state = "WARNING" 
              if current_state == 2: 
                 p_current_state = "CRITICAL" 
              if current_state == 3: 
                 p_current_state = "UNKNOWN" 

           if re.search( "^plugin_output",line) :
              plugin_output = line
              plugin_output = plugin_output.replace( "plugin_output=","" )

           if 'last_check' in line:
              last_check = float( words[1] )
              l_time = datetime.datetime.fromtimestamp( last_check )

           if 'next_check' in line:
              next_check = float( words[1] )
              n_time = datetime.datetime.fromtimestamp( next_check )

              if details == 'D':
                 print "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" 
                 prt_heading()

              print "%7s %-30s %-10s %-24s %-24s %-24s %s" % ( has_been_checked,host_name,p_current_state,l_time,n_time,check_command,plugin_output )
              if details == 'D':
                 prt_details( host_name )
                 print

    return 0

################################################################################

def prt_details( p_host_name ):

    global rows
    global timestamp

    printflag = 0 
    hostflag  = 0 

    last_state_change        = "" 
    l_last_state_change      = "" 
    last_hard_state_change   = "" 
    l_last_hard_state_change = "" 
    last_time_up             = "" 
    l_last_time_up           = "" 
    last_time_down           = "" 
    l_last_time_down         = "" 
    last_update              = "" 
    l_last_update            = "" 
    last_time_unreachable    = "" 
    l_last_time_unreachable  = "" 
    last_notification        = "" 
    l_last_notification      = "" 
    next_notification        = "" 
    l_next_notification      = "" 
    is_flapping              = ""
    l_is_flapping            = ""
    flap_detection_enabled   = ""
    l_flap_detection_enabled = ""
    notifications_enabled    = "" 
    l_notifications_enabled  = "" 
    check_execution_time     = ""
    check_latency            = ""
    check_interval           = "" 
    retry_interval           = "" 
    notification_period      = ""

    for line in rows:
        if "}" in line:
           if printflag == 1:
              printflag = 0

        if "hoststatus {" in line:
           printflag = 1

        if printflag == 1:
           words  = line.split("=")

           if 'host_name' in line:
              if words[1] == p_host_name:
                 host_name = words[1]
                 hostflag = 1
              else:
                 hostflag = 0 

           if hostflag == 1:

              if 'current_attempt' in line:
                 current_attempt = words[1]

              if 'max_attempts' in line:
                 max_attempts = words[1]

              if 'check_execution_time' in line:
                 check_execution_time = float( words[1] )

              if 'check_latency' in line:
                 check_latency = float( words[1] )

              if 'check_interval' in line:
                 check_interval = float( words[1] )

              if 'retry_interval' in line:
                 retry_interval = float( words[1] )

              if 'notification_period' in line:
                 notification_period = words[1]

              if 'flap_detection_enabled' in line:
                 flap_detection_enabled = int( words[1] )
                 if flap_detection_enabled == 1 :
                    l_flap_detection_enabled = 'Y'
                 if flap_detection_enabled != 1 :
                    l_flap_detection_enabled = 'N'

              if 'notifications_enabled' in line:
                 notifications_enabled = int( words[1] ) 
                 if notifications_enabled == 1 :
                    l_notifications_enabled = 'Y'
                 if notifications_enabled != 1 :
                    l_notifications_enabled = 'N'


              if 'last_state_change' in line:
                 if words[1] != '0':
                    last_state_change = float( words[1] )
                    l_last_state_change = datetime.datetime.fromtimestamp( last_state_change )
                 else:
                    l_last_state_change = ""

              if 'last_hard_state' in line:
                 if words[1] != '0':
                    last_hard_state = float( words[1] )
                    l_last_hard_state = datetime.datetime.fromtimestamp( last_hard_state )
                 else:
                    l_last_hard_state =  ""

              if 'last_time_up' in line:
                 if words[1] != '0':
                    last_time_up = float( words[1] )
                    l_last_time_up = datetime.datetime.fromtimestamp( last_time_up )
                 else:
                    l_last_time_up = ""

              if 'last_time_down' in line:
                 if words[1] != '0':
                    last_time_down = float( words[1] )
                    l_last_time_down = datetime.datetime.fromtimestamp( last_time_down )
                 else:
                    l_last_time_down = ""

              if 'last_time_unreachable' in line:
                 if words[1] != '0':
                    last_time_unreachable = float( words[1] )
                    l_last_time_unreachable = datetime.datetime.fromtimestamp( last_time_unreachable )
                 else:
                    l_last_time_unreachable = ""

              if 'last_notification' in line:
                 if words[1] != '0':
                    last_notification = float( words[1] )
                    l_last_notification = datetime.datetime.fromtimestamp( last_notification )
                 else:
                    l_last_notification = ""

              if 'next_notification' in line:
                 if words[1] != '0':
                    next_notification = float( words[1] )
                    l_next_notification = datetime.datetime.fromtimestamp( next_notification )
                 else:
                    l_next_notification = ""

              if 'last_update' in line:
                 if words[1] != '0':
                    last_update = float( words[1] )
                    l_last_update = datetime.datetime.fromtimestamp( last_update )
                 else:
                    l_last_update = ""

              if 'is_flapping' in line:
                 is_flapping = words[1]
                 if is_flapping == '1':
                    l_is_flapping = "Y"
                 if is_flapping == '0':
                    l_is_flapping = "N"

                 print
                 print "%49s %24s %-16s %-4.4f  %-16s %6s %24s %s " % ( " ", "Check",  "Execution Time", check_execution_time, "Current Attempt", current_attempt, "Flap Detection Enabled?", l_flap_detection_enabled  ) 
                 print "%49s %24s %-16s %-4.4f  %-16s %6s %24s %s " % ( " ", " ", "Latency " , check_latency , "Max Attempts" , max_attempts, "Flapping ?", l_is_flapping )
                 print "%49s %24s %-16s %-4.4f  %-16s %4.4f " % ( " ", " ", "Interval " , check_interval , "Retry Interval" , retry_interval,  )
                 print
                 print "%49s %-24s %-24s %-24s %-24s %-24s %-24s " % ( " ", "Last State Change", "Last Hard State", "Last Time Up", "Last Time Down", "Last Time Unreachable", "" ) 
                 print "%49s %-24s %-24s %-24s %-24s %-24s %-24s " % ( " ", l_last_state_change , l_last_hard_state , l_last_time_up , l_last_time_down , l_last_time_unreachable , "" )
                 print
                 print "%49s %-24s %-24s %-24s %-20s %-s " % ( " ", "Last Update ", "Last Notification", "Next Notification", "Notifications On?", l_notifications_enabled  ) 
                 print "%49s %-24s %-24s %-24s %-20s %-s " % ( " ", l_last_update , l_last_notification , l_next_notification , "Notification Period"  , notification_period  )
                 print

    return 0

################################################################################

import time
import datetime
import re
import sys

today     = datetime.datetime.today()
rows      = [line.strip() for line in open('/var/log/nagios/status.dat')]
details   = ""

timestamp = time.strftime( "%Y-%m-%d %H:%M:%S" )

print "%s" % ( timestamp )

if sys.argv[1:]:
   parg = sys.argv[1]
   if parg == 'D':
      details = 'D'
      prt_host_info()
   if parg == '--help':
      prt_help()
      exit
else:
   prt_host_info()
