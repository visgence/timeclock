/*
 *job_slider.js
 *
 *script: This is script's primary functions is to find all jquery ui sliders on the page and
 *to ensure that they add up to the total amount worked for that day.
 * */
$("document").ready(function ()
{
    var d = new Date();

    //Find all job slider divs
    divs = $(".job_slider");

    //bind each one
    for (var i = 0; i < divs.length; i++) 
    {   
        var datastream_id = divs[i].id;
    }



    $("#job1").slider
    ({
        slide: function(event, ui) {  }
    });

})
