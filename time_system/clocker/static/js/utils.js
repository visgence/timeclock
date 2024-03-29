$(() => {
    initPassDialog();

    $(document).ajaxComplete((event, xhr, settings) => {
        if (xhr.responseText && xhr.responseText.trim() !== '') {
            try {
                jsonData = JSON.parse(xhr.responseText);
                if (jsonData.hasOwnProperty('status') && jsonData['status'] === 302) {
                    window.location = jsonData['location'];
                }
            } catch (e) {
                console.log(e);
            }
        }
    });

    $('#sys-modal').modal({
        show: false,
    })
        .on('hidden.bs.modal', () => {
            const classes = 'has-error has-success has-warning';
            $('#sys-modal .modal-title').html('');
            $('#sys-modal .modal-body').removeClass(classes).children('span').html('');
        });
});

function initPassDialog() {
    $('#change-pass-modal').modal({
        show: false,
        backdrop: 'static',
    })
        .on('hidden.bs.modal show.bs.modal', () => {
            resetPassForm();
        });

    $('#change-pass-link').on('click', () => {
        $('#change-pass-modal').modal('show');

        // Return false since it's a link we're clicking on
        return false;
    });

    $('#change-pass-btn').on('click', () => {
        changePassword();
    });
}

function passError(error) {
    $('#pass-msg').addClass('alert alert-danger').html(error);
}

function resetPassError() {
    $('#pass-msg').removeClass('alert alert-danger').html('');
}

function resetPassForm() {
    resetPassError();
    $('#change-pass-modal form').get(0).reset();
}

/** This method will pop up a dialog that will allow the user to change their password.
 *
 */
function changePassword() {
    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
    const jsonData = {
        oldPassword: $('#oldPassword').val(),
        newPassword: $('#passwordInput').val(),
    };

    if (jsonData.oldPassword.trim() === '') {
        passError('Please enter your old password');
        return;
    }
    if (jsonData.newPassword.trim() === '') {
        passError('Please enter your new password');
        return;
    }
    if (jsonData.newPassword !== $('#passwordReinput').val().trim()) {
        passError('Your new passwords do not match.');
        return;
    }

    // const self = this;
    const postData = {
        csrfmiddlewaretoken: csrf,
        jsonData: JSON.stringify(jsonData),
    };

    $.post('/changePassword/', postData, (resp) => {
        if (resp.accessError) {
            window.location = '/';
        } else if (resp.errors) {
            passError(resp.errors);
        } else if (resp.success) {
            $('#change-pass-modal').modal('hide');
            sysDialog(resp.success, 'Success!', 'success');
        } else {
            passError('An unknown error has occured');
        }
    });
}

function sysDialog(msg, title, type) {
    const types = {
        error: 'has-error',
        success: 'has-success',
        warning: 'has-warning',
    };

    if (types.hasOwnProperty(type)) {
        $('#sys-modal div.modal-body').addClass(types[type]);
    }
    $('#sys-modal div.modal-body').children('span').html(msg);
    $('#sys-modal .modal-title').html(title);
    $('#sys-modal').modal('show');
}


function localeDateFormat() {
    let str = '';
    str += this.getFullYear() + '/';
    str += (this.getMonth() + 1 < 10 ? '0' + (this.getMonth() + 1) : this.getMonth() + 1) + '/';
    str += this.getDate() < 10 ? '0' + this.getDate() : this.getDate();
    str += ' ';

    return str;
}

Date.prototype.localeDateFormat = localeDateFormat;

function getHash() { // eslint-disable-line
    const hash = location.hash.substring(1).split('&');
    const obj = {};
    hash.forEach((item) => {
        if (item === '') {
            return;
        }
        key = item.split('=')[0];
        value = item.split('=')[1];
        obj[key] = value;
    });
    return obj;
}

function updateHash(newHash) { // eslint-disable-line
    let str = '#';
    Object.keys(newHash).forEach((key) => {
        str += key + '=' + newHash[key] + '&';
    });
    // remove trailing &
    str = str.substring(0, str.length - 1);
    location.hash = str;
}
