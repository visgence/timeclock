/** Gets the html for managing a users streams and puts it in the content of the page */
function load_model_grid(app, model)
{
    console.log("foo");
    var url = "/utilities/model_editor/"+app+"/"+model+"/";
    $.get(url, {}, function(data) {
        $('#content').html(data);
        var back_link = $("<a></a>", {
            "href": "",
            "text": "Go Back"
        });
        var title = $("<h2></h2>", {
            "html": "Manage "+model+"s"
        });
        $('#content').prepend(title).prepend(back_link);
    });
}






