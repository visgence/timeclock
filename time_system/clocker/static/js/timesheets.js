$(function() {
    "use strict";

    var url = "/timeclock/timesheets/";
    var Timesheet = $.fn.Timesheets;


    var Timesheets = function(vars) {
        this.timesheetList = ko.observableArray();

    };

    var failcallback = function(resp) {
        console.log("FAILURE!!!!");
        console.log(resp);
    };


    Timesheets.prototype.rebuild = function(vars) {
        vars = vars || {};
        if (vars.hasOwnProperty('timesheetList')) {
            var tmp_tsList = [];
            $.each(vars.timesheetList, function(i, ts) {
                var newTs = new TimeSheet(ts);
                tmp_tsList.push(newTs);
            });
            
            this.timesheetList(tmp_tsList);
        }
    };

    Timesheets.prototype.refresh = function() {
        return $.getJSON(url).then(this.rebuild.bind(this), failcallback);
    };

    $.fn.Timesheets = Timesheets;
});