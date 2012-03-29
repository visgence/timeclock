#!usr/bin/perl
use strict;

#Use directives
use DBI;
use Data::Dumper;
use POSIX qw(strftime);

clock_in_out($ARGV[0], $ARGV[1]);

######
#
#   Clock's a user in or out.
#
#   Parameters:
#   @_[0] = the user name to clock in or out for
#   @_[1] = "In" for clocking in or "Out" for clocking out
#   
######
sub clock_in_out 
{
    my ($user_name, $status) = @_;

    my $dbh = DBI->connect("dbi:SQLite:dbname=time_clock.sqlite", "", "") or die "Couldn't connect to the database at clock_in_out(): $DBI::errstr";
    my $sth;
    my $param;

    #First check if the user can even clock in or out. Then clock them "In" or "Out"
    if(user_exists($user_name, $dbh)) 
    {
        if(my $id = can_clock($user_name, $status, $dbh))
        {
            if($status eq "In")
            {
                $sth = $dbh->prepare("INSERT INTO time_clock (time_in, user_name)
                                      VALUES (strftime(\"%Y %m %d %H %M\", datetime('now', 'localtime')), ?)") or die "Couldn't prepare statment in clock_in_out(): $DBI::errstr";
                $param = $user_name;
            }
            elsif($status eq "Out")
            {
                $sth = $dbh->prepare("UPDATE time_clock
                                      SET time_out=strftime(\"%Y %m %d %H %M\", datetime('now', 'localtime'))
                                      WHERE id = ?") or die "Couldn't prepare statment in clock_in_out(): $DBI::errstr";
                $param = $id;
            }

            $sth->execute($param) or die "Couldn't execute statement in clock_in_out(): $DBI::errstr";
        }
    }
}

######
#
#   See if a given user is able to clock in or out without it being in error.
#
#   Parameters:
#   @_[0] = the user name to check for
#   @_[1] = "In" or "Out" denoting clocking in or out
#   @_[2] = handler for the database that contains the information we need to check
#
#   Returns:
#   A the id of the user if the given user can clock in/out and 0 otherwise
#
######
sub can_clock 
{
    my ($user_name, $status, $dbh) = @_;

    my $sth = $dbh->prepare("SELECT max(id) AS id, time_in, time_out 
                             FROM time_clock
                             WHERE user_name = ?") or die "Could not prepare statement in can_clock(): $DBI::errstr";

    $sth->execute($user_name) or die "Could not execute statement in can_clock(): $DBI::errstr";
    my $result = $sth->fetchrow_hashref();

    #Base case of when the user has never once clocked in yet.
    return 1 if($result->{id} eq undef && $status eq "In");
    
    #Make sure we can "clock in" or "clock out" without error.
    if($status eq "In" && $result->{time_out} ne undef)
    {
        return $result->{id};
    }
    elsif($status eq "Out" && $result->{time_in} ne undef && $result->{time_out} eq undef)
    {
        return $result->{id};
    }

    print "Failed to clock $user_name $status\n"; #DEBUG

    return 0;
}

######
#
#   Checks to see if a given user name for an employee exists or not.
#
#   Parameters:
#   @_[0] = the user name to check for
#   @_[1] = handler for the database that contains the information we need to check
#
#   Returns:
#   A 1 if the user name currently exists and is valid and 0 otherwise
#
######
sub user_exists
{
    my ($user_name, $dbh) = @_;

    my $sth = $dbh->prepare("SELECT user_name 
                             FROM employees
                             WHERE user_name = ?") or die "Could not prepare statement in user_exists(): $DBI::errstr";

    $sth->execute($user_name) or die "Could not execute statement in user_exists(): $DBI::errstr";
    my $result = $sth->fetchrow_hashref();

    return 1 if($result->{user_name} eq $user_name);

    print "User does not exists yet.  Please add $user_name first before clocking\n"; #DEBUG
    return 0;
}
