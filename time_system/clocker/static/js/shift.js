$(() => {
    'use strict';

    const Shift = function (consts) {
        const __this = this;
        const shiftUrl = '/timeclock/shifts/';
        const dayLabels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

        this.id = ko.observable();
        this.time_in = ko.observable();
        this.time_in_label = ko.observable();
        this.time_out_label = ko.observable();
        this.time_out = ko.observable();
        this.hours = ko.observable();
        this.employee = ko.observable();

        this.updating = ko.observable(false);
        this.shiftToEdit = ko.observable();

        this.init = function (consts) {
            consts = consts || {};

            this.rebuild(consts);
        }.bind(this);

        this.rebuild = function (consts) {
            consts = consts || {};

            if (consts.hasOwnProperty('id')) {
                this.id(consts.id);
            }
            if (consts.hasOwnProperty('time_in')) {
                this.time_in(consts.time_in);
                this.time_in_label(this.formatDateString(consts.time_in));
            }
            if (consts.hasOwnProperty('time_out')) {
                this.time_out(consts.time_out);
                this.time_out_label(this.formatDateString(consts.time_out));
            }
            if (consts.hasOwnProperty('hours')) {
                this.hours(consts.hours);
            }
            if (consts.hasOwnProperty('employee')) {
                this.employee(consts.employee);
            }

        }.bind(this);

        this.formatDateString = function (time) {
            if (!time) {
                return '-';
            }

            const d = new Date(time);
            const shiftWeekdayIndex = d.getDay();
            const shiftWeekday = dayLabels[shiftWeekdayIndex];

            let shiftMinutes = d.getMinutes();
            if (shiftMinutes < 10) {
                shiftMinutes = '0' + shiftMinutes;
            }

            let shiftHours = d.getHours();
            if (shiftHours < 10) {
                shiftHours = '0' + shiftHours;
            }

            const shiftTime = shiftHours + ':' + shiftMinutes;

            const shiftYear = d.getFullYear();

            let shiftMonth = (d.getMonth() + 1);
            if (shiftMonth < 10) {
                shiftMonth = '0' + shiftMonth;
            }

            let shiftDay = d.getDate();
            if (shiftDay < 10) {
                shiftDay = '0' + shiftDay;
            }

            const shiftDate = shiftYear + '-' + shiftMonth + '-' + shiftDay;

            const dateStr = shiftWeekday + ', ' + shiftDate + ', ' + shiftTime;

            return dateStr;

        }.bind(this);

        this.summary = function () {
            window.location = '/timeclock/summary/' + this.id();
        }.bind(this);

        this.editShift = function () {
            const data = this.toDict();
            const editShift = new Shift(data);
            this.shiftToEdit(editShift);

            this.updating(true);
        }.bind(this);

        this.cancelEdit = function () {
            this.updating(false);
        }.bind(this);

        this.bindInputs = function (e) {
            $(e).find('.time-in-input').datetimepicker({
                showSecond: true,
                dateFormat: 'mm/dd/yy',
                timeFormat: 'hh:mm:ss',
            });
            $(e).find('.time-out-input').datetimepicker({
                showSecond: true,
                dateFormat: 'mm/dd/yy',
                timeFormat: 'hh:mm:ss',
            });
        }.bind(this);

        this.update = function () {
            let url = shiftUrl;
            let requestType = 'POST';
            const data = this.shiftToEdit().toDict();
            const csrf = $('input[name="csrfmiddlewaretoken"]').val();

            if (data.id) {
                url += data.id + '/';
                requestType = 'PUT';
            }

            const startingTimestampToBeSaved = new Date(data.time_in).getTime();
            const endingTimestampToBeSaved = new Date(data.time_out).getTime();
            const currentDate = new Date().getTime();

            if (startingTimestampToBeSaved > endingTimestampToBeSaved) {
                alert('Time In Cannot Be After Time Out, Check Shift On:\n' + data.time_in);
                return;
            }

            if ((startingTimestampToBeSaved > currentDate) || (endingTimestampToBeSaved > currentDate)) {
                alert('Shift Time(s) Cannot Be In the Future, Check Shift On:\n' + data.time_out);
                return;
            }

            return $.ajax({
                url: url,
                dataType: 'json',
                type: requestType,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrf);
                },
                data: JSON.stringify(data),
            }).done(() => {
                $(window).trigger('shift-updated');
            }).fail((resp) => {
                alert(resp.responseText);
            });

        }.bind(this);

        this.deleteWarning = function () {
            $('#delete-warning #delete-shift-btn').off('click').on('click', () => {
                __this.deleteShift();
                $('#delete-warning').modal('hide');
            });
            $('#delete-warning').modal();
        }.bind(this);

        this.deleteShift = function () {
            if (!this.id()) {
                return $.Deferred().reject().promise();
            }

            const url = shiftUrl + this.id() + '/';
            const requestType = 'DELETE';
            const csrf = $('input[name="csrfmiddlewaretoken"]').val();

            return $.ajax({
                url: url,
                dataType: 'json',
                type: requestType,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrf);
                },
            }).done(() => {

                $(window).trigger('shift-updated');

            }).fail((resp) => {

                alert(resp.responseText);

            });

        }.bind(this);

        this.toDict = function () {
            return {
                id: this.id(),
                time_in: this.time_in(),
                time_out: this.time_out(),
                hours: this.hours(),
                employee: this.employee(),
            };
        }.bind(this);

        this.init(consts);
    };

    $.fn.Shift = Shift;
});
