$(() => {
    const TimelineShifts = function () {

        // const __this = this;
        const shiftUrl = '/timeclock/shifts';
        const oneHourInMs = 3600000;
        const oneDayInMs = 86400000;
        const oneWeekInMs = 604800000;

        // this.currentWeek = 0;
        this.shifts = ko.observableArray();
        this.startingTimestamp = ko.observable();
        this.pageNum = ko.observable();
        this.totalPages = ko.observable();
        this.empId = ko.observable();
        this.weekOffset = 0;
        this.shiftTimeline = ko.observable();

        const ShiftTimeline = $.fn.ShiftTimeline;

        this.init = (consts) => {

            this.shiftTimeline(new ShiftTimeline());

            this.pageNum = 1;

            consts = consts || {};
        };

        this.reload = function (empId) {

            this.empId = empId;

            processShifts = (rawShifts) => {

                this.FormatShifts(rawShifts);

                this.updateLabels();

            };

            handleError = (error) => {
                console.log(error);
            };

            this.getShifts(empId).then(processShifts, handleError);

        }.bind(this);


        this.nextWeek = function () {

            this.weekOffset -= 1;

            this.startingTimestamp = this.IncrementTimestampByWeek(this.startingTimestamp);

            this.shiftTimeline().rebuild(this.shifts[this.weekOffset], this.startingTimestamp);

            this.updateLabels();

        }.bind(this);

        this.prevWeek = function () {

            this.weekOffset += 1;
            this.startingTimestamp = this.DecrementTimestampByWeek(this.startingTimestamp);

            if (this.weekOffset === this.shifts.length) {
                this.getNextPageOfShifts();
            } else {

                this.shiftTimeline().rebuild(this.shifts[this.weekOffset], this.startingTimestamp);

            }

            this.updateLabels();

        }.bind(this);

        this.rebuild = (consts) => {

        };


        this.FormatShifts = (rawShifts) => {

            let weeks = [];

            let shiftsInWeek = [];

            let startingTimestamp = this.CalculateStartingTime();

            let weekStartingTime = startingTimestamp;

            const timeOfLastLoggedShift = new Date(rawShifts[0]['time_in']).getTime();

            while (startingTimestamp > timeOfLastLoggedShift) {
                weeks.push([]);
                startingTimestamp = startingTimestamp - oneWeekInMs;
            }

            startingTimestamp = startingTimestamp / 1000;

            let endingTimestamp = startingTimestamp + ((oneDayInMs - 100) / 1000) * 7;

            for (let i = 0; i < rawShifts.length; i++) {

                let shiftTimestamp = new Date(rawShifts[i]['time_in']).getTime() / 1000;

                if (shiftTimestamp < endingTimestamp && shiftTimestamp > startingTimestamp) {
                    shiftsInWeek.push(rawShifts[i]);


                } else if (shiftTimestamp < startingTimestamp) {
                    startingTimestamp -= (oneWeekInMs / 1000);
                    endingTimestamp -= (oneWeekInMs / 1000);
                    weeks.push(shiftsInWeek);

                    shiftsInWeek = [];
                    shiftsInWeek.push(rawShifts[i]);
                }

            }

            weeks.push(shiftsInWeek);

            for (let i = 0; i < weeks.length; i++) {
                weeks[i] = this.BreakIntoDays(weeks[i]);
            }

            if (this.shifts.length === 0) {
                this.shifts = weeks;
            } else {
                let startingLength = this.shifts.length;
                for (let i = 0; i < weeks.length; i++) {
                    this.shifts[startingLength + i] = weeks[i];
                }
            }

            this.shiftTimeline().rebuild(weeks[0], weekStartingTime);

            this.startingTimestamp = weekStartingTime;

        };

        this.DecrementTimestampByWeek = (timestamp) => {

            const timezoneOffset = new Date(timestamp).getTimezoneOffset();

            const newTimezoneOffset = new Date(timestamp - oneWeekInMs).getTimezoneOffset();

            if (timezoneOffset > newTimezoneOffset) {
                return timestamp - (oneWeekInMs + oneHourInMs);

            } else if (timezoneOffset < newTimezoneOffset) {
                return timestamp - (oneWeekInMs - oneHourInMs);
            }

            return timestamp - oneWeekInMs;

        };

        this.IncrementTimestampByWeek = (timestamp) => {

            const timezoneOffset = new Date(timestamp).getTimezoneOffset();

            const newTimezoneOffset = new Date(timestamp + oneWeekInMs).getTimezoneOffset();

            if (timezoneOffset > newTimezoneOffset) {
                return timestamp + (oneWeekInMs - oneHourInMs);

            } else if (timezoneOffset < newTimezoneOffset) {
                return timestamp + (oneWeekInMs + oneHourInMs);
            }

            return timestamp + oneWeekInMs;

        };

        this.BreakIntoDays = (weekOfShifts) => {

            let days = [];

            for (let i = 0; i < 7; i++) {
                days[i] = [];
            }

            let shiftDay;


            for (let i = 0; i < weekOfShifts.length; i++) {
                shiftDay = new Date(weekOfShifts[i]['time_out']).getDay();
                days[shiftDay].push(weekOfShifts[i]);
            }

            return days;
        };

        this.CalculateStartingTime = () => {

            const currentDayOfWeek = new Date().getDay();

            let timezoneOffset = new Date().getTimezoneOffset();

            let beginningOfWorkWeek = (new Date().setHours(0, 0, 0, 0)) - ((currentDayOfWeek) * oneDayInMs) - (this.weekOffset * oneWeekInMs);

            let newTimezoneOffset = new Date(beginningOfWorkWeek).getTimezoneOffset();

            if (timezoneOffset > newTimezoneOffset) {
                beginningOfWorkWeek -= (60000);
            } else if (timezoneOffset < newTimezoneOffset) {
                beginningOfWorkWeek += 3600000;

            }

            return beginningOfWorkWeek;
        };

        this.getShifts = () => {

            const promise = new Promise((resolve, reject) => {

                $.ajax({
                    url: shiftUrl + '?page=' + this.pageNum + '&per_page=1&employee=' + this.empId,
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

        this.getNextPageOfShifts = () => {

            processShifts = (rawShifts) => {

                this.FormatShifts(rawShifts);

                this.updateLabels();

            };

            handleError = (error) => {
                console.log(error);
            };

            this.pageNum += 1;

            this.getShifts().then(processShifts, handleError);

        };

        this.updateLabels = () => {

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

            const startingDate  = new Date(this.startingTimestamp);

            const endingDate = new Date(this.IncrementTimestampByWeek(this.startingTimestamp));
            
            const startingLabel = months[startingDate.getMonth()] + ', ' + startingDate.getDate();

            const endingLabel = months[endingDate.getMonth()] + ', ' + endingDate.getDate();

            $('#week-range-label').text(startingLabel + ' - ' + endingLabel);

            if (this.weekOffset === 0) {
                $('#next-week-button').hide();
            } else {
                $('#next-week-button').show();
            }

            if ((this.pageNum === this.totalPages) && (this.weekOffset === this.shifts.length - 1)) {
                $('#prev-week-button').hide();
            } else {
                $('#prev-week-button').show();
            }

        };

        this.init();

    };

    $.fn.TimelineShifts = TimelineShifts;
});