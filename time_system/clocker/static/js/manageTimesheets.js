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
                timesheets.refresh().done(prepareCollapses);
            });
        }.bind(this);

        var setupPickers = function() {
            $('.input-daterange').datepicker();
        };

        this.shouldSeperate = function(curTsIndex, nextTsIndex) {
            if (curTsIndex == 0 || this.timesheetList().length <= 1 || nextTsIndex >= this.timesheetList().length)
                return false;
            
            var curTs = this.timesheetList()[curTsIndex];
            var nextTs = this.timesheetList()[nextTsIndex];
            if (curTs.startTimestamp() == nextTs.startTimestamp())
                return false;

            return true;
        }.bind(this);

        var prepareCollapses = function() {
            $("#timesheet-accordion").on("show.bs.collapse", function(e) {
                var targetTs = ko.dataFor(e.target);
                targetTs.loadPayData();
            })
        };

        var init = function(vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('employeeOptions')) {
                vars.employeeOptions.unshift({"id": -1, display: "All"});
                this.employeeOptions(vars.employeeOptions);            
            }

            timesheets.refresh().done(prepareCollapses);
            setupPickers();

            var newTs = {"messageCenter": this.messageCenter()};
            this.newTimesheet(new Timesheet(newTs));
        }.bind(this);

        init(vars);
    };

    $.fn.ManageTimesheets = ManageTimesheets;
});