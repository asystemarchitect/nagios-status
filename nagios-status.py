#!/usr/bin/python
################################################################################
#
#	Program:	nagios-status.py
#
#	Author:		Tim Schaefer, tim@asystemarchitect.com
#
#       Latest:		October 2012
#
#	Description:	Walks through Nagios' status.dat and displays 
#			information on the command-line similar to what you 
#			would see in the web-browser.
#
#       This program shows service status information at the host-object level.
#
#	Usage:  
#
#	./nagios-status.py D	
#
#			-- Shows host-object detail information
#
#	./nagios-status.py --host hostname
#
#			-- Shows information for a specific host rather
#			   than the entire list of host-objects available
#
#	./nagios-status.py D --host -hostname-
#
#			-- Shows single-host-object information and detailed 
#			   information for that host-object
#
#	License:	This program is shareware. I own it but I'm sharing.
#
################################################################################

def prt_host_header():
    global timestamp
    global host_counter
    print 
    print 
    print host_counter, timestamp
    print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" 
    print "%7s %-30s %-10s %-24s %-24s %-24s %s" % ( "Checked" ,"Host Name", "State", "Last Check", "Next Check", "Check Command", "Plugin Output" )
    return 0

def prt_service_header( p_host_name ):
    print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" 
    print "%7s %-30s %-20s %-10s %-20s %-20s %s" % ( "Checked" ,"Host Service Checks","Service", "Status", "Last Check", "Next Check", "Plugin Output" )
    print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" 
    return 0

################################################################################

def prt_service_status():

    global hosts
    global host_counter
    global timestamp

    last_host           = "" 
    host_name           = "" 
    has_been_checked    = ""
    service_description = ""
    l_time              = ""
    n_time              = ""
    plugin_output       = ""
    p_host_name         = "" 
    current_state       = "" 
    p_current_state     = "" 
    printflag           = 1
    hostflag            = 1 

    for bigline in hosts:
        if "}" in bigline:
           if printflag == 1:
              printflag = 0

        if "servicestatus {" in bigline:
           printflag = 1

        if printflag == 1:
           words  = bigline.split("=")

           if 'host_name' in bigline:
              host_name = words[1]
              if host_name != last_host:
                 host_counter += 1
                 prt_host_status( host_name )
                 prt_service_header( host_name )
                 p_host_name = host_name
              else:
                 p_host_name = " "

           if 'current_state' in bigline:
              current_state = int(words[1])
              if current_state == 0: 
                 p_current_state = "OK" 
              if current_state == 1: 
                 p_current_state = "WARNING" 
              if current_state == 2: 
                 p_current_state = "CRITICAL" 
              if current_state == 3: 
                 p_current_state = "UNKNOWN" 
   
           if 'has_been_checked' in bigline:
              has_been_checked = words[1]
    
           if 'service_description' in bigline:
              service_description = words[1]
    
           if re.search( "^plugin_output",bigline) :
              plugin_output = bigline
              plugin_output = plugin_output.replace( "plugin_output=","" )
    
           if 'last_check' in bigline:
              last_check = float( words[1] )
              l_time = datetime.datetime.fromtimestamp( last_check )
    
           if 'next_check' in bigline:
              if words[1] != '0':
                 next_check = float( words[1] )
                 n_time = datetime.datetime.fromtimestamp( next_check )
              else:
                 n_time = " "

              print "%7s %-30s %-20s %-10s %-20s %-20s %s" % ( has_been_checked,p_host_name,service_description,p_current_state,l_time,n_time,plugin_output )

           last_host = host_name
    
    return 0 

################################################################################

def prt_host_status( p_host_name ):

    global rows
    global details 
    global host_counter 

    printflag                = 0
    hostflag                 = 0
    has_been_checked         = ""
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
    current_state            = "" 
    p_current_state          = "" 
    l_time                   = ""
    n_time                   = ""
    check_command            = ""
    plugin_output            = ""
    host_name                = ""
    max_attempts             = "" 
    words                    = "" 

    print
    prt_host_header()

    for line in rows:
        if "}" in line:
           if printflag == 1:
              printflag = 0

        if "hoststatus {" in line:
           printflag = 1

        if printflag == 1:
           words  = line.split("=")

           if 'host_name' in line:
              host_name = words[1]
              if words[1] == p_host_name:
                 hostflag = 1
              else:
                 hostflag = 0

           if hostflag == 1:
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
   
                  print "%7s %-30s %-10s %-24s %-24s %-24s %s" % ( has_been_checked,host_name,p_current_state,l_time,n_time,check_command,plugin_output )
 
                  if details == 'D' and host_name == p_host_name:
                     prt_details( host_name )
                     print

    return 0

################################################################################

def prt_details( p_host_name ):

    global rows      
    global host_counter 
    global details

    printflag                = 0 
    hostflag                 = 0 

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
    current_attempt          = ""
    max_attempts             = "" 
    last_hard_state          = "" 
    l_last_hard_state        = "" 

    for line in rows :
        if "}" in line:
           printflag = 0

        if "hoststatus {" in line:
           printflag = 1

        if printflag == 1:
           words  = line.split("=")

           if 'host_name' in line:
              host_name = words[1]
              if host_name == p_host_name:
                 hostflag = 1
              else:
                 hostflag = 0 

           if hostflag == 1:
              if 'current_attempt' in line:
                 current_attempt = words[1]
   
              if 'max_attempts' in line:
                 max_attempts = words[1]
   
              if 'check_execution_time' in line:
                 check_execution_time = words[1] 
                 # check_execution_time = float( words[1] )
   
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
                 notifications_enabled = words[1] 
                 if notifications_enabled == "1" :
                    l_notifications_enabled = 'Y'
                 if notifications_enabled == "0" :
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
    print "%7s %41s %-24s %-24s %-24s %-24s %-24s %-24s " % ( " ", " ", "Last State Change", "Last Hard State", "Last Time Up", "Last Time Down", "Last Time Unreachable", "" ) 
    print "%7s %41s %-24s %-24s %-24s %-24s %-24s %-24s " % ( " ", " ", l_last_state_change , l_last_hard_state , l_last_time_up , l_last_time_down , l_last_time_unreachable , "" )
    print
    print "%7s %41s %-24s %-24s %-24s %-20s %-s " % ( " ", " ", "Last Update ", "Last Notification", "Next Notification", "Notifications On?", l_notifications_enabled  ) 
    print "%7s %41s %-24s %-24s %-24s %-20s %-s " % ( " ", " ", l_last_update , l_last_notification , l_next_notification , "Notification Period"  , notification_period  )
    print
    print "%7s %41s %-16s %6s  %-16s %6s %24s %s " % ( " ", "Check",  "Execution Time", check_execution_time, "Current Attempt", current_attempt, "Flap Detection Enabled?", l_flap_detection_enabled  ) 
    print "%7s %41s %-16s %6s  %-16s %6s %24s %s " % ( " ", " ", "Latency " , check_latency , "Max Attempts" , max_attempts, "Flapping?", l_is_flapping )
    print "%7s %41s %-16s %6s  %-16s %6s "         % ( " ", " ", "Interval " , check_interval , "Retry Interval" , retry_interval,  )

    return 0

################################################################################

import datetime
import time
import re
import sys

today        = datetime.datetime.today()
status_file  = "/var/log/nagios/status.dat"
rows         = [line.strip() for line in open(status_file)]

timestamp    = time.strftime( "%Y-%m-%d %H:%M:%S" )

shosts       = "" 
hosts        = "" 
l_hostarr    = ""
hostarr      = ""
printflag    = 1 
a_host_name  = "" 
words        = "" 
host_counter = 0 
details      = ""
idx          = 0
host_flag    = 0

for parg in sys.argv:

    if parg == '--help':
       prt_help()
       exit

    if parg == 'D':
       details = 'D'

    if parg == '--host':
       idx += 1
       host_flag   = 1
       a_host_name = sys.argv[idx]
       for line in rows:
           if "}" in line:
              printflag = 0
              hostarr   = hostarr + line
              hostarr   = hostarr + "\n" 

           if "servicestatus {" in line:
              if printflag == 0:
                 printflag += 1

              if printflag == 1:
                 hostarr   = hostarr + line
                 hostarr   = hostarr + "\n" 

           if 'host_name' in line:
              words = line.split("=")
              host_name = words[1]
              if host_name == a_host_name:
                 printflag += 1
 
           if printflag == 2:
              hostarr   = hostarr + line
              hostarr   = hostarr + "\n" 

    idx += 1

if host_flag == 1:
   hosts  = hostarr.split('\n')
   shosts = hosts
else:
   hosts  = rows
   shosts = rows

print "Nagios Service Checks // %s // %s // %s " % ( timestamp,status_file,a_host_name )

prt_service_status()
