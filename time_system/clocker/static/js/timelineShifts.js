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


        const shiftUrl = '/timeclock/shifts';
        const oneHourInMs = 3600000;
        const oneDayInMs = 86400000;
        const oneWeekInMs = 604800000;

        this.shiftsDividedIntoWeeks = [];
        this.startingTimestamp = 0;
        this.pageNum = 1;
        this.totalPages = 0;
        this.empId = '';
        this.weekOffset = 0;
        this.shiftTimeline = ko.observable();

        const ShiftTimeline = $.fn.ShiftTimeline;

        this.init = () => {

            this.shiftTimeline(new ShiftTimeline());

        };

        this.reload = function (empId) {

            this.empId = empId;

            processShifts = (rawShifts) => {

                FormatShifts(rawShifts);

                updateLabels();

            };

            handleError = (error) => {
                console.log(error);
            };

            getShifts(empId).then(processShifts, handleError);

        }.bind(this);


        this.nextWeek = function () {

            this.weekOffset -= 1;

            this.startingTimestamp = IncrementTimestampByWeek(this.startingTimestamp);

            this.shiftTimeline().rebuild(this.shiftsDividedIntoWeeks[this.weekOffset], this.startingTimestamp);

            updateLabels();

        }.bind(this);

        this.prevWeek = function () {

            this.weekOffset += 1;

            this.startingTimestamp = DecrementTimestampByWeek(this.startingTimestamp);

            if (this.weekOffset === this.shiftsDividedIntoWeeks.length) {
                getNextPageOfShifts();

            } else {

                this.shiftTimeline().rebuild(this.shiftsDividedIntoWeeks[this.weekOffset], this.startingTimestamp);

            }

            updateLabels();

        }.bind(this);

        FormatShifts = (rawShifts) => {

            if (rawShifts.length === 0) {
                return [];
            }

            const shiftsDividedIntoWeeks = [];

            let shiftsInCurrentWeek = [];

            let startingTimestamp = CalculateStartingTime();

            const timeOfLastLoggedShift = new Date(rawShifts[0]['time_in']).getTime();

            while (startingTimestamp > timeOfLastLoggedShift) { //  Pads blank weeks until last logged shift is in range
                shiftsDividedIntoWeeks.push([]);
                startingTimestamp = DecrementTimestampByWeek(startingTimestamp);
            }

            let endingTimestamp = IncrementTimestampByWeek(startingTimestamp - 1000);

            for (let i = 0; i < rawShifts.length; i++) {

                const shiftTimestamp = new Date(rawShifts[i]['time_in']).getTime();

                if (shiftTimestamp < endingTimestamp && shiftTimestamp > startingTimestamp) { //    shift is within current work week time range
                    shiftsInCurrentWeek.push(rawShifts[i]);

                } else if (shiftTimestamp < startingTimestamp) { // means that the next shift is in a different work week

                    startingTimestamp = DecrementTimestampByWeek(startingTimestamp);
                    endingTimestamp = DecrementTimestampByWeek(endingTimestamp);
                    shiftsDividedIntoWeeks.push(shiftsInCurrentWeek);

                    while (shiftTimestamp < startingTimestamp) { // pads blank weeks if the next shift farther than one work week away
                        startingTimestamp = DecrementTimestampByWeek(startingTimestamp);
                        endingTimestamp = DecrementTimestampByWeek(endingTimestamp);
                        shiftsDividedIntoWeeks.push([]);
                    }

                    shiftsInCurrentWeek = []; //    new week of shifts
                    shiftsInCurrentWeek.push(rawShifts[i]);
                }

            }

            shiftsDividedIntoWeeks.push(shiftsInCurrentWeek);

            for (let i = 0; i < shiftsDividedIntoWeeks.length; i++) {//  now break the weeks of shifts into days
                shiftsDividedIntoWeeks[i] = BreakIntoDays(shiftsDividedIntoWeeks[i]);
            }

            if (this.shiftsDividedIntoWeeks.length === 0) {

                this.shiftsDividedIntoWeeks = shiftsDividedIntoWeeks;

            } else {
                const startingLength = this.shiftsDividedIntoWeeks.length;

                for (let i = 0; i < shiftsDividedIntoWeeks.length; i++) { //    append new weeks onto previous shift array
                    this.shiftsDividedIntoWeeks[startingLength + i] = shiftsDividedIntoWeeks[i];
                }

            }

            this.shiftTimeline().rebuild(this.shiftsDividedIntoWeeks[this.weekOffset], this.startingTimestamp);

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

            let beginningOfWorkWeek = (new Date().setHours(0, 0, 0, 0)) - ((currentDayOfWeek) * oneDayInMs) - (this.weekOffset * oneWeekInMs);

            const newTimezoneOffset = new Date(beginningOfWorkWeek).getTimezoneOffset();

            const totalTimezoneOffset = Math.abs(timezoneOffset - newTimezoneOffset) / 60;

            if (timezoneOffset > newTimezoneOffset) { //    add or subtract hours based on UTC Offset changes.
                beginningOfWorkWeek -= (oneHourInMs * totalTimezoneOffset);
            } else if (timezoneOffset < newTimezoneOffset) {
                beginningOfWorkWeek += (oneHourInMs * totalTimezoneOffset);
            }

            this.startingTimestamp = beginningOfWorkWeek;

            console.log(new Date(beginningOfWorkWeek));

            return beginningOfWorkWeek;
        };

        getShifts = () => {

            const promise = new Promise((resolve, reject) => {

                $.ajax({
                    url: shiftUrl + '?page=' + this.pageNum + '&per_page=50&employee=' + this.empId,
                    type: 'GET',
                    success: (data) => {
                        this.totalPages = data.totalPages;
                        resolve(data.shifts);
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

            if ((this.pageNum === this.totalPages) && (this.weekOffset === this.shiftsDividedIntoWeeks.length - 1)) { //    if  
                $('#prev-week-button').hide();
            } else {
                $('#prev-week-button').show();
            }

        };

        this.init();

    };

    $.fn.TimelineShifts = TimelineShifts;
});
