/*
 *job_slider.js
 *
 *script: This is script's primary functions is to find all jquery ui sliders on the page and
 *to ensure that they add up to the total amount worked for that day.
 * */



function create_slider_handler(job_id, total_time)
{
    var max_sum = Math.floor(total_time/60);

    return $("#" + job_id).slider
    ({
        max:Math.floor(total_time/60),

        slide: function(event, ui)
        {
            var sum = 0;


            $(".job_slider").not(this).each(function() 
            {
                sum += $(this).slider("value");
            });

            sum += ui.value;

            if (sum > max_sum)
            {
                event.preventDefault();
            }
            else
            {


            var hours = Math.floor(ui.value / 60);
            var minutes = Math.floor(ui.value - (hours * 3600)/60);

            //Handle the case where minustes > 60
            if(minutes%60 == 0 && minutes != 0) 
            {
                hours =  hours + 1;
                minutes = minutes - (hours * 60)
            }

            if(hours < 10) hours = '0' + hours;
            if(minutes < 10) minutes = '0' + minutes;

            $('#hours_' + job_id).val(hours+':'+minutes); 

            value = ui.value - $(this).slider("value");

            var time = time_to_sec($("#total_time").val());

                $("#total_time").val(sec_to_time(time - value*60));
            }
        }


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

        //initialize time to zero
        $('#hours_' + job_ids[i].id).val('00:00'); 
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
            hours = parseInt(hours.substr(0,2));
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
        }
        else//both digits are significant
        {
            minutes = parseInt(minutes.substr(0,2));
        }

    }
    else{minutes = 0;}
    
    return  ((hours * 3600) + ( minutes * 60));
}//end sec_to_time




function submit_form()
{

    //If the total time has not been spent, alert
    if($("#total_time").val() != "00:00")
    {
        alert("Please allocate all work time.");
        return;
    }


    //Create json object
    var json = 
    {
        "emp_id" : $("#emp_id").val(),
        "shift_id": $("#shift_id").val(),
    }

    var job_array = new Array();

    $(".job_slider").each(function() 
    {
        job_id = this.id;

        if($("#miles_" + job_id).val() != 0 || time_to_sec($("#hours_" + job_id).val()) != 0)
        {
            job_array.push
            ({
                "job_id":this.id, 
                "miles":$("#miles_" + job_id).val(),
                "notes":$("#notes_" + job_id).val(),
                "hours":time_to_sec($("#hours_" + job_id).val())
            });
        }

    });
    
    json.shift_summary = job_array;
        
    $.ajax
    ({
      type: 'POST',
      url: '/timeclock/shift_summary/',
      data:'json=' +JSON.stringify(json),
      success: function(){window.location = "/timeclock"},
      dataType: 'html'
    });

    //$('#debug').html(JSON.stringify(json));
    
}

/*The following is needed in order for django's csrf token protection to play
nice with ajax requests.
Refer to https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/#csrf-ajax
*/
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


function toggle_section(id, e) {
	console.log("foo");
    if ($(e).hasClass('ui-icon-circle-triangle-s')) {
    	$('#'+id).hide({duration:0});
        $(e).removeClass('ui-icon-circle-triangle-s');
        $(e).addClass('ui-icon-circle-triangle-e');
    }
    else if ( $(e).hasClass('ui-icon-circle-triangle-e') ) {
        $('#'+id).show({duration:0});
        $(e).removeClass('ui-icon-circle-triangle-e');
        $(e).addClass('ui-icon-circle-triangle-s');
    }
}
