$(function() {
    "use strict";

    var Timesheets = $.fn.Timesheets;
    var MessageCenter = $.fn.MessageCenter;


    var ManageTimesheets = function(vars) {
        this.messageCenter = ko.observable(new MessageCenter());

        this.createFrom = ko.observable();
        this.createTo = ko.observable();
        this.createEmployee = ko.observable();

        var timesheets = new Timesheets({"messageCenter": this.messageCenter()});
        this.timesheetList = ko.computed(function() {

            return timesheets.timesheetList() ? timesheets.timesheetList() : [];
        }, this);


        this.createTimesheet = function() {
            var newTsData = {
                start: (new Date(this.createFrom())).getTime()/1000,
                end: (new Date(this.createTo())).getTime()/1000,
                employee: this.createEmployee()
            };

            timesheets.createTimesheet(newTsData);
        }.bind(this);

        var setupPickers = function() {
            $('.input-daterange').datepicker();
        };

        var init = function(vars) {
            vars = vars || {};

            timesheets.refresh();

            setupPickers();
        }.bind(this);

        init(vars);
    };

    $.fn.ManageTimesheets = ManageTimesheets;
});