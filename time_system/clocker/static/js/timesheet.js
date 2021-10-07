$(() => {
    'use strict';

    const timesheetUrl = '/timeclock/timesheets/';
    const MessageCenter = $.fn.MessageCenter;

    const Timesheet = function (vars) {
        this.id = null;

        this.start = ko.observable().extend({
            required: 'Please specify a pay period.',
        });
        this.startTimestamp = ko.computed({
            read: function () {
                return this.start() ? (new Date(this.start())).getTime() / 1000 : NaN;
            },
            write: function (ts) {
                if (!$.isNumeric(ts)) {
                    return;
                }

                const d = new Date(ts * 1000);
                this.start(d.toLocaleDateString());
            },
        }, this);

        this.end = ko.observable().extend({
            required: 'Please specify a pay period.',
        });;
        this.endTimestamp = ko.computed({
            read: function () {
                return this.end() ? (new Date(this.end())).getTime() / 1000 : NaN;
            },
            write: function (ts) {
                if (!$.isNumeric(ts)) {
                    return;
                }
                const d = new Date(ts * 1000);
                this.end(d.toLocaleDateString());
            },
        }, this);


        this.employee = ko.observable().extend({
            required: 'Please select an employee.',
        });

        this.signature = ko.observable();
        this.signedOnMsg = ko.observable();
        this.signAgreement = ko.observable(false).extend({
            required: 'Please Accept the timesheet.',
        });

        this.shifts = ko.observableArray();
        this.isBusy = ko.observable(false);

        this.timeperiod = ko.computed(function () {
            const start = new Date(this.startTimestamp() * 1000);
            const end = new Date(this.endTimestamp() * 1000);

            return start.localeDateFormat() + ' - ' + end.localeDateFormat();
        }, this);

        this.employeeName = ko.computed(function () {
            const employee = this.employee();
            if (!employee) {
                return '';
            }

            return employee.first_name + ' ' + employee.last_name;
        }, this);

        this.belongsToUser = function (user) {
            const employee = this.employee();
            return employee.username === user ? true : false;
        };

        this.messageCenter = ko.observable();

        const init = function (vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('id')) {
                this.id = vars.id;
            }

            if (vars.hasOwnProperty('start')) {
                this.startTimestamp(vars.start);
            }

            if (vars.hasOwnProperty('end')) {
                this.endTimestamp(vars.end);
            }

            if (vars.hasOwnProperty('employee')) {
                this.employee(vars.employee);
            }

            if (vars.hasOwnProperty('shifts')) {
                this.shifts(vars.shifts);
            }

            if (vars.hasOwnProperty('messageCenter')) {
                this.messageCenter(vars.messageCenter);
            } else {
                this.messageCenter(new MessageCenter());
            }
            if (vars.hasOwnProperty('signature')) {
                this.signedOnMsg = 'Timesheet signed';
            }

            if (vars.hasOwnProperty('signatureDate')) {
                this.signedOnMsg = 'Signed on ' + vars.signatureDate;
            }
            this.rebuild(vars);
        }.bind(this);

        this.rebuild = function (vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('signature')) {
                this.signature(vars.signature);
            }
        }.bind(this);

        this.validateCreation = function () {
            let noErrors = true;

            if (this.id !== null) {
                this.messageCenter().setErrors('This timesheet appears to already be created! This should not have happened...');
                noErrors = false;
            }

            if (!this.start.validate()) {
                noErrors = false;
            }
            if (!this.end.validate()) {
                noErrors = false;
            }
            if (!this.employee.validate()) {
                noErrors = false;
            }

            return noErrors;
        }.bind(this);

        this.signTimesheet = function () {
            if (!this.signAgreement.validate()) {
                return $.Deferred().reject().promise();
            }
            const __this = this;
            const url = timesheetUrl + this.id + '/';
            const requestType = 'PUT';
            const payload = {
                action: 'sign',
            };

            return this.update(url, requestType, payload).done(__this.rebuild);
        }.bind(this);

        this.payData = ko.observable();
        this.loadPayData = function () {
            if (this.payData()) {
                return $.Deferred().resolve().promise();
            }
            const __this = this;
            const url = timesheetUrl + this.id + '/';
            this.isBusy(true);

            return $.get(url, (resp) => {
                __this.payData(resp);
            })
                .always(() => {
                    __this.isBusy(false);
                });
        }.bind(this);

        this.create = function () {
            if (!this.validateCreation()) {
                return $.Deferred().reject().promise();
            }
            const url = timesheetUrl;
            const requestType = 'POST';
            const payload = this.creationData();

            return this.update(url, requestType, payload);
        }.bind(this);

        this.update = function (url, requestType, payload) {
            this.messageCenter().dismissErrors();

            return $.ajax({
                url: url,
                dataType: 'json',
                type: requestType,
                beforeSend: function (xhr) {
                    const csrf = $('input[name="csrfmiddlewaretoken"]').val();
                    xhr.setRequestHeader('X-CSRFToken', csrf);
                },
                data: JSON.stringify(payload),
            })
                .fail(failUpdateCallback.bind(this));

        }.bind(this);

        this.creationData = function () {
            return {
                start: this.startTimestamp(),
                end: this.endTimestamp(),
                employee: this.employee(),
            };
        }.bind(this);

        const failUpdateCallback = function (resp) {
            console.log(resp);
            if (resp.hasOwnProperty('responseJSON')) {
                this.messageCenter().setErrors(resp.responseJSON);
            } else if (resp.hasOwnProperty('responseText')) {
                this.messageCenter().setErrors(resp.responseText);
            } else {
                this.messageCenter().setErrors('something unexpected occured.');
                console.error(resp);
            }
        };

        init(vars);
    };

    $.fn.Timesheet = Timesheet;
});
