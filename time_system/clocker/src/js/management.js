/** Gets the html for managing a users streams and puts it in the content of the page */
function load_model_grid (app, model) { //eslint-disable-line
    const url = '/chucho/model_editor/' + app + '/' + model + '/';
    $.get(url, {}, (data) => {
        $('#content').html(data);
        const back_link = $('<a></a>', {
            href: '',
            text: 'Go Back',
        });
        const title = $('<h2></h2>', {
            html: 'Manage ' + model + 's',
        });
        $('#content').prepend(title).prepend(back_link);
    });
}
