$(() => {
    'use strict';

    const Timesheet = $.fn.Timesheet;
    const MessageCenter = $.fn.MessageCenter;


    const ManageTimesheets = function (consts) {

        this.messageCenter = ko.observable(new MessageCenter());
        this.newTimesheet = ko.observable();
        this.pageNum = ko.observable(1);
        this.totalPages = ko.observable();
        this.currentPage = ko.observable();
        this.isFirstPage = ko.computed(() => {
            return this.pageNum() === 1;
        });
        this.isLastPage = ko.computed(() => {
            return this.pageNum() === this.currentPage();
        });
        this.timesheets = ko.observableArray();
        this.employeeOptions = ko.observableArray();

        this.createTimesheet = function () {
            const __this = this;

            this.newTimesheet().create().done(() => {
                const newTs = {
                    messageCenter: __this.messageCenter()
                };
                __this.newTimesheet(new Timesheet(newTs));
                setupPickers();
                this.pageNum(1);
                this.getTimesheets();
            });
        }.bind(this);

        const setupPickers = function () {
            $('.input-daterange').datepicker();
        };

        // Called when user clicks on a timesheet to toggle open/close
        const toggleTsCallback = function (e) {
            const state = getHash();
            const ts = $(e.target).data('target');

            // If timesheet is already the current state just toggle it
            if (state.hasOwnProperty('timesheet') && state.timesheet === ts) {
                const collapsable = $('#timesheet-' + state.timesheet);
                const targetTs = ko.dataFor(collapsable.get(0));
                if (!targetTs.isBusy()) {
                    $(collapsable).collapse('toggle');
                }
            } else {
                updateHash({
                    timesheet: ts,
                });
            }
        }.bind(this);

        // Add needed hooks to bootstrap collapse elements for when a user tries to toggle a timesheet.
        const prepareCollapses = function () {
            $('.panel-collapse').collapse({
                toggle: false,
                parent: '#timesheet-accordion',
            });
            $('#timesheet-accordion').on('click', 'a.collapse-toggle', toggleTsCallback);
        };

        const init = function (consts) {
            consts = consts || {};

            if (consts.hasOwnProperty('employeeOptions')) {
                consts.employeeOptions.unshift({
                    id: -1,
                    display: 'All',
                });
                this.employeeOptions(consts.employeeOptions);
            }

            this.pageNum(1);
            this.getTimesheets();

            setupPickers();

            const newTs = {
                messageCenter: this.messageCenter(),
            };
            this.newTimesheet(new Timesheet(newTs));
            $(window).on('hashchange', hashchange);
        }.bind(this);

        const hashchange = function () {
            const state = getHash();

            if (state.hasOwnProperty('timesheet')) {
                const collapsable = $('#timesheet-' + state.timesheet);
                const targetTs = ko.dataFor(collapsable.get(0));

                // Wait till data is loaded before opening collapse
                targetTs.loadPayData().then(() => {
                    $(collapsable).collapse('show');
                });
            }

        };

        this.getTimesheets = function () {

            const url = '/timeclock/timesheets?page=' + this.pageNum() + '&per_page=10';
            $.ajax({
                type: "GET",
                url: url,
                success: (resp) => {
                    console.log(resp)
                    this.buildTimesheets(resp['timesheets']);
                    this.totalPages(resp['totalPages']);
                    this.updateButtonVisbility();
                    prepareCollapses();
                    $(window).trigger('hashchange');
                },
                error: (error) => {
                    console.log(error);
                },
            });

        };

        this.updateButtonVisbility = function () {
            if (this.pageNum() === 1) {
                $('.previous').hide();
            } else {
                $('.previous').show();
            }
            if (this.pageNum() === this.totalPages()) {
                $('.next').hide();
            } else {
                $('.next').show();
            }
        };

        this.buildTimesheets = function (timesheets) {
            const timesheetsArray = [];
            for (let i = 0; i < timesheets.length; i++) {
                timesheetsArray.push(new Timesheet(timesheets[i]));
            }
            this.timesheets(timesheetsArray);
        };


        this.nextPage = function () {
            if (this.pageNum() < this.totalPages()) {
                this.pageNum(this.pageNum() + 1);
                this.getTimesheets();
                history.replaceState({}, document.title, ".")
            }
        }.bind(this);

        this.prevPage = function () {
            if (this.pageNum() > 1) {
                this.pageNum(this.pageNum() - 1);
                this.getTimesheets();
                history.replaceState({}, document.title, ".")
            }
        }.bind(this);

        this.lastPage = function () {
            this.pageNum(this.totalPages());
            this.getTimesheets();
            history.replaceState({}, document.title, ".")
        }.bind(this);

        this.firstPage = function () {
            this.pageNum(1);
            this.getTimesheets();
            history.replaceState({}, document.title, ".")
        }.bind(this);

        init(consts);
    };

    $.fn.ManageTimesheets = ManageTimesheets;
});