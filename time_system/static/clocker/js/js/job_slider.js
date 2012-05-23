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
        slide: function(event, ui) {  }
    });

}//end create_slider_handler 



$("document").ready(function ()
{

    //Find all job slider divs
    job_ids = $(".job_slider");

    //create a handler for each slider
    for (var i = 0; i < job_ids.length; i++) 
    {   
        create_slider_handler(job_ids[i].id)
    }

})
