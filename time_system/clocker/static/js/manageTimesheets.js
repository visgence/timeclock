$(() => {
    'use strict';

    const Timesheets = $.fn.Timesheets;
    const Timesheet = $.fn.Timesheet;
    const MessageCenter = $.fn.MessageCenter;


    const ManageTimesheets = function (consts) {

        this.messageCenter = ko.observable(new MessageCenter());
        this.newTimesheet = ko.observable();

        const timesheets = new Timesheets({messageCenter: this.messageCenter()});
        this.timesheetList = ko.computed(() => {
            return timesheets.timesheetList() ? timesheets.timesheetList() : [];
        }, this);

        this.employeeOptions = ko.observableArray();

        this.createTimesheet = function () {
            const __this = this;

            this.newTimesheet().create().done(() => {
                const newTs = {messageCenter: __this.messageCenter()};
                __this.newTimesheet(new Timesheet(newTs));
                setupPickers();
                timesheets.refresh().done(prepareCollapses);
            });
        }.bind(this);

        const setupPickers = function () {
            $('#start-time').datetimepicker({
                format: 'YYYY-MM-DD',
            }).on('dp.change', (ev) => {
                $('#end-time').data('DateTimePicker').minDate(ev.date);
            });
            $('#end-time').datetimepicker({
                format: 'YYYY-MM-DD',
            }).on('dp.change', (ev) => {
                $('#start-time').data('DateTimePicker').maxDate(ev.date);
            });
        };

        this.shouldSeperate = function (curTsIndex, nextTsIndex) {
            if (this.timesheetList().length <= 1 || nextTsIndex >= this.timesheetList().length) {
                return false;
            }

            const curTs = this.timesheetList()[curTsIndex];
            const nextTs = this.timesheetList()[nextTsIndex];
            if (curTs.startTimestamp() === nextTs.startTimestamp()) {
                return false;
            }

            return true;
        }.bind(this);

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
                updateHash({timesheet: ts});
            }
        };

        // Called when the timesheets list finishes refreshing during module init.
        const tsRefreshCallback = function (resp) {
            prepareCollapses();
            $(window).trigger('hashchange');
        };

        // Add needed hooks to bootstrap collapse elements for when a user tries to toggle a timesheet.
        const prepareCollapses = function () {
            $('.panel-collapse').collapse({toggle: false, parent: '#timesheet-accordion'});
            $('#timesheet-accordion').on('click', 'a.collapse-toggle', toggleTsCallback);
        };

        const init = function (consts) {
            consts = consts || {};

            if (consts.hasOwnProperty('employeeOptions')) {
                consts.employeeOptions.unshift({id: -1, display: 'All'});
                this.employeeOptions(consts.employeeOptions);
            }

            timesheets.refresh().done(tsRefreshCallback);

            setupPickers();

            const newTs = {messageCenter: this.messageCenter()};
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

        const pageNum = parseInt(location.search.split('=')[1]);
        let total = Math.round((this.timesheetList().length / 10) + 0.5);

        this.pageNum = 1;

        if (isNaN(pageNum)) {
            window.history.pushState('timesheets', 'timesheets', '?page=' + this.pageNum);
        } else {
            this.pageNum = pageNum;
        }

        this.nextPage = function () {
            total = location.search.split('&')[1].split('=')[1];
            if (this.pageNum < total) {
                this.pageNum += 1;
                window.history.pushState('timesheets', 'timesheets', '?page=' + this.pageNum + '&of=' + total);
                location.reload();
            }
        }.bind(this);

        this.prevPage = function () {
            total = location.search.split('&')[1].split('=')[1];
            if (this.pageNum > 1) {
                this.pageNum -= 1;
                window.history.pushState('timesheets', 'timesheets', '?page=' + this.pageNum + '&of=' + total);
                location.reload();
            }
        }.bind(this);

        this.lastPage = function () {
            total = location.search.split('&')[1].split('=')[1];
            window.history.pushState('timesheets', 'timesheets', '?page=' + total + '&of=' + total);
            location.reload();
        }.bind(this);

        this.firstPage = function () {
            total = location.search.split('&')[1].split('=')[1];
            window.history.pushState('timesheets', 'timesheets', '?page=' + 1 + '&of=' + total);
            location.reload();
        }.bind(this);

        init(consts);
    };

    $.fn.ManageTimesheets = ManageTimesheets;
});
