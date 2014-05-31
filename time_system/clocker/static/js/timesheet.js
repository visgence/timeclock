$(function() {
    "use strict";

    var timesheetUrl = "/timeclock/timesheets/";
    var MessageCenter = $.fn.MessageCenter;
    
    var Timesheet = function(vars) {

        this.id = null;
        this.start = ko.observable();
        this.end = ko.observable();
        this.employee = ko.observable();
        this.signature = ko.observable();
        this.shifts = ko.observableArray();

        this.timeperiod = ko.computed(function() {
            var start = new Date(this.start()*1000);
            var end = new Date(this.end()*1000);

            return start.localeDateFormat()+" - "+end.localeDateFormat();
        }, this);

        this.employeeName = ko.computed(function() {
            var employee = this.employee();
            if (!employee)
                return "";

            return employee.first_name + " " + employee.last_name;
        }, this);

        this.belongsToUser = function(user) {
            var employee = this.employee();
            return employee.username === user ? true : false;
        }

        this.messageCenter = ko.observable();
        
        var init = function(vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('id'))
                this.id = vars.id;

            if (vars.hasOwnProperty('start'))
                this.start(vars.start);

            if (vars.hasOwnProperty('end'))
                this.end(vars.end);

            if (vars.hasOwnProperty('employee'))
                this.employee(vars.employee);
           
            if (vars.hasOwnProperty('signature'))
                this.signature(vars.signature);
            
            if (vars.hasOwnProperty('shifts'))
                this.shifts(vars.shifts);
            
            if (vars.hasOwnProperty('messageCenter'))
                this.messageCenter(vars.messageCenter);
            else
                this.messageCenter(new MessageCenter());
        }.bind(this);

        this.validateCreation = function() {
            var noErrors = true;

            if (this.id !== null) noErrors = false;
            if (!this.start() || isNaN(new Date(this.start()*1000))) noErrors = false;
            if (!this.end() || isNaN(new Date(this.end()*1000))) noErrors = false;
            if (!this.employee()) noErrors = false;

            return noErrors;
        }.bind(this);

        this.signTimesheet = function() {
            var url = timesheetUrl+this.id+"/";
            var requestType = "PUT";
            var payload = {
                action: "sign"
            };
            return this.update(url, requestType, payload);
        }.bind(this);

        this.create = function() {
            if (!this.validateCreation()) {
                this.messageCenter().setErrors('Could not create!');
                return $.Deferred().reject().promise();
            }

            var url = timesheetUrl;
            var requestType = "POST";
            var payload = {
                start: this.start(),
                end: this.end(),
                employee: this.employee()
            };

            return this.update(url, requestType, payload);
        }.bind(this);

        this.update = function(url, requestType, payload) {

            return $.ajax({
                 url: url
                ,dataType: 'json'
                ,type: requestType
                ,beforeSend: function(xhr) {
                    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
                    xhr.setRequestHeader('X-CSRFToken', csrf);
                }
                ,data: JSON.stringify(payload)
            })
            .fail(failUpdateCallback.bind(this));

        }.bind(this);

        var failUpdateCallback = function(resp) {
            if (resp.hasOwnProperty('responseJSON'))
                this.messageCenter().setErrors(resp.responseJSON);
            else {
                this.messageCenter().setErrors("something unexpected occured.");
                console.error(resp);
            }
        };

        init(vars); 
    };

    $.fn.Timesheet = Timesheet;
});