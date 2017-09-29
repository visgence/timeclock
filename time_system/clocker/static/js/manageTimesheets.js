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
            if (this.timesheetList().length <= 1 || nextTsIndex >= this.timesheetList().length)
                return false;

            var curTs = this.timesheetList()[curTsIndex];
            var nextTs = this.timesheetList()[nextTsIndex];
            if (curTs.startTimestamp() == nextTs.startTimestamp())
                return false;

            return true;
        }.bind(this);

        //Called when user clicks on a timesheet to toggle open/close
        var toggleTsCallback = function(e) {
            var state = $.bbq.getState();
            var ts = $(e.target).data("target");

            //If timesheet is already the current state just toggle it
            if (state.hasOwnProperty("timesheet") && state.timesheet == ts) {
                var collapsable = $("#timesheet-"+state.timesheet);
                var targetTs = ko.dataFor(collapsable.get(0));
                if (!targetTs.isBusy())
                    $(collapsable).collapse('toggle');
            }
            else
                $.bbq.pushState({"timesheet": ts});
        };

        //Called when the timesheets list finishes refreshing during module init.
        var tsRefreshCallback = function(resp) {
            prepareCollapses();
            $(window).trigger("hashchange")
        };

        //Add needed hooks to bootstrap collapse elements for when a user tries to toggle a timesheet.
        var prepareCollapses = function() {
            $('.panel-collapse').collapse({toggle: false, parent: "#timesheet-accordion"});
            $("#timesheet-accordion").on("click", "a.collapse-toggle", toggleTsCallback);
        };

        var init = function(vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('employeeOptions')) {
                vars.employeeOptions.unshift({"id": -1, display: "All"});
                this.employeeOptions(vars.employeeOptions);
            }

            timesheets.refresh().done(tsRefreshCallback);

            setupPickers();

            var newTs = {"messageCenter": this.messageCenter()};
            this.newTimesheet(new Timesheet(newTs));
            $(window).on('hashchange', hashchange);
        }.bind(this);

        var hashchange = function() {
            var state = $.bbq.getState();

            if (state.hasOwnProperty('timesheet')) {
                var collapsable = $("#timesheet-"+state.timesheet);
                var targetTs = ko.dataFor(collapsable.get(0));

                //Wait till data is loaded before opening collapse
                targetTs.loadPayData().then(function() {
                    $(collapsable).collapse('show');
                });
            }

        };

        var pageNum = parseInt(location.search.split("=")[1]);
        var total = Math.round((this.timesheetList().length/10)+0.5);

        this.pageNum = 1;

        if (isNaN(pageNum)){
            window.history.pushState("timesheets", "timesheets", "?page="+this.pageNum)
        } else {
            this.pageNum = pageNum;
        }

        this.nextPage = function(){
            total = location.search.split("&")[1].split("=")[1]
            if(this.pageNum < total){
                this.pageNum += 1;
                window.history.pushState("timesheets", "timesheets", "?page="+this.pageNum + "&of="+total)
                location.reload();
            }
        }.bind(this);

        this.prevPage = function(){
            total = location.search.split("&")[1].split("=")[1]
            if(this.pageNum > 1){
                this.pageNum -= 1;
                window.history.pushState("timesheets", "timesheets", "?page="+this.pageNum + "&of="+total)
                location.reload();
            }
        }.bind(this);

        this.lastPage = function(){
            total = location.search.split("&")[1].split("=")[1]
            window.history.pushState("timesheets", "timesheets", "?page="+total + "&of="+total)
            location.reload();
        }.bind(this);

        this.firstPage = function(){
            total = location.search.split("&")[1].split("=")[1]
            window.history.pushState("timesheets", "timesheets", "?page="+1 + "&of="+total)
            location.reload();
        }.bind(this)

        init(vars);
    };

    $.fn.ManageTimesheets = ManageTimesheets;
});