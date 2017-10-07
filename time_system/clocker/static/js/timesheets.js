$(() => {
    'use strict';

    const url = '/timeclock/timesheets/';
    const Timesheet = $.fn.Timesheet;
    const MessageCenter = $.fn.MessageCenter;

    const Timesheets = function (consts) {
        this.timesheetList = ko.observableArray();

        this.messageCenter = ko.observable();

        const init = function (consts) {
            consts = consts || {};

            if (consts.hasOwnProperty('messageCenter')) {
                this.messageCenter(consts.messageCenter);
            } else {
                this.messageCenter(new MessageCenter());
            }
        }.bind(this);
        init(consts);
    };

    const failcallback = function (resp) {
        this.messageCenter().setErrors(resp);
    };

    Timesheets.prototype.rebuild = function (consts) {
        consts = consts || {};
        if (consts.hasOwnProperty('timesheetList')) {
            const tmp_tsList = [];
            const pageNum = parseInt(location.search.split('=')[1]);
            for (let i = pageNum * 10 - 10; i < consts.timesheetList.length; i++) {
                if (i > pageNum * 10) {
                    break;
                }
                tmp_tsList.push(new Timesheet(consts.timesheetList[i]));
            }
            const count = Math.round((consts.timesheetList.length / 10) + 0.5);
            window.history.pushState('timesheets', 'timesheets', location.search.split('&')[0] + '&of=' + count);

            this.timesheetList(tmp_tsList);
        }
    };

    Timesheets.prototype.refresh = function () {
        const __this = this;
        return $.getJSON(url).then(__this.rebuild.bind(__this), failcallback);
    };

    Timesheets.prototype.createTimesheets = function (data) {
        if (!$.isArray(data)) {
            return;
        }

        return $.ajax({
            url: url,
            dataType: 'json',
            type: 'POST',
            beforeSend: function (xhr) {
                const csrf = $('input[name="csrfmiddlewaretoken"]').val();
                xhr.setRequestHeader('X-CSRFToken', csrf);
            },
            data: JSON.stringify(data),
        });
    };

    $.fn.Timesheets = Timesheets;


});
