#!/usr/bin/perl
use strict;
use DateTime;
use Data::Dumper;
use Math::Round;
use XML::Simple;

use constant {
    MONTH => 0,
    DAY => 1,
    YEAR => 2,
};

use constant {
    DATETIME => 0,
    EMAIL => 1,
    INOUT => 2,
};


my $names;
my $temp;
my $hourlyRate = 12.00;
my @rangeData;

#Grab file name and the time ranges we need to check
my $fileName = $ARGV[0];
my $begin = $ARGV[1];
my $end = $ARGV[2];

#Break up the beginning and ending range dates
my @beginRange = splitData($begin, '-');
my @endRange = splitData($end, '-');
my $beginDate = DateTime->new(year => int($beginRange[YEAR]), month => int($beginRange[MONTH]), day => int($beginRange[DAY]));
my $endDate = DateTime->new(year => int($endRange[YEAR]), month => int($endRange[MONTH]), day => int($endRange[DAY]));

open(FILE, $fileName) or die "Couldn't open $fileName for parsing: $!";

#Throw away first line since it contains nothing usefull but headers
my $line = <FILE>;
chomp($line);
parseData($line);


#parses the spreadsheet with all the time clock info and sticks the total times inside $names
sub parseData {

    my $line = shift;

    while($line = <FILE>) {

        chomp($line);
    
        my $info = getData($line);

        if(($info->{"currentDate"} == $beginDate || $info->{"currentDate"} > $beginDate) && ($info->{"currentDate"} == $endDate || $info->{"currentDate"}  < $endDate)) {
            if (!exists $names->{$info->{"name"}}) {
                $names->{$info->{"name"}} = {};
                $temp->{$info->{"name"}} = {}; 
            }
            if($info->{"inOut"} eq "In" && $temp->{$info->{"name"}}->{$info->{"currentDate"}} eq undef) {
                $temp->{$info->{"name"}}->{$info->{"currentDate"}} =  $info->{"time"};
            }
            elsif($info->{"inOut"} eq "Out" && !($temp->{$info->{"name"}}->{$info->{"currentDate"}} eq undef)) {
                my $inTime = $temp->{$info->{"name"}}->{$info->{"currentDate"}};
                my $outTime = $info->{"time"};
                my $totalTime = getInOutTime($inTime, $outTime);
            
                if(!$names->{$info->{"name"}}->{$info->{"currentDate"}} eq undef) { 
                    $totalTime = addTimes($names->{$info->{"name"}}->{$info->{"currentDate"}}, $totalTime); 
                    $names->{$info->{"name"}}->{$info->{"currentDate"}} = $totalTime;
                }
                else {
                    $names->{$info->{"name"}}->{$info->{"currentDate"}} = $totalTime;
                }
                $temp->{$info->{"name"}}->{$info->{"currentDate"}} = undef;
            
            }
        }
    }
    
    
    
    foreach my $line (sort keys %$names) {
        my $totalTime = 0.0;
        print "$line: \n";
        foreach my $date (sort keys %{$names->{$line}}) {
            my $hour = $names->{$line}->{$date};
            $totalTime = addTimes($totalTime, $hour);
            $date =~ s/T00:00:00//;
            print "     $date: " . $hour . "\n";
        }
        print "     Total Hour: $totalTime = \$" . $totalTime * $hourlyRate . "\n";
    }

    
}

#Adds two times in the form of hour.minute together and returns the new time.
sub addTimes {
    
    my @first = split('\.', shift);
    my @second = split('\.', shift);
    my $hour = $first[0] + $second[0];
    my $minute = $first[1] + $second[1];
    my @total = ($hour, $minute);
    
    if($total[1] >= 60) {
        $total[0] += 1;
        $total[1] -= 60;
    }

    return my $newTime = $total[0] . "." . $total[1];
} 

#Takes an in and an out time and calculates the difference in the form "hours.minutes" rounded to the nearest 15 minutes
sub getInOutTime {
    my $inTime = shift;
    my $outTime = shift;
    my $totalHour = $outTime->{Hour} - $inTime->{Hour};
    my $totalMin;

    if($outTime->{Minute} >= $inTime->{Minute}) {
        $totalMin = $outTime->{Minute} - $inTime->{Minute};
    }
    else {
        $totalHour -= 1;
        $totalMin = 60 - ($inTime->{Minute} - $outTime->{Minute});
    }

    $totalMin = nearest(15, $totalMin);

    if($totalMin >= 60) {
        $totalHour += 1;
        $totalMin = 0;
    }

    return $totalHour . "." . $totalMin;
}

#Returns an array with date information split from a date parameter.  Second parameter specifies what to split around
sub splitData{
    my $date = shift;
    my $splitDelimeter = shift;
    my @datePieces = split($splitDelimeter, $date);
    return @datePieces;
}

#Get's and splits up all the date, time, and email pieces.
sub getData {  
    my @data = split(',',shift);

    #Get the date and time data
    my @dateTime = split('\s', $data[DATETIME]);
    my @timeData = splitData($dateTime[1], ':');
    my @date = splitData($dateTime[0], '/');
    my $time = {'Hour' => $timeData[0], 'Minute' => $timeData[1], 'Second' => $timeData[2]};
    my $currentDate = DateTime->new(year => int($date[YEAR]), month => int($date[MONTH]), day => int($date[DAY]));

    #Get the names and in out status
    my $name = $data[EMAIL];
    $name =~ s/\@visgence\.com//;
    my $inOut = $data[INOUT]; 

    my $info = {
        time => $time,
        currentDate => $currentDate,
        name => $name,
        inOut => $inOut,
    };

    return $info;
}
