$(() => {
    'use strict';

    const ManageShifts = function (vars) {
        const __this = this;
        const ShiftList = $.fn.ShiftList;
        const TimelineShifts = $.fn.TimelineShifts;
        const employeeUrl = '/timeclock/employees/';

        const oneHourInMs = 3600000;
        const oneDayInMs = 86400000;
        const oneWeekInMs = 604800000;

        const shiftListData = {
            per_page: 25,
        };

        this.shiftList = ko.observable();
        this.weekOf = ko.observable();
        this.currentWeekOffset = ko.observable();
        this.timelineShifts = ko.observable();
        this.startingTimestamp = 0;
        this.endingTimestamp = ko.observable();
        this.employees = ko.observableArray();
        this.managingEmployee = ko.observable();

        this.employee = ko.observable();
        this.selectedEmployee = ko.computed({
            read: function () {
                return this.employee();
            },
            write: function (emp) {
                updateHash({
                    emp: emp.id,
                });
            },
        }, this);

        this.managingSelf = ko.computed(function () { //eslint-disable-line
            const selectedEmp = this.selectedEmployee();
            const managingEmp = this.managingEmployee();
            let managing = false;

            if (selectedEmp && managingEmp && selectedEmp.id === managingEmp.id) {
                managing = true;
            }
            return managing;
        }.bind(this));

        this.init = function (vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('managingEmployee')) {
                this.managingEmployee(vars.managingEmployee);
            }
            this.calculateStartingTimestamp();
            this.shiftList(new ShiftList(shiftListData));
            this.timelineShifts(new TimelineShifts());
            // TODO: this will change once I get more time to do something more proper
            $(window).on('shift-updated', () => {
                __this.shiftList().reload(__this.startingTimestamp, __this.endingTimestamp, __this.selectedEmployee().id);
            });

            $(window).on('hashchange', hashchangeHandler);
            return loadEmployees().then(() => {
                $(window).trigger('hashchange');
            });
            // setInputBindings();
        };

        const hashchangeHandler = function (e) {
            const state = getHash();
            if (state.hasOwnProperty('emp')) {
                const empId = parseInt(state.emp);
                $.each(__this.employees(), (i, emp) => {
                    if (empId === emp.id) {
                        __this.employee(emp);
                        console.log(emp.id);
                        __this.shiftList().reload(this.startingTimestamp, this.endingTimestamp, emp.id);
                        __this.timelineShifts().reload(this.startingTimestamp, this.endingTimestamp, emp.id);
                        return false;
                    }
                });
            }
        }.bind(this);

        // Checks if the shift table should add a blank row to seperate groups of shifts by day
        // this.shouldAddSeperator = function (index, nextIndex) {

        //     if (index >= this.shiftList().shifts().length || nextIndex >= this.shiftList().shifts().length) {
        //         return false;
        //     }
        //     const currentDate = new Date(this.shiftList().shifts()[index].time_in());
        //     const nextDate = new Date(this.shiftList().shifts()[nextIndex].time_in());

        //     if (currentDate.getDate() !== nextDate.getDate()) {
        //         return true;
        //     }
        //     return false;
        // }.bind(this);

        this.prevPage = function () {

            const state = getHash();
            if (state.hasOwnProperty('emp')) {
                const empId = parseInt(state.emp);

                this.startingTimestamp = this.DecrementTimestampByWeek(this.startingTimestamp);
                this.endingTimestamp = this.DecrementTimestampByWeek(this.endingTimestamp);


                __this.timelineShifts().reload(this.startingTimestamp, this.endingTimestamp, empId);

                __this.shiftList().reload(this.startingTimestamp, this.endingTimestamp, empId);

            }

        }.bind(this);

        this.nextPage = function () {

            const state = getHash();
            if (state.hasOwnProperty('emp')) {
                const empId = parseInt(state.emp);

                this.startingTimestamp = this.IncrementTimestampByWeek(this.startingTimestamp);
                this.endingTimestamp = this.IncrementTimestampByWeek(this.endingTimestamp);


                __this.timelineShifts().reload(this.startingTimestamp, this.endingTimestamp, empId);

                __this.shiftList().reload(this.startingTimestamp, this.endingTimestamp, empId);

            }

        }.bind(this);


        this.calculateStartingTimestamp = function () {

            let currentDayOfWeek = new Date().getDay(); //  return 0-6 day indexes (Sun- Sat)

            if (currentDayOfWeek === 0) { //    set monday to be start of work week, sunday last, all other days shifted back by 1
                currentDayOfWeek = 6;
            } else if (currentDayOfWeek === 1) {
                currentDayOfWeek = 0;
            } else {
                currentDayOfWeek -= 1;
            }

            const timezoneOffset = new Date().getTimezoneOffset();

            let beginningOfWorkWeek = (new Date().setHours(0, 0, 0, 0)) - ((currentDayOfWeek) * oneDayInMs);

            const newTimezoneOffset = new Date(beginningOfWorkWeek).getTimezoneOffset();

            const totalTimezoneOffset = Math.abs(timezoneOffset - newTimezoneOffset) / 60;

            if (timezoneOffset > newTimezoneOffset) { //    add or subtract hours based on UTC Offset changes.
                beginningOfWorkWeek -= (oneHourInMs * totalTimezoneOffset);
            } else if (timezoneOffset < newTimezoneOffset) {
                beginningOfWorkWeek += (oneHourInMs * totalTimezoneOffset);
            }

            this.startingTimestamp = beginningOfWorkWeek;

            this.endingTimestamp = this.startingTimestamp + oneWeekInMs;

            return beginningOfWorkWeek;
        };

        this.DecrementTimestampByWeek = (timestamp) => {

            //  Decrements timestamp by week, accounting for timezone offset

            const timezoneOffset = new Date(timestamp).getTimezoneOffset();

            const newTimezoneOffset = new Date(timestamp - oneWeekInMs).getTimezoneOffset();

            const totalTimezoneOffset = Math.abs(timezoneOffset - newTimezoneOffset) / 60;

            if (timezoneOffset > newTimezoneOffset) {
                return timestamp - (oneWeekInMs + (oneHourInMs * totalTimezoneOffset));

            } else if (timezoneOffset < newTimezoneOffset) {
                return timestamp - (oneWeekInMs - (oneHourInMs * totalTimezoneOffset));
            }

            return timestamp - oneWeekInMs;

        };

        this.IncrementTimestampByWeek = (timestamp) => {

            //  Increments timestamp by week, accounting for timezone offset

            const timezoneOffset = new Date(timestamp).getTimezoneOffset();

            const newTimezoneOffset = new Date(timestamp + oneWeekInMs).getTimezoneOffset();

            const totalTimezoneOffset = Math.abs(timezoneOffset - newTimezoneOffset) / 60;

            if (timezoneOffset > newTimezoneOffset) {
                return timestamp + (oneWeekInMs - (oneHourInMs * totalTimezoneOffset));

            } else if (timezoneOffset < newTimezoneOffset) {
                return timestamp + (oneWeekInMs + (oneHourInMs * totalTimezoneOffset));
            }

            return timestamp + oneWeekInMs;

        };

        function loadEmployees() {
            const state = getHash();
            // If we see that there is no preset employee hash we will default to the current user.
            let setUser = false;
            if (!state.hasOwnProperty('emp')) {
                setUser = true;
            }
            return $.get(employeeUrl, (resp) => {
                $.each(resp.employees, (i, emp) => {
                    __this.employees.push(emp);
                    if (setUser && emp.id === __this.managingEmployee().id) {
                        __this.selectedEmployee(emp);
                    }
                });
            });
        };

        function setInputBindings() { //eslint-disable-line
            $('input.icon-input').on('input', () => {
                const currentVal = $(this).val();
                if (currentVal === '' && !$(this).is(':focus')) {
                    $(this).removeClass('icon-input-hide');
                } else {
                    $(this).addClass('icon-input-hide');
                }
            }).focus(() => {
                $(this).addClass('icon-input-hide');
            }).focusout(() => {
                if ($(this).val() === '') {
                    $(this).removeClass('icon-input-hide');
                }
            }).trigger('input');

            $('.date-input').bootstrapDP({
                autoclose: true,
                orientation: 'top',
                format: 'yyyy-mm-dd',
            }).on('hide', (e) => {
                $(e.target).trigger('input');
            });

            $('.time-input').timepicker({
                showMeridian: false,
                showSeconds: true,
                defaultTime: false,
                minuteStep: 1,
            }).on('show.timepicker', (e) => {
                $(e.target).val(e.time.value);
            }).on('changeTime.timepicker', (e) => {
                if (e.time.value === '') {
                    $(e.target).val('0:00:00');
                } else {
                    $(e.target).val(e.time.value);
                }
            }).val('');
        }
    };
    $.fn.ManageShifts = ManageShifts;
});
