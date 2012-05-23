/*
 *job_slider.js
 *
 *script: This is script's primary functions is to find all jquery ui sliders on the page and
 *to ensure that they add up to the total amount worked for that day.
 * */


function create_slider_handler(job_id, total_time)
{

    //alert(total_time);
    return $("#" + job_id).slider
    ({
        slide: function(event, ui)
        {
            var hours = Math.floor(ui.value / 60);
            var minutes = Math.floor(ui.value - (hours * 3600)/60);

            //Handle the case where minustes > 60
            if(minutes%60 == 0 && minutes != 0) 
            {
                hours =  hours + 1;
                //alert("hours: " + hours + " minutes: " + minutes);
                minutes = minutes - (hours * 60)
            }

            if(hours < 10) hours = '0' + hours;
            if(minutes < 10) minutes = '0' + minutes;

            $('#hours_' + job_id).val(hours+':'+minutes); 


            var time = time_to_sec($("#total_time").val());
            $('#debug').html('total_seconds: ' + time);
            $("#total_time").val(sec_to_time(total_time - (minutes*60) - (hours*3600)));

        },
        max:Math.floor(total_time/60)

    });

}//end create_slider_handler 



$("document").ready(function ()
{
    //Convert total time from seconds to hour:min
    total_time = $("#total_time").val();
    $("#total_time").val(sec_to_time(total_time));

    time_to_sec($("#total_time").val());//DEBUG
    //Find all job slider divs
    job_ids = $(".job_slider");

    //create a handler for each slider
    for (var i = 0; i < job_ids.length; i++) 
    {   
        create_slider_handler(job_ids[i].id, total_time);
    }

})

function sec_to_time(sec)
{
    var hours = Math.floor(sec / 3600);
    var minutes = Math.floor((sec - (hours * 3600))/60);

    if(hours < 10) hours = '0' + hours;
    if(minutes < 10) minutes = '0' + minutes;
    
    return hours + ':' + minutes;
}//end sec_to_time

//Parses a time string in the form 'hh:mm' and converts to seconds
//Returns: Integer seconds
function time_to_sec(time)
{
    //pull the hours out
    var hours = time.substr(0,2);
    
    //alert(hours);
    if(hours != '00')
    {
        //if there is a leading zero, chuck it.
        if(hours.substr(0,1) == '0')
        {
            hours = parseInt(hours.substr(1,1));
            //alert(hours);
        }
        else//both digits are significant
        {
            hours = parseInt(minutes.substr(0,2));
            //alert(hours);
        }


    }
    else{hours = 0;}

    //pull out the minutes
    var minutes= time.substr(3,2);
    if(minutes != '00')
    {
        //if there is a leading zero, chuck it.
        if(minutes.substr(0,1) == '0')
        {
            minutes = parseInt(minutes.substr(1,1));
            //alert(minutes);
        }
        else//both digits are significant
        {
            minutes = parseInt(minutes.substr(0,2));
            //alert(minutes);
        }

    }
    else{minutes = 0;}
    
    //$('#debug').html('total_seconds: ' + Math.floor((hours * 3600) + ( minutes * 60)))
    return  Math.floor((hours * 3600) + ( minutes * 60));
}//end sec_to_time
