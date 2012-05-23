/*
 *job_slider.js
 *
 *script: This is script's primary functions is to find all jquery ui sliders on the page and
 *to ensure that they add up to the total amount worked for that day.
 * */


function create_slider_handler(job_id)
{
    return $("#" + job_id).slider
    ({
        slide: function(event, ui)
        {
            var hours = Math.floor(ui.value / 3600);
            var minutes = Math.floor(ui.value - (hours * 3600)/60);
            //var minutes = Math.floor((ui.value - (hours * 3660))/60);

            if(hours.length == 1) hours = '0' + hours;
            if(minutes.length == 1) minutes = '0' + minutes;

            $('#hours_' + job_id).val(hours+':'+minutes); 

        },
        //max:$("#total_time").val()

    });

}//end create_slider_handler 



$("document").ready(function ()
{
    //Convert total time from seconds to hour:min
    total_time = sec_to_time($("#total_time").val());
    $("#total_time").val(total_time);

    //Find all job slider divs
    job_ids = $(".job_slider");

    //create a handler for each slider
    for (var i = 0; i < job_ids.length; i++) 
    {   
        create_slider_handler(job_ids[i].id);
    }

})

function sec_to_time(sec)
{
    var hours = Math.floor(sec / 3600);
    var minutes = Math.floor((sec - (hours * 3600))/60);

    if(hours.length == 1) hours = '0' + hours;
    if(minutes.length == 1) minutes = '0' + minutes;
    
    return hours + ':' + minutes;
}//end sec_to_time
