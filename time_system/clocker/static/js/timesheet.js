$(function() {
    "use strict";

    var timesheetUrl = "/timeclock/timesheets/";
    var MessageCenter = $.fn.MessageCenter;
    
    var Timesheet = function(vars) {

        this.id = null;
        
        this.start = ko.observable().extend({required: "Please specify a pay period."});
        this.startTimestamp = ko.computed({
            read: function() {
                return this.start() ? (new Date(this.start())).getTime()/1000 : NaN;
            },
            write: function(ts) {
                if (!$.isNumeric(ts))
                    return;

                var d = new Date(ts*1000);
                this.start(d.toLocaleDateString());
            }
        }, this);
        
        this.end = ko.observable().extend({required: "Please specify a pay period."});;
        this.endTimestamp = ko.computed({
            read: function() {
                return this.end() ? (new Date(this.end())).getTime()/1000 : NaN;
            },
            write: function(ts) {
                if (!$.isNumeric(ts))
                    return;

                var d = new Date(ts*1000);
                this.end(d.toLocaleDateString());
            }
        }, this);
        

        this.employee = ko.observable().extend({required: "Please select an employee."});
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

            if (this.id !== null) {
                this.messageCenter().setErrors("This timesheet appears to already be created! This should not have happened...");
                noErrors = false;
            }
            
            if (!this.start.validate()) noErrors = false;
            if (!this.end.validate()) noErrors = false;
            if (!this.employee.validate()) noErrors = false;

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
            if (!this.validateCreation())
                return $.Deferred().reject().promise();

            var url = timesheetUrl;
            var requestType = "POST";
            var payload = {
                start: this.startTimestamp(),
                end: this.endTimestamp(),
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