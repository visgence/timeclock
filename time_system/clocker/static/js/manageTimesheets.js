$(function() {
    "use strict";

    var Timesheets = $.fn.Timesheets;
    var Timesheet = $.fn.Timesheet;
    var MessageCenter = $.fn.MessageCenter;


    var ManageTimesheets = function(vars) {
        
        this.messageCenter = ko.observable(new MessageCenter());
        this.newTimesheet = ko.observable();

        var timesheets = new Timesheets({"messageCenter": this.messageCenter()});
        this.timesheetList = ko.computed(function() {
            return timesheets.timesheetList() ? timesheets.timesheetList() : [];
        }, this);

        this.employeeOptions = ko.observableArray();

        this.createTimesheet = function() {
            var __this = this;

            this.newTimesheet().create().done(function() {
                var newTs = {"messageCenter": __this.messageCenter()};
                __this.newTimesheet(new Timesheet(newTs));
                setupPickers();
                timesheets.refresh();
            });
        }.bind(this);

        var setupPickers = function() {
            $('.input-daterange').datepicker();
        };

        var init = function(vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('employeeOptions')) {
                vars.employeeOptions.unshift({"id": -1, display: "All"});
                this.employeeOptions(vars.employeeOptions);            
            }

            timesheets.refresh();
            setupPickers();

            var newTs = {"messageCenter": this.messageCenter()};
            this.newTimesheet(new Timesheet(newTs));
        }.bind(this);

        init(vars);
    };

    $.fn.ManageTimesheets = ManageTimesheets;
});