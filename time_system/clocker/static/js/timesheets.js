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
            var pageNum = parseInt(location.search.split("=")[1])
            for(var i = pageNum*10-10; i < vars.timesheetList.length; i++){
                if(i > pageNum*10) break;
                tmp_tsList.push(new Timesheet(vars.timesheetList[i]));
            }
            var count = Math.round((vars.timesheetList.length/10)+0.5)
             window.history.pushState("timesheets", "timesheets", location.search.split("&")[0] + "&of="+count)

            this.timesheetList(tmp_tsList);
        }
    };

    Timesheets.prototype.refresh = function() {
        var __this = this;
        return $.getJSON(url).then(__this.rebuild.bind(__this), failcallback);
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
