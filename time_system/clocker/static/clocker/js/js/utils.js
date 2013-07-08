
/** This method will pop up a dialog that will allow the user to change their password.
  *
  */
function changePassDialog()
{
    var ok = {
        text: 'OK',
        click: function() {
            $(this).dialog('close');
        }
    };

    var buttons = [
        {
            text: 'Change Password',
            click: function() {
                // Send the change password request
                var postData = {};
                var self = this;

                postData.oldPassword = $('#oldPassword').val();
                postData.newPassword = $('#passwordInput').val();

                if ( postData.oldPassword === '' ) {
                    makeDialog('Please enter your old password', 'Error', [ok]);
                    return;
                }
                if ( postData.newPassword === '' ) {
                    makeDialog('Please enter your new password', 'Error', [ok]);
                    return;
                }
                if ( postData.newPassword !== $('#passwordReinput').val() ) {
                    makeDialog('Your new passwords do not match.  Please reenter them.', 'Error', [ok]);
                    return;
                }
                var csrf = $('input[name="csrfmiddlewaretoken"]').val();
                $.post('/changePassword/', {csrfmiddlewaretoken: csrf,
                                                      jsonData: JSON.stringify(postData)},
                       function(resp) {
                           if(resp.accessError)
                               makeDialog(resp.accessError, 'Error', [{text:'OK', click: function(){window.location = "/"}}]);
                           else if ( resp.errors )
                               makeDialog(resp.errors, 'Error', [ok]);
                           else if ( resp.success ) {
                               makeDialog(resp.success, 'Success', [ok]);
                               $(self).dialog('close');
                           }
                           else
                               makeDialog(resp, 'Unknown Error', [ok]);
                       });
            }
        },
        {
            text: 'Cancel',
            click: function() {
                $(this).dialog('close');
            }
        }
    ];
    
    $.get('/passwordForm/', {}, function(resp) {
        if(resp.accessError)
            makeDialog(resp.accessError, 'Error', [{text:'OK', click: function(){window.location = "/"}}]);
        else if ( resp.errors )
            makeDialog(resp.errors, 'Error', [{text:'OK', click: function(){$(this).dialog('close');}}]);
        else if ( resp.html )
            makeDialog(resp.html, 'Change Password', buttons);
        else
            makeDialog(resp, 'Unknown Error', [{text:'OK', click: function(){$(this).dialog('close');}}]);
    });
}


/** This method will create a dialogue and insert content from an ajax call
 *  into it.
 *
 * \param[in] msg   The message (html) to use in the dialog.
 * \param[in] title  The title on the dialog.
 * \param[in] buttons An array of js objects.  Must follow the jquery-ui dialog button specification:
 *                    E.g.  buttons = [{text: 'Ok', click: function(){ $(this).dialog('close'); } }, ...]
 */
function makeDialog(msg, title, buttons)
{
    var div = $('<div></div>');
    
    $(div).addClass('serverDialog');

    // Find all the serverDialogs, and find the one with the largest id
    var IDs = $.map($('.serverDialog'), function(e, i) {
        console.log(e);
        console.log($(e).data('id'));
        return $(e).data('id');
    });

    var data_id = 0;

    if ( IDs.length !== 0 )
        data_id = Math.max.apply(null,IDs) + 1; 

    var id = 'serverDialog' + data_id;

    $(div).data('id', data_id);
    $(div).attr('id', id);
    $(div).css('display', 'none');
    $(div).attr('title', title);
    $(div).html(msg);
    $('body').append(div);
    $('#' + id).dialog({
        autoOpen: true,
        resizable: true,
        hide: 'fade',
        show: 'fade',
        modal: true,
        minWidth: 350,
        maxWidth: 1000,
        minHeight: 300,
        maxHeight: 1000,
        dialogClass: "dialogue",
        close: function() {
            $(this).dialog('destroy');
            $('#' + id).remove();
        },
        buttons: buttons
    });
}
