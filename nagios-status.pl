#!/usr/bin/perl
################################################################################
#
#	Program:	nagios.status.pl
#
#	Author:		Copyright (c) 2012 Tim Schaefer, 
#			tim@asystemarchitect.com All Rights Reserved.
#
#	Latest:		2012-01
#
#			THIS IS A WORK IN PROGRESS
#
#	Description:	Displays the same information as the Nagios web interface
#			does for service detail.  This is the most common view
#			used to check the status of services.
#
#	Limits: 	Hostgroup and servicegroup information is not in the
#			status.dat, therefore you cannot do hostgroup or 
#			servicegroup reporting.
#
#	Usage:	
#
# 	./nagios_status.pl data=status.dat [host=host] [service=service] [state=state]
#
#	where
#
#	data=status.dat	The full path to the nagios status.dat file, typically
#			found under the Nagios installation.  Check your nagios.cfg
#			for the location of the status.dat file.
#
#	host=host	Either a FQHN or partial hostname will match wildcard
#
#	service=service Either a service-name or partial will match wildcard
#
#	state=state	OK,WARNING,CRITICAL,UNKNOWN
#
#	License:	This program is shareware. I own it but I'm sharing.
#
################################################################################

	$ENV{TZ} = 'PST8DST' ;

	use POSIX ;
	use CGI   ;

	my $cgi = new CGI ;

	my %data_hash ;
	my %server_hash ;

	my $data      = $cgi->param( "data" ) ;
	   $data      = ($data)?"$data" : '/var/log/nagios/status.dat' ;

	my $host      = $cgi->param( "host" ) ;
	   $host      = ($host)?"$host" : 'NULL' ;

	my $service   = $cgi->param( "service" ) ;
	   $service   = ($service)?"$service" : 'NULL' ;

	my $state     = $cgi->param( "state" ) ;
	   $state     = ($state)?"$state" : 'NULL' ;

	my $system    = $cgi->param( "system" ) ;
	   $system    = ($system)?"$system" : 'NULL' ;

	my $use_hdr   = $cgi->param( "use_hdr" ) ;
	   $use_hdr   = ($use_hdr)?"$use_hdr" : 'Y' ;

	my $usage     = $cgi->param( "usage" ) ;
	   $usage     = ($usage)?"$usage" : 'N' ;

	my $last_host = ""  ;

	my $epoch     = time ;
	my $timestamp = cnvt_epoch_to_timestring ( $epoch ) ;

	my $t_last_check ;
	my $t_next_check ;

	my $str_len ;
	my $tline   ;
	my $bline   ;
	my $header  ;

	my $state_count = 0 ;
	my $host_count = 0 ;

	my $host_name = "" ; my $service_description = "" ; my $modified_attributes = "" ; my $check_command = "" ;
	my $check_period = "" ; my $notification_period = "" ; my $check_interval = "" ; my $retry_interval = "" ;
	my $event_handler = "" ; my $has_been_checked = "" ; my $should_be_scheduled = "" ; my $check_execution_time = "" ;
	my $check_latency = "" ; my $check_type = "" ; my $current_state = "" ; my $last_hard_state = "" ;
	my $last_event_id = "" ; my $current_event_id = "" ; my $current_problem_id = "" ; my $last_problem_id = "" ;
	my $current_attempt = "" ; my $max_attempts = "" ; my $state_type = "" ; my $last_state_change = "" ;
	my $last_hard_state_change = "" ; my $last_time_ok = "" ; my $last_time_warning = "" ; my $last_time_unknown = "" ;
	my $last_time_critical = "" ; my $plugin_output = "" ; my $long_plugin_output = "" ; my $performance_data = "" ;
	my $last_check = "" ; my $next_check = "" ; my $check_options = "" ; my $current_notification_number = "" ;
	my $current_notification_id = "" ; my $last_notification = "" ; my $next_notification = "" ; my $no_more_notifications = "" ;
	my $notifications_enabled = "" ; my $active_checks_enabled = "" ; my $passive_checks_enabled = "" ; my $event_handler_enabled = "" ;
	my $problem_has_been_acknowledged = "" ; my $acknowledgement_type = "" ; my $flap_detection_enabled = "" ; my $failure_prediction_enabled = "" ;
	my $process_performance_data = "" ; my $obsess_over_service = "" ; my $last_update = "" ; my $is_flapping = "" ;
	my $percent_state_change = "" ; my $scheduled_downtime_depth = "" ; my $STATE = "" ; my $last_version = 'NULL' ; my $version = 'NULL' ;

	my @fields = "" ;

	## print STDERR "stdin => state [$state]" ;

	if( $ARGV[0] eq '--help' )
		{
		print_usage();
		exit;
		}

	$hc = 0 ;
	set_header();
	# print_header();

        # if( $service ne 'NULL' ) { print_header(); }

	if( $data ne 'NULL' )
		{
		load_data() ;
		# print_hash();
		filter_report();
		## $host_count = count_hosts();
		## if( $host_count == 1 ) { print_header(); }
		print_report();
		}
	else	{
		print_usage();
		}

################################################################################

sub print_usage {

print <<ENDOFUSAGE;

nagios_status - Copyright 2012 (c) Tim Schaefer All Rights Reserved 

Usage:	

	./nagios_status.pl data=status.dat [host=host] [service=service] [state=state]

	where

	data=status.dat	The full path to the nagios status.dat file, typically
			found under the Nagios installation.  Check your nagios.cfg
			for the location of the status.dat file.

	host=host	Either a FQHN or partial hostname will match wildcard

	service=service Either a service-name or partial will match wildcard

	state=state	OK,WARNING,CRITICAL,UNKNOWN

Usage Examples:

	nagios.status.pl data=status.dat

	nagios.status.pl data=status.dat service=service

	nagios.status.pl data=status.dat state=state

	nagios.status.pl data=status.dat host=host

	nagios.status.pl use_hdr=N 

ENDOFUSAGE

}

################################################################################

sub load_data {

	open( DATA, "<$data" ) or die "Can't open $data file\n"  ;

	$idx = 0 ;
	while (<DATA>) 
		{
		chomp $_  ;	

		if ( $_ =~ /host_name=/ && $svc == 1 )
			{
			$combo_str = $_ ;
			@combo_arr = split( "=", $_ ) ;
			$hostname  = $combo_arr[1] ;
			++$host_count ;
			}

		if ( /^service/ )
			{
			$svc       = 1 ;
			$hash_idx  = sprintf( "%4.4d", $idx ) ;
			$combo_key = $hostname . "_" . $hash_idx ;

			if( $host eq 'NULL' && $service eq 'NULL' )
				{
				if( $state eq 'NULL' )
					{
					$STATE       = "ALL" ;
					$state_count = 0 ;
					$data_hash{$combo_key} = "HOST=ALL, SERVICE=ALL, STATE=ALL, " . $line ;
					}
				else
					{
					$STATE       = $state ;
					++$state_count ;
					$data_hash{$combo_key} = "HOST=ALL, SERVICE=ALL, STATE=$state, " . $line ;
					}
				}

			if( $host ne 'NULL' && $service eq 'NULL' )
				{
				if( $state eq 'NULL' )
					{
					$STATE       = "ALL" ;
					$state_count = 0 ;
					$data_hash{$combo_key} = "HOST=$host, SERVICE=ALL, STATE=ALL, " . $line ;
					}
				else
					{
					$STATE       = $state ;
					++$state_count ;
					$data_hash{$combo_key} = "HOST=$host, SERVICE=ALL, STATE=$state, " . $line ;
					}
				}

			if( $host eq 'NULL' && $service ne 'NULL' )
				{
				if( $state eq 'NULL' )
					{
					$STATE       = "ALL" ;
					$state_count = 0 ;
					$data_hash{$combo_key} = "HOST=ALL, SERVICE=$service, STATE=ALL, " . $line ;
					}
				else
					{
					$STATE       = $state ;
					++$state_count ;
					$data_hash{$combo_key} = "HOST=ALL, SERVICE=$service, STATE=$state, " . $line ;
					}
				}

			if( $host ne 'NULL' && $service ne 'NULL' )
				{
				if( $state eq 'NULL' )
					{
					$STATE       = "ALL" ;
					$state_count = 0 ;
					$data_hash{$combo_key} = "HOST=$host, SERVICE=$service, STATE=ALL, " . $line ;
					}
				else
					{
					$STATE       = $state ;
					++$state_count ;
					$data_hash{$combo_key} = "HOST=$host, SERVICE=$service, STATE=$state, " . $line ;
					}
				}


			##
			## print STDERR "\n\nLOAD HASH => $data_hash{$combo_key} \n\n" ;
			##

			$line                  = "" ;
			++$idx ;
			}
		else	{
			$svc = 0 ;
			if( $_ !~ '}' )
				{
				$_ =~ s/^\s+// ;
				$line .= $_    ;
				$line .= ", "  ;
				}
			}
		}
}
1;

################################################################################

sub count_hosts {

	$count = 0 ;
	foreach $k ( sort keys %data_hash )
        	{
        	@fields = split( ',', $data_hash{$k} ) ;
		$cols = scalar @fields ;
		$c_host_name = $fields[3] ;
		if( $last_host_name ne $c_host_name && $c_host_name !~ /#####/ )
			{
			++$count ;
			}
		$last_host_name = $c_host_name ;
		}

	return $count ;
}

################################################################################

sub print_report {

	$rowid       = 0 ;
	$headcounter = 0 ;
	$last_p_host_name = "X" ;

	foreach $k ( sort keys %data_hash )
        	{
		init_fields();

        	@fields = split( ',', $data_hash{$k} ) ;

		parse_fields();

		if( $current_state == 0 ) { $p_current_state = "OK" ; }
		if( $current_state == 1 ) { $p_current_state = "WARNING" ; }
		if( $current_state == 2 ) { $p_current_state = "CRITICAL" ; }
		if( $current_state == 3 ) { $p_current_state = "UNKNOWN" ; }

		$t_last_check = cnvt_epoch_to_timestring( $last_check ) ;
		if( $t_last_check eq '1969-12-31 16:00:00' ) { $t_last_check = "Not Checked" ; }

		$t_next_check = cnvt_epoch_to_timestring( $next_check ) ;
		$now          = time ;

		if( $next_check >= $now ) { $p_next_check = $t_next_check ; } else { $p_next_check = "" ; }

		$attempts = $current_attempt . "/" . $max_attempts ;

		################################################################################	

                $p_ack = sprintf( "%s", $problem_has_been_acknowledged ) ;

                if(  $p_ack != 0 ) { $ack = "A"; } else { $ack = " "; }

		################################################################################	

		if( $HOST eq 'ALL' && $SERVICE eq 'ALL' )
			{
			if( $last_host ne $host_name )
				{
				$svc_cnt     = 0 ;
				$p_host_name = $host_name ;
				if( length( $host_name ) > 0 )
					{
					if( $rowid > 0 )
						{
						print_header();
						}
					}
				++$hc;
				}
			else	{
				++$svc_cnt ;
				}

			if( $service_description  )
				{
				if( $svc_cnt > 0 )
					{
					$p_host_name = ""  ;
					}
				print_row();
				}
			}

		################################################################################	

		if( $HOST ne 'ALL' && $SERVICE eq 'ALL' )
			{
			if( $last_host ne $host_name )
				{
				$svc_cnt = 0 ;
				$p_host_name = $host_name ;
				if( length( $host_name ) > 0 )
					{
					if( $rowid > 0 )
						{
						print_header();
						}
					}
				++$hc;
				}
			else	{
				++$svc_cnt ;
				}

			if( $service_description  && $host_name =~ $HOST )
				{
				if( $svc_cnt > 0 )
					{
					$p_host_name = ""  ;
					}
				print_row();
				}
			}

		################################################################################	

		if( $HOST eq 'ALL' && $SERVICE ne 'ALL' )
			{
			if( $last_host ne $host_name )
				{
				$svc_cnt     = 0 ;
				$p_host_name = $host_name ;
				if( length( $host_name ) > 0 )
					{
					if( $rowid > 0 )
						{
						print_header();
						}
					}
				++$hc;
				}
			else	{
				++$svc_cnt ;
				}

			if( $service_description  && $service_description =~ $SERVICE )
				{
				if( $svc_cnt > 0 )
					{
					$p_host_name = ""  ;
					}
				print_row();
				}
			}

		################################################################################	

		if( $HOST ne 'ALL' && $SERVICE ne 'ALL' )
			{

			$p_host_name = $host_name ;

			if( $service_description  && $service_description =~ $SERVICE )
				{
				print_row();
				}
			}


		################################################################################	

		$last_host        = $host_name ;
		$last_hostgroup   = $hostgroup ;
		$last_p_host_name = $p_host_name ;
		++$rowid ;
		}

}
1;

################################################################################

sub print_row {

	printf( "%s %42s %-35s %8s %-20s %-20s %8s %s\n", $ack, $p_host_name, $service_description, $p_current_state, $t_last_check, $p_next_check, $attempts,  $plugin_output ) ;

}

################################################################################

sub cnvt_epoch_to_timestring {

	my $epoch          = $_[0] ;
	my $formatted_time = strftime("%Y-%m-%d %H:%M:%S", localtime($epoch) ) ;

	return $formatted_time ;
}

################################################################################

sub set_header {

	if( $use_hdr eq 'Y' )
		{
		$header  = sprintf( "%s %-42s %-35s %8s %-20s %-20s %8s %s", " ", "Host", "Service Description", "Status", "Last Check", "Next Check", "Attempts", "Output" ) ;
		$str_len = length( $header ) ;
		$str_len += 120 ;

		my $i    = 0 ;
		for( $i = 0 ; $i < $str_len ; ++$i ) { $tline .= sprintf( "%s", '_' ) ; }

		my $i    = 0 ;
		for( $i = 0 ; $i < $str_len ; ++$i ) { $bline .= sprintf( "%s", '-' ) ; }

		}
	else	{
		$header = "" ;
		$tline  = "" ;
		$bline  = "" ;
		}
}

################################################################################

sub print_header {

	if( $use_hdr eq 'Y' )
		{
		print "$tline\n" ;
		print "$header\n" ;
		print "$bline\n" ;
		}
}
1;

################################################################################

sub print_hash {

	foreach $k ( sort keys %data_hash )
        	{
		print STDERR "\nPRINT HASH => $data_hash{$k}\n" ;
		}
}

################################################################################

sub filter_report {

	$rowid       = 0 ;
	$headcounter = 0 ;
	$last_p_host_name = "X" ;

	foreach $k ( sort keys %data_hash )
        	{

		init_fields();

        	@fields = split( ',', $data_hash{$k} ) ;

		parse_fields();

		if( $current_state == 0 ) { $p_current_state = "OK" ; }
		if( $current_state == 1 ) { $p_current_state = "WARNING" ; }
		if( $current_state == 2 ) { $p_current_state = "CRITICAL" ; }
		if( $current_state == 3 ) { $p_current_state = "UNKNOWN" ; }

		if( $STATE ne 'ALL' )
			{
			if ( $p_current_state ne $STATE )
				{
				$data_hash{$k} = "" ;
				--$state_count ;
				}
			}

		if( $service ne 'NULL' )
			{
			if ( $service_description ne $service )
				{
				$data_hash{$k} = "" ;
				}
			}

		if( $host ne 'NULL' )
			{
			if ( $host_name ne $host )
				{
				$data_hash{$k} = "" ;
				}
			}

		if( $version ne 'NULL' )
			{
			$data_hash{$k} = "" ;
			}

		++$idx ;
		}

}

################################################################################

sub parse_fields {

		init_fields();

		foreach $l ( sort( @fields ) )
			{
			@t   = split( "=", $l ) ;
			$var = $t[0] ;
			$val = $t[1] ;
			$var =~ s/\s+//g ; 

			if( $var )
				{

				if ($var =~ /HOST/)    { $HOST    = $val ; } 
				if ($var =~ /SERVICE/) { $SERVICE = $val ; } 
				if ($var =~ /STATE/)   { $STATE = $val ; } 

				if ($var =~ /host_name/) { $host_name = $val ; } 
				if ($var =~ /service_description/) { $service_description = $val ; } 
				if ($var =~ /modified_attributes/) { $modified_attributes = $val ; } 
				if ($var =~ /check_command/) { $check_command = $val ; } 
				if ($var =~ /check_period/) { $check_period = $val ; } 
				if ($var =~ /notification_period/) { $notification_period = $val ; } 
				if ($var =~ /check_interval/) { $check_interval = $val ; } 
				if ($var =~ /retry_interval/) { $retry_interval = $val ; } 
				if ($var =~ /event_handler/) { $event_handler = $val ; } 
				if ($var =~ /has_been_checked/) { $has_been_checked = $val ; } 
				if ($var =~ /should_be_scheduled/) { $should_be_scheduled = $val ; } 
				if ($var =~ /check_execution_time/) { $check_execution_time = $val ; } 
				if ($var =~ /check_latency/) { $check_latency = $val ; } 
				if ($var =~ /check_type/) { $check_type = $val ; } 
				if ($var =~ /current_state/) { $current_state = $val ;  } 
				if ($var =~ /last_hard_state/) { $last_hard_state = $val ; } 
				if ($var =~ /last_event_id/) { $last_event_id = $val ; } 
				if ($var =~ /current_event_id/) { $current_event_id = $val ; } 
				if ($var =~ /current_problem_id/) { $current_problem_id = $val ; } 
				if ($var =~ /last_problem_id/) { $last_problem_id = $val ; } 
				if ($var =~ /current_attempt/) { $current_attempt = $val ; } 
				if ($var =~ /max_attempts/) { $max_attempts = $val ; } 
				if ($var =~ /state_type/) { $state_type = $val ; } 
				if ($var =~ /last_state_change/) { $last_state_change = $val ; } 
				if ($var =~ /last_hard_state_change/) { $last_hard_state_change = $val ; } 
				if ($var =~ /last_time_ok/) { $last_time_ok = $val ; } 
				if ($var =~ /last_time_warning/) { $last_time_warning = $val ; } 
				if ($var =~ /last_time_unknown/) { $last_time_unknown = $val ; } 
				if ($var =~ /last_time_critical/) { $last_time_critical = $val ; } 
				if ($var =~ /plugin_output/) { $plugin_output = $val ; } 
				if ($var =~ /long_plugin_output/) { $long_plugin_output = $val ; } 
				if ($var =~ /performance_data/) { $performance_data = $val ; } 
				if ($var =~ /last_check/) { $last_check = $val ; } 
				if ($var =~ /next_check/) { $next_check = $val ; } 
				if ($var =~ /check_options/) { $check_options = $val ; } 
				if ($var =~ /current_notification_number/) { $current_notification_number = $val ; } 
				if ($var =~ /current_notification_id/) { $current_notification_id = $val ; } 
				if ($var =~ /last_notification/) { $last_notification = $val ; } 
				if ($var =~ /next_notification/) { $next_notification = $val ; } 
				if ($var =~ /no_more_notifications/) { $no_more_notifications = $val ; } 
				if ($var =~ /notifications_enabled/) { $notifications_enabled = $val ; } 
				if ($var =~ /active_checks_enabled/) { $active_checks_enabled = $val ; } 
				if ($var =~ /passive_checks_enabled/) { $passive_checks_enabled = $val ; } 
				if ($var =~ /event_handler_enabled/) { $event_handler_enabled = $val ; } 
				if ($var =~ /problem_has_been_acknowledged/) { $problem_has_been_acknowledged = $val ; } 
				if ($var =~ /acknowledgement_type/) { $acknowledgement_type = $val ; } 
				if ($var =~ /flap_detection_enabled/) { $flap_detection_enabled = $val ; } 
				if ($var =~ /failure_prediction_enabled/) { $failure_prediction_enabled = $val ; } 
				if ($var =~ /process_performance_data/) { $process_performance_data = $val ; } 
				if ($var =~ /obsess_over_service/) { $obsess_over_service = $val ; } 
				if ($var =~ /last_update/) { $last_update = $val ; } 
				if ($var =~ /is_flapping/) { $is_flapping = $val ; } 
				if ($var =~ /percent_state_change/) { $percent_state_change = $val ; } 
				if ($var =~ /scheduled_downtime_depth/) { $scheduled_downtime_depth = $val ; } 
				}
			}

}

################################################################################

sub init_fields {

	$host_name = "" ; $service_description = "" ; $modified_attributes = "" ; $check_command = "" ;
	$check_period = "" ; $notification_period = "" ; $check_interval = "" ; $retry_interval = "" ;
	$event_handler = "" ; $has_been_checked = "" ; $should_be_scheduled = "" ; $check_execution_time = "" ;
	$check_latency = "" ; $check_type = "" ; $current_state = "" ; $last_hard_state = "" ;
	$last_event_id = "" ; $current_event_id = "" ; $current_problem_id = "" ; $last_problem_id = "" ;
	$current_attempt = "" ; $max_attempts = "" ; $state_type = "" ; $last_state_change = "" ;
	$last_hard_state_change = "" ; $last_time_ok = "" ; $last_time_warning = "" ; $last_time_unknown = "" ;
	$last_time_critical = "" ; $plugin_output = "" ; $long_plugin_output = "" ; $performance_data = "" ;
	$last_check = "" ; $next_check = "" ; $check_options = "" ; $current_notification_number = "" ;
	$current_notification_id = "" ; $last_notification = "" ; $next_notification = "" ; $no_more_notifications = "" ;
	$notifications_enabled = "" ; $active_checks_enabled = "" ; $passive_checks_enabled = "" ; $event_handler_enabled = "" ;
	$problem_has_been_acknowledged = "" ; $acknowledgement_type = "" ; $flap_detection_enabled = "" ; $failure_prediction_enabled = "" ;
	$process_performance_data = "" ; $obsess_over_service = "" ; $last_update = "" ; $is_flapping = "" ;
	$percent_state_change = "" ; $scheduled_downtime_depth = "" ; 
	$STATE = "" ; $last_version = 'NULL' ; $version = 'NULL' ;
}
