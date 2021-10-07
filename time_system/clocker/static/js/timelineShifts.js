$(() => {
    const TimelineShifts = function () {

        /* timelineShifts.js
        Author: Jacob Bakarich
        Date: May 7, 2018

        This function uses the shift endpoint on /shifts to return get a list of shifts in a given time range.
        Shifts returned are formatted to be sorted by day of week, and then passed to ShiftTimeline to be 
        graphed.

        On selecting the "previous week" button, an additional week of shifts is requested using a new time 
        range. returned shifts are formatted and appended to an array that will be used to display weeks 
        again if "Next Week" is selected.
        
        */

        const oneHourInMs = 3600000;
        const oneDayInMs = 86400000;

        this.shiftsDividedIntoWeeks = [];
        this.startingTimestamp = 0;
        this.endingTimestamp = 0;
        this.empId = '';
        this.weekOffset = 0;
        this.employeeColor = '';
        this.firstShiftTimestamp = 0;
        this.shiftTimeline = ko.observable();

        const ShiftTimeline = $.fn.ShiftTimeline;

        this.rebuild = function (shifts, startingTimestamp, endingTimestamp, employeeColor) {

            this.shiftsDividedIntoWeeks = [];

            this.startingTimestamp = startingTimestamp;

            this.endingTimestamp = endingTimestamp;

            this.employeeColor = employeeColor;

            this.shiftTimeline(new ShiftTimeline());

            FormatShifts(shifts);

        }.bind(this);

        FormatShifts = (rawShifts) => {

            formattedShifts = BreakIntoDays(rawShifts);


            if (this.shiftsDividedIntoWeeks.length === 0) {
                this.shiftsDividedIntoWeeks = formattedShifts;
            } else {
                this.shiftsDividedIntoWeeks[this.weekOffset] = formattedShifts;
            }

            // updateLabels();

            this.shiftTimeline().rebuild(formattedShifts, this.startingTimestamp, this.employeeColor);

        };

        BreakIntoDays = (weekOfShifts) => {

            const days = [];

            for (let i = 0; i < 7; i++) {
                days[i] = [];
            }

            let shiftDay;

            for (let i = 0; i < weekOfShifts.length; i++) {
                shiftDay = new Date(weekOfShifts[i]['time_out']).getDay();
                // console.log(shiftDay);
                if (shiftDay === 0) { //    move sunday to last day of week, per billing periods
                    shiftDay = 6;
                } else if (shiftDay === 1) { // monday now first day of week
                    shiftDay = 0;
                } else {
                    shiftDay -= 1;
                }

                days[shiftDay].push(weekOfShifts[i]);
            }

            return days;
        };

        CalculateStartingTime = () => {

            //  Returns a starting timestamp for the desired work week, defined as Sunday -> Saturday
            //  Accounts for timezone offset.

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

            return beginningOfWorkWeek;
        };

    };

    $.fn.TimelineShifts = TimelineShifts;
});
