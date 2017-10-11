$(() => {
    'use strict';

    const Shift = function (consts) {
        const __this = this;
        const shiftUrl = '/timeclock/shifts/';

        this.id = ko.observable();
        this.time_in = ko.observable();
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
            }
            if (consts.hasOwnProperty('time_out')) {
                this.time_out(consts.time_out);
            }
            if (consts.hasOwnProperty('hours')) {
                this.hours(consts.hours);
            }
            if (consts.hasOwnProperty('employee')) {
                this.employee(consts.employee);
            }

        }.bind(this);

        this.getTimeInDate = function () {
            if (!this.time_in()) {
                return '';
            }

            const d = new Date(this.time_in());
            const dateStr = (d.getMonth() + 1) + '/' +
                (d.getDate().length === 1 ? '0' + d.getDate() : d.getDate()) + '/' +
                d.getFullYear();
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

            return $.ajax({
                url: url,
                dataType: 'json',
                type: requestType,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrf);
                },
                data: JSON.stringify(data),
            })
                .done(() => {
                    $(window).trigger('shift-updated');
                })
                .fail((resp) => {
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
            })
                .done(() => {
                    $(window).trigger('shift-updated');
                })
                .fail((resp) => {
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
