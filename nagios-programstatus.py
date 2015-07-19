#!/usr/bin/python
################################################################################
#
#	Program:	nagios-programstatus.py
#
#	Author:		Tim Schaefer, tim@asystemarchitect.com
#
#	Description:	Walks through Nagios' status.dat and displays information
#			on the command-line similar to what you would see in the
#			web-browser.
#
#	License:	This program is shareware. I own it but I'm sharing.
#
################################################################################
#
# Field Reference
# 
# info {
# 	created=1350362903
# 	version=3.4.1
# 	last_update_check=1346369589
# 	update_available=1
# 	last_version=3.3.1
# 	new_version=3.4.1
# 	}
#
# programstatus {
# 	modified_host_attributes=0
# 	modified_service_attributes=0
# 	nagios_pid=32409
# 	daemon_mode=1
# 	program_start=1349903652
# 	last_command_check=1350362902
# 	last_log_rotation=1350284400
# 	enable_notifications=1
# 	active_service_checks_enabled=1
# 	passive_service_checks_enabled=1
# 	active_host_checks_enabled=1
# 	passive_host_checks_enabled=1
# 	enable_event_handlers=1
# 	obsess_over_services=0
# 	obsess_over_hosts=0
# 	check_service_freshness=1
# 	check_host_freshness=0
# 	enable_flap_detection=1
# 	enable_failure_prediction=1
# 	process_performance_data=0
# 	global_host_event_handler=
# 	global_service_event_handler=
# 	next_comment_id=15
# 	next_downtime_id=1
# 	next_event_id=793
# 	next_problem_id=334
# 	next_notification_id=19560
# 	total_external_command_buffer_slots=4096
# 	used_external_command_buffer_slots=0
# 	high_external_command_buffer_slots=104
# 	active_scheduled_host_check_stats=0,5,17
# 	active_ondemand_host_check_stats=0,4,12
# 	passive_host_check_stats=0,0,0
# 	active_scheduled_service_check_stats=4,17,51
# 	active_ondemand_service_check_stats=0,0,0
# 	passive_service_check_stats=16,147,445
# 	cached_host_check_stats=0,4,12
# 	cached_service_check_stats=0,0,0
# 	external_command_stats=18,160,484
# 	parallel_host_check_stats=0,5,17
# 	serial_host_check_stats=0,0,0
# 	}

import time
import datetime
import re

timestamp   = time.strftime( "%Y-%m-%d %H:%M:%S" )

status_file = '/var/log/nagios/status.dat' 
rows = [line.strip() for line in open(status_file)]

def prt_header():
    timestamp   = time.strftime( "%Y-%m-%d %H:%M:%S" )
    global status_file
    today = datetime.datetime.today()
    print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" 
    print "%s - %s - %s" % ( "Nagios Program Status",timestamp,status_file )
    print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" 

    return 0


def prt_prog_info():
    global rows
    printflag = 1 

    created           = "" 
    version           = "" 
    last_update_check = "" 
    update_available  = "" 
    last_version      = ""
    new_version       = ""

    for line in rows:
        if "}" in line:
           if printflag == 1:
              printflag = 0

        if "info  {" in line:
           printflag = 1

        if printflag == 1:
           words  = line.split("=")

           if 'created' in line:
              if words[1] != '0':
                 created = float( words[1] )
                 l_created = datetime.datetime.utcfromtimestamp( created )
              else:
                 created = " "
                 l_created = " "

           if 'version' in line:
              version = words[1]

           if 'last_update_check' in line:
              last_update_check = words[1] 
              if words[1] != '0':
                 last_update_check = float( words[1] )
                 l_last_update_check = datetime.datetime.utcfromtimestamp( last_update_check )
              else:
                 last_update_check = " "
                 l_last_update_check = " "

           if 'update_available' in line:
              update_available = words[1]

           if 'last_version' in line:
              last_version = words[1]

           if 'new_version' in line:
              last_version = words[1] 

              print "%-40s : %s" % ( "created", l_created ) 
              print "%-40s : %s" % ( "version", version ) 
              print "%-40s : %s" % ( "last_update_check", l_last_update_check ) 
              print "%-40s : %s" % ( "update_available", update_available ) 
              print "%-40s : %s" % ( "last_version", last_version ) 
              print "%-40s : %s" % ( "new_version", new_version ) 
              print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" 

    return 0 



def prt_prog_status():
    global rows 
    printflag = 0 

    for line in rows:
        if "}" in line:
           if printflag == 1:
              printflag = 0

        if "programstatus {" in line:
           printflag = 1

        if printflag == 1 :
           words  = line.split("=")
           if 'modified_host_attributes' in line:
              modified_host_attributes = words[1] 

           if 'modified_service_attributes' in line:
              modified_service_attributes = words[1] 

           if 'nagios_pid' in line:
              nagios_pid = words[1] 

           if 'daemon_mode' in line:
              daemon_mode = words[1] 

           if 'program_start' in line:
              if words[1] != '0':
                 program_start = float( words[1] )
                 l_program_start = datetime.datetime.utcfromtimestamp( program_start )
              else:
                 program_start = " "
                 l_program_start = " "

           if 'last_command_check' in line:
              if words[1] != '0':
                 last_command_check = float( words[1] )
                 l_command_check = datetime.datetime.utcfromtimestamp( last_command_check )
              else:
                 last_command_check = " " 
                 l_command_check = " " 

           if 'last_log_rotation' in line:
              if words[1] != '0':
                 last_log_rotation = float( words[1] )
                 l_log_rotation = datetime.datetime.utcfromtimestamp( last_log_rotation )
              else:
                 last_log_rotation = " " 
                 l_log_rotation = " "

           if 'enable_notifications' in line:
              enable_notifications = words[1] 

           if 'active_service_checks_enabled' in line:
              active_service_checks_enabled = words[1] 

           if 'passive_service_checks_enabled' in line:
              passive_service_checks_enabled = words[1] 

           if 'active_host_checks_enabled' in line:
              active_host_checks_enabled = words[1] 

           if 'passive_host_checks_enabled' in line:
              passive_host_checks_enabled = words[1] 

           if 'enable_event_handlers' in line:
              enable_event_handlers = words[1] 

           if 'obsess_over_services' in line:
              obsess_over_services = words[1] 

           if 'obsess_over_hosts' in line:
              obsess_over_hosts = words[1] 

           if 'check_service_freshness' in line:
              check_service_freshness = words[1] 

           if 'check_host_freshness' in line:
              check_host_freshness = words[1] 

           if 'enable_flap_detection' in line:
              enable_flap_detection = words[1] 

           if 'enable_failure_prediction' in line:
              enable_failure_prediction = words[1] 

           if 'process_performance_data' in line:
              process_performance_data = words[1] 

           if 'global_host_event_handler' in line:
              global_host_event_handler = words[1] 

           if 'global_service_event_handler' in line:
              global_service_event_handler = words[1] 

           if 'next_comment_id' in line:
              next_comment_id = words[1] 

           if 'next_downtime_id' in line:
              next_downtime_id = words[1] 

           if 'next_event_id' in line:
              next_event_id = words[1] 

           if 'next_problem_id' in line:
              next_problem_id = words[1] 

           if 'next_notification_id' in line:
              next_notification_id = words[1] 

           if 'total_external_command_buffer_slots' in line:
              total_external_command_buffer_slots = words[1] 

           if 'used_external_command_buffer_slots' in line:
              used_external_command_buffer_slots = words[1] 

           if 'high_external_command_buffer_slots' in line:
              high_external_command_buffer_slots = words[1] 

           if 'active_scheduled_host_check_stats' in line:
              active_scheduled_host_check_stats = words[1] 

           if 'active_ondemand_host_check_stats' in line:
              active_ondemand_host_check_stats = words[1] 

           if 'passive_host_check_stats' in line:
              passive_host_check_stats = words[1] 

           if 'active_scheduled_service_check_stats' in line:
              active_scheduled_service_check_stats = words[1] 

           if 'active_ondemand_service_check_stats' in line:
              active_ondemand_service_check_stats = words[1] 

           if 'passive_service_check_stats' in line:
              passive_service_check_stats = words[1] 

           if 'cached_host_check_stats' in line:
              cached_host_check_stats = words[1] 

           if 'cached_service_check_stats' in line:
              cached_service_check_stats = words[1] 

           if 'external_command_stats' in line:
              external_command_stats = words[1] 

           if 'parallel_host_check_stats' in line:
              parallel_host_check_stats = words[1] 

           if 'serial_host_check_stats' in line:
              serial_host_check_stats = words[1] 

              print "%-40s : %s" % ( "modified_host_attributes", modified_host_attributes ) 
              print "%-40s : %s" % ( "modified_service_attributes", modified_service_attributes ) 
              print "%-40s : %s" % ( "nagios_pid", nagios_pid ) 
              print "%-40s : %s" % ( "daemon_mode", daemon_mode ) 
              print "%-40s : %s" % ( "program_start", l_program_start ) 
              print "%-40s : %s" % ( "last_command_check", l_command_check ) 
              print "%-40s : %s" % ( "last_log_rotation", l_log_rotation ) 
              print "%-40s : %s" % ( "enable_notifications", enable_notifications ) 
              print "%-40s : %s" % ( "active_service_checks_enabled", active_service_checks_enabled ) 
              print "%-40s : %s" % ( "passive_service_checks_enabled", passive_service_checks_enabled ) 
              print "%-40s : %s" % ( "active_host_checks_enabled", active_host_checks_enabled ) 
              print "%-40s : %s" % ( "passive_host_checks_enabled", passive_host_checks_enabled ) 
              print "%-40s : %s" % ( "enable_event_handlers", enable_event_handlers ) 
              print "%-40s : %s" % ( "obsess_over_services", obsess_over_services ) 
              print "%-40s : %s" % ( "obsess_over_hosts", obsess_over_hosts ) 
              print "%-40s : %s" % ( "check_service_freshness", check_service_freshness ) 
              print "%-40s : %s" % ( "check_host_freshness", check_host_freshness ) 
              print "%-40s : %s" % ( "enable_flap_detection", enable_flap_detection ) 
              print "%-40s : %s" % ( "enable_failure_prediction", enable_failure_prediction ) 
              print "%-40s : %s" % ( "process_performance_data", process_performance_data ) 
              print "%-40s : %s" % ( "global_host_event_handler", global_host_event_handler ) 
              print "%-40s : %s" % ( "global_service_event_handler", global_service_event_handler ) 
              print "%-40s : %s" % ( "next_comment_id", next_comment_id ) 
              print "%-40s : %s" % ( "next_downtime_id", next_downtime_id ) 
              print "%-40s : %s" % ( "next_event_id", next_event_id ) 
              print "%-40s : %s" % ( "next_problem_id", next_problem_id ) 
              print "%-40s : %s" % ( "next_notification_id", next_notification_id ) 
              print "%-40s : %s" % ( "total_external_command_buffer_slots", total_external_command_buffer_slots ) 
              print "%-40s : %s" % ( "used_external_command_buffer_slots", used_external_command_buffer_slots ) 
              print "%-40s : %s" % ( "high_external_command_buffer_slots", high_external_command_buffer_slots ) 
              print "%-40s : %s" % ( "active_scheduled_host_check_stats", active_scheduled_host_check_stats ) 
              print "%-40s : %s" % ( "active_ondemand_host_check_stats", active_ondemand_host_check_stats ) 
              print "%-40s : %s" % ( "passive_host_check_stats", passive_host_check_stats ) 
              print "%-40s : %s" % ( "active_scheduled_service_check_stats", active_scheduled_service_check_stats ) 
              print "%-40s : %s" % ( "active_ondemand_service_check_stats", active_ondemand_service_check_stats ) 
              print "%-40s : %s" % ( "passive_service_check_stats", passive_service_check_stats ) 
              print "%-40s : %s" % ( "cached_host_check_stats", cached_host_check_stats ) 
              print "%-40s : %s" % ( "cached_service_check_stats", cached_service_check_stats ) 
              print "%-40s : %s" % ( "external_command_stats", external_command_stats ) 
              print "%-40s : %s" % ( "parallel_host_check_stats", parallel_host_check_stats ) 
              print "%-40s : %s" % ( "serial_host_check_stats", serial_host_check_stats ) 

    return 0

prt_header()
prt_prog_info()
prt_prog_status()

