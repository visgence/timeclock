/** Gets the html for managing a users streams and puts it in the content of the page */
function load_model_grid(app, model)
{
    var url = "/utilities/model_editor/"+app+"/"+model+"/";
    $.get(url, {}, function(data) {
        $('#content').html(data);
        var back_link = $("<a></a>", {
            "href": "",
            "text": "Go Back"
        });

        $('#content').prepend(back_link);
    });
}






