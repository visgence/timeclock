$(function() {
    "use strict";

    var url = "/timeclock/timesheets/";
    var Timesheet = $.fn.Timesheet;
    var MessageCenter = $.fn.MessageCenter;

    var Timesheets = function(vars) {
        this.timesheetList = ko.observableArray();

        this.messageCenter = ko.observable();

        var init = function(vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('messageCenter'))
                this.messageCenter(vars.messageCenter);
            else
                this.messageCenter(new MessageCenter());

        }.bind(this);

        init(vars);
    };

    var failcallback = function(resp) {
        this.messageCenter().setErrors(resp)
    };


    Timesheets.prototype.rebuild = function(vars) {
        vars = vars || {};
        if (vars.hasOwnProperty('timesheetList')) {
            var tmp_tsList = [];
            $.each(vars.timesheetList, function(i, ts) {
                var newTs = new Timesheet(ts);
                tmp_tsList.push(newTs);
            });
            
            this.timesheetList(tmp_tsList);
        }
    };

    Timesheets.prototype.refresh = function() {
        var __this = this;
        return $.getJSON(url).then(__this.rebuild.bind(__this), failcallback);
    };

    Timesheets.prototype.createTimesheet = function(data) {
        var __this = this;
        data['messageCenter'] = this.messageCenter();
        var newTimesheet = new Timesheet(data);
        newTimesheet.create().then(__this.refresh.bind(__this)); 
    };

    Timesheets.prototype.createTimesheets = function(data) {
        if (!$.isArray(data))
            return;
    
        return $.ajax({
             url: url
            ,dataType: 'json'
            ,type: "POST"
            ,beforeSend: function(xhr) {
                var csrf = $('input[name="csrfmiddlewaretoken"]').val();
                xhr.setRequestHeader('X-CSRFToken', csrf);
            }
            ,data: JSON.stringify(data)
        });
    };

    $.fn.Timesheets = Timesheets;
});