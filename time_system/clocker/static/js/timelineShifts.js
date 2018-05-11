$(() => {
    const TimelineShifts = function () {

        /* timelineShifts.js
        Author: Jacob Bakarich
        Date: May 7, 2018

        This function uses the same endpoint as shiftList to get a paginated list of logged shifts,
        then formats the shifts into work weeks and days, and calls Timeline.js to use d3 to graph formatted
        shifts.

        The shifts are formatted from a paginated list into an array sorted by work weeks, and week days. 
        Timeline.js graphs one week at a time, and displaying previous/next weeks are supported via prev
        week and nextWeek functions. 


        Next 'page' of shifts are automatically requested when the current page's worth of shifts is
        reached. If no more pages are availible, the "previous week" button is hidden.

        */


        const shiftUrl = '/timeclock/shifts/';
        const oneHourInMs = 3600000;
        const oneDayInMs = 86400000;
        const oneWeekInMs = 604800000;

        this.shiftsDividedIntoWeeks = [];
        this.startingTimestamp = 0;
        this.empId = '';
        this.weekOffset = 0;
        this.employeeColor = '';
        this.isReloading = false;
        this.firstShiftTimestamp = 0;
        this.shiftTimeline = ko.observable();

        const ShiftTimeline = $.fn.ShiftTimeline;

        this.reload = function (empId) {

            this.startingTimestamp = CalculateStartingTime();

            this.shiftsDividedIntoWeeks = [];

            this.weekOffset = 0;

            this.isReloading = true;

            this.shiftTimeline(new ShiftTimeline());

            this.empId = empId;

            processShifts = (rawShifts) => {

                FormatShifts(rawShifts);

                updateLabels();

            };

            handleError = (error) => {
                console.log(error);
            };

            getShifts().then(processShifts, handleError);


        }.bind(this);


        this.nextWeek = function () {

            this.weekOffset -= 1;

            console.log(this.weekOffset);

            console.log(this.shiftsDividedIntoWeeks);
            console.log(this.shiftsDividedIntoWeeks[this.weekOffset]);

            this.startingTimestamp = IncrementTimestampByWeek(this.startingTimestamp);

            this.shiftTimeline().rebuild(this.shiftsDividedIntoWeeks[this.weekOffset], this.startingTimestamp, this.employeeColor);

            updateLabels();

        }.bind(this);

        this.prevWeek = function () {

            this.weekOffset += 1;

            this.startingTimestamp = DecrementTimestampByWeek(this.startingTimestamp);

            processShifts = (rawShifts) => {

                FormatShifts(rawShifts);

            };

            handleError = (error) => {
                console.log(error);
            };

            getShifts().then(processShifts, handleError);

            updateLabels();

        }.bind(this);

        FormatShifts = (rawShifts) => {

            if (rawShifts.length === 0) {
                return [];
            }

            formattedShifts = BreakIntoDays(rawShifts);


            if (this.shiftsDividedIntoWeeks.length === 0) {
                this.shiftsDividedIntoWeeks = formattedShifts;
            } else {
                this.shiftsDividedIntoWeeks[this.weekOffset] = formattedShifts;
            }

            updateLabels();

            console.log(this.shiftsDividedIntoWeeks);

            this.shiftTimeline().rebuild(formattedShifts, this.startingTimestamp, this.employeeColor);

        };

        DecrementTimestampByWeek = (timestamp) => {

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

        IncrementTimestampByWeek = (timestamp) => {

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

        BreakIntoDays = (weekOfShifts) => {

            // console.log(weekOfShifts);

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

            // console.log(days);

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

        getShifts = () => {

            const promise = new Promise((resolve, reject) => {

                let startingTimestampInSeconds = this.startingTimestamp / 1000;
                let endingTimestampinSeconds = (this.startingTimestamp + oneWeekInMs) / 1000;


                $.ajax({
                    url: shiftUrl + '?starting_timestamp=' + startingTimestampInSeconds + '&ending_timestamp=' + endingTimestampinSeconds + '&employee=' + this.empId,
                    type: 'GET',
                    success: (data) => {

                        if (data.shifts.length > 0) {
                            this.employeeColor = data.shifts[0].employee.employee_color;
                            this.firstShiftTimestamp = new Date(data.first_shift).getTime();
                            resolve(data.shifts);
                        } else {
                            resolve([]);
                        }
                    },
                    error: (error) => {
                        reject(error);
                    },

                });

            });
            return promise;

        };

        getNextPageOfShifts = () => {

            processShifts = (rawShifts) => {

                FormatShifts(rawShifts);

                updateLabels();

            };

            handleError = (error) => {
                console.log(error);
            };

            this.pageNum += 1;

            getShifts().then(processShifts, handleError);

        };

        updateLabels = () => {

            // console.log("WAT");

            const months = [
                'January',
                'February',
                'March',
                'April',
                'May',
                'June',
                'July',
                'August',
                'September',
                'October',
                'November',
                'December',
            ];

            const startingDate = new Date(this.startingTimestamp);

            const endingDate = new Date(IncrementTimestampByWeek(this.startingTimestamp - oneDayInMs));

            const startingLabel = months[startingDate.getMonth()] + ' ' + startingDate.getDate() + ', ' + startingDate.getFullYear();

            const endingLabel = months[endingDate.getMonth()] + ' ' + endingDate.getDate() + ', ' + endingDate.getFullYear();

            $('#week-range-label').text(startingLabel + ' - ' + endingLabel);

            if (this.weekOffset === 0) {
                $('#next-week-button').hide();
            } else {
                $('#next-week-button').show();
            }

            if (this.startingTimestamp < this.firstShiftTimestamp) {
                $('#prev-week-button').hide();
            } else {
                $('#prev-week-button').show();
            }
        };

    };

    $.fn.TimelineShifts = TimelineShifts;
});