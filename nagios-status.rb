#!/usr/bin/ruby
################################################################################
#
#	Program:	nagios-status.rb
#
#	Author:		Tim Schaefer, tim@asystemarchitect.com
#
#	Description:	Displays Nagios monitoring information on the command
#			line, similar to what you'd see in a web browser.
#
#	Latest:		October 2012
#
#	License:	This program is shareware. I own it but I'm sharing.
#
################################################################################

def prt_host_header( host_counter, p_host_name )
    printf "\n" 
    printf "\n" 
    printf "%3.3d %s\n", host_counter, p_host_name 
    printf "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n" 
    printf "%7s %-30s %-10s %-24s %-24s %-24s %s\n", "Checked" ,"Host Name", "State", "Last Check", "Next Check", "Check Command", "Plugin Output" 
    printf "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n" 
    return 0
end

################################################################################

def prt_service_header( p_host_name )
    printf "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n" 
    printf "%7s %-30s %-20s %-10s %-20s %-20s %s\n" , "Checked" ,"Host Service Checks","Service", "Status", "Last Check", "Next Check", "Plugin Output" 
    print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n" 
    return 0
end

################################################################################

def prt_host_status( p_host_name, details )

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
    check_command            = ""
    plugin_output            = ""
    host_name                = ""
    max_attempts             = "" 
    words                    = "" 

    h = File.open( "/var/log/nagios/status.dat" )

    while line = h.gets do

        if ( line.match /\}/ )
              printflag = 0
        end

        if ( line.match /hoststatus/  )
           printflag = 1
        end

        if( printflag == 1 )
           words  = line.split("=")

           if ( line.match /host_name/ )
              host_name = words[1].chomp
              if ( host_name === p_host_name )
                 hostflag = 1
              else
                 hostflag = 0
              end
           end

           if ( hostflag == 1 )
              if ( line.match /has_been_checked/  )
                 has_been_checked = words[1].chomp
              end
   
              if ( line.match /check_command/ )
                 check_command = words[1].chomp
              end
   
              if ( line.match /current_state/ )
                 current_state = Integer( words[1].chomp )
                 if current_state == 0
                    p_current_state = "OK" 
                 end

                 if current_state == 1 
                    p_current_state = "WARNING" 
                 end

                 if current_state == 2 
                    p_current_state = "CRITICAL" 
                 end

                 if current_state == 3 
                    p_current_state = "UNKNOWN" 
                 end
              end

              if( line.match /last_check/ ) 
                 last_check = Integer( words[1].chomp )
                 if( last_check > 0 )
                   p_nc = Time.at(last_check)
                   p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                   p_last_check = p_dt
                 end
              end

              if( line.match /next_check/ ) 
                 next_check = Integer( words[1].chomp )
                 if( next_check > 0 )
                   p_nc = Time.at(next_check)
                   p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                   p_next_check = p_dt
                 end
              end
   
              if( line.match /plugin_output/ ) 
		   if ! line.match 'long_plugin_output'
                      plugin_output   = line.chomp
		      p_plug = plugin_output.sub( '	plugin_output=',"" )
		      plugin_output = p_plug
                   end
              end

              if ( line.match /current_attempt/ )
                 current_attempt = words[1].chomp
              end
   
              if ( line.match /max_attempts/ )
                 max_attempts = words[1].chomp
              end
   
              if ( line.match /check_execution_time/ )
                 check_execution_time = words[1].chomp
              end
   
              if ( line.match /check_latency/ )
                 check_latency = words[1].chomp
              end
   
              if ( line.match /check_interval/ )
                 check_interval = words[1].chomp
              end
   
              if ( line.match /retry_interval/ )
                 retry_interval = words[1].chomp
              end
   
              if ( line.match /notification_period/ )
                 notification_period = words[1].chomp
              end
   
              if ( line.match /flap_detection_enabled/ )
                 flap_detection_enabled = Integer( words[1].chomp )
                 if flap_detection_enabled == 1 
                    l_flap_detection_enabled = 'Y'
                 end
                 if flap_detection_enabled != 1 
                    l_flap_detection_enabled = 'N'
                 end
              end
   
              if ( line.match /notifications_enabled/ )
                 notifications_enabled = Integer( words[1].chomp )
                 if notifications_enabled == 1 
                    l_notifications_enabled = 'Y'
                 end
                 if notifications_enabled == 0 
                    l_notifications_enabled = 'N'
                 end
              end
   
              if ( line.match /last_state_change/ )
                 last_state_change = Integer( words[1] )
                 if( last_state_change > 0 )
                     p_nc = Time.at(last_state_change)
                     p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                     l_last_state_change = p_dt
                 end
              end
     
              if ( line.match /last_hard_state/ )
                 last_hard_state = Integer( words[1] )
                 if( last_hard_state > 0 )
                   p_nc = Time.at(last_hard_state)
                   p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                   l_last_hard_state = p_dt
                 else
                   l_last_hard_state = last_hard_state
                 end
              end
         
              if ( line.match /last_time_up/ )
                 last_time_up = Integer( words[1] )
                 if( last_time_up > 0 )
                   p_nc = Time.at(last_time_up)
                   p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                   l_last_time_up = p_dt
                 end
              end
     
              if ( line.match /last_time_down/ )
                 last_time_down = Integer( words[1] )
                 if( last_time_down > 0 )
                    p_nc = Time.at(last_time_down)
                    p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                    l_last_time_down = p_dt
                 end
              end
     
              if ( line.match /last_time_unreachable/ )
                 last_time_unreachable = Integer( words[1] )
                 if( last_time_unreachable > 0 )
                    p_nc = Time.at(last_time_unreachable)
                    p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                    l_last_time_unreachable = p_dt
                 end
              end
     
              if ( line.match /last_notification/ )
                 last_notification = Integer( words[1] )
                 if( last_notification > 0 )
                    p_nc = Time.at(last_notification)
                    p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                    l_last_notification = p_dt
                 end
              end
     
              if ( line.match /next_notification/ )
                 next_notification = Integer( words[1] )
                 if( next_notification > 0 )
                    p_nc = Time.at(next_notification)
                    p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                    l_next_notification = p_dt
                 end
              end
     
              if ( line.match /last_update/ )
                 last_update = Integer( words[1] )
                 if( last_update > 0 )
                    p_nc = Time.at(last_update)
                    p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                    l_last_update = p_dt
                 end
              end
     
              if ( line.match /is_flapping/  )
                 is_flapping = words[1].chomp
                 if is_flapping == '1'
                    l_is_flapping = "Y"
                 end
                 if is_flapping == '0'
                    l_is_flapping = "N"
                 end
              end

               if( line.match /scheduled_downtime_depth/ ) 
                   printflag = 2
               end

              if ( printflag == 2 )

                 printf "%7s %-30s %-10s %-24s %-24s %-24s %s\n" , has_been_checked,host_name,p_current_state,p_last_check,p_next_check,check_command,plugin_output 

                 if ( details === 'Y'  )

                         printf "\n"
                         printf( "%7s %41s %-24s %-24s %-24s %-24s %-24s %-24s\n" , " ", " ", "Last State Change", "Last Hard State", "Last Time Up", "Last Time Down", "Last Time Unreachable", ""  )
                         printf( "%7s %41s %-24s %-24s %-24s %-24s %-24s %-24s\n" , " ", " ", l_last_state_change , l_last_hard_state , l_last_time_up , l_last_time_down , l_last_time_unreachable , ""  )
                         printf "\n"
              
                         printf( "%7s %41s %-24s %-24s %-24s %-20s %-s\n" , " ", " ", "Last Update ", "Last Notification", "Next Notification", "Notifications On?", l_notifications_enabled   )
                         printf( "%7s %41s %-24s %-24s %-24s %-20s %-s\n" , " ", " ", l_last_update , l_last_notification , l_next_notification , "Notification Period"  , notification_period  )
                         printf "\n"
            
                         printf( "%7s %41s %-16s %4.4f  %-18s %6d %47s %s\n" , " ", "Check",  "Execution Time", check_execution_time, "Current Attempt", current_attempt, "Flap Detection Enabled?", l_flap_detection_enabled  )
                         printf( "%7s %41s %-16s %4.4f  %-18s %6d %47s %s\n" , " ", " ", "Latency " , check_latency , "Max Attempts" , max_attempts, "Flapping?", l_is_flapping )
                         printf( "%7s %41s %-16s %4.4f  %-18s %4.4f\n", " ", " ", "Interval " , check_interval , "Retry Interval" , retry_interval )
                         printf "\n"

                 end  # end-details

              end  # end-printflag-2

             end  # end-hostflag-1

        end  # end-if-printflag-1

    end  # end-while

end

################################################################################

     f = File.open( "/var/log/nagios/status.dat" )

     host_counter          = 0
     l_time                = "" 
     n_time                = "" 
     last_host             = "" 
     p_host_name           = ""
     p_current_state       = "" 
     p_has_been_checked    = ""
     p_service_description = ""
     p_plugin_output       = ""
     p_last_check          = ""
     p_next_check          = ""

     i_hostname            = "ALL"
     details               = 'N'

     idx = 0
     nidx = 1
     for arg in ARGV
    	if( ARGV[idx] == '--host' and ARGV[nidx] )
            i_hostname = ARGV[nidx]
        end
    	if( ARGV[idx] == '--details'  )
            details = 'Y'
        end
        idx += 1
        nidx += 1
     end

     while line = f.gets do

        if ( i_hostname === 'ALL' )
	    if ( line.match /servicestatus/ )
                printflag = 1
	    end

	    if ( line.match /\}/ )
		printflag = 0
	    end
        else
            if line.match /host_name/
               words  = line.split( '=' )
               host_name =  words[1].chomp
               if host_name === i_hostname 
                  printflag = 1
               end
            end

	    if ( line.match /\}/ )
		printflag = 0
	    end
        end

        if( printflag == 1 )

          words  = line.split( '=' )

                     if ( line.match /host_name/ ) 
                          host_name = words[1]
                          p_host_name = host_name.chomp

          
                        if ( p_host_name != last_host )
                           host_counter += 1
                           last_host = p_host_name
          		 prt_host_header( host_counter, p_host_name )
                           prt_host_status( p_host_name, details )
                           prt_service_header( p_host_name )
                        else
                           p_host_name = " "
                        end
                     end
          
                     if( line.match /current_state/ )
                        p_current_state = "" 
                        current_state = words[1]
                        c_current_state = current_state.chomp
                        if c_current_state == "0"
                             p_current_state = "OK" 
                        end
                        if c_current_state == "1" 
                             p_current_state = "WARNING" 
                        end
                        if c_current_state == "2" 
                             p_current_state = "CRITICAL" 
                        end
                        if c_current_state == "3" 
                             p_current_state = "UNKNOWN" 
                        end
                     end
             
                     if( line.match /has_been_checked/ )
                        has_been_checked = words[1]
                        p_has_been_checked = has_been_checked.chomp
                     end
              
                     if( line.match /service_description/ ) 
                        service_description = words[1]
                        p_service_description = service_description.chomp
                     end
              
                     if( line.match /plugin_output/ ) 
          		if ! line.match 'long_plugin_output'
                              plugin_output   = line
                              p_plugin_output = plugin_output.chomp
          		    p_plug = p_plugin_output.sub( '	plugin_output=',"" )
          		    p_plugin_output = p_plug
                          end
                     end
              
                     if( line.match /last_check/ ) 
                        last_check = Integer( words[1] )
                        if( last_check > 0 )
                            p_nc = Time.at(last_check)
                            p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                            p_last_check = p_dt
                        else
                           p_last_check  = ""
                        end
                     end
          
                     if( line.match /next_check/ ) 
                        next_check = Integer( words[1] )
                        if( next_check > 0 )
                            p_nc = Time.at(next_check)
                            p_dt = p_nc.strftime("%Y-%m-%d %H:%M:%S")
                            p_next_check = p_dt
                        else
                           p_next_check  = ""
                        end
                     end
          
                     if( line.match /scheduled_downtime_depth/ ) 
          		printflag = 2
                     end
          
          	   if(  printflag == 2 ) 
                        printf( "%7s %-30s %-20s %-10s %-20s %-20s %s\n", p_has_been_checked,p_host_name,p_service_description,p_current_state,p_last_check,p_next_check,p_plugin_output  )
                     end
          
       	end  # end-printflag-1
     end   # end-while
