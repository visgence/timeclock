$(() => {
    const TimelineShifts = function () {

        const __this = this;
        const shiftUrl = '/timeclock/shifts';
        const oneDayInMs = 86400000;
        const oneWeekInMs = 604800000;
        // this.totalPages = ko.observable();
        // this.currentPage = ko.observable();
        this.currentWeek = 0;
        // this.earliestShiftHour = ko.observable();
        // this.latestShiftHour = ko.observable();
        this.shifts = ko.observableArray();
        this.startingTime = ko.observable();
        this.pageNum = ko.observable()
        this.weekOffset = ko.observable();
        this.shiftTimeline = ko.observable();

        const ShiftTimeline = $.fn.ShiftTimeline;

        this.init = (consts) => {

            this.shiftTimeline(new ShiftTimeline());

            // console.log(this.shiftTimeline);

            // return;


            consts = consts || {};

            if (consts.hasOwnProperty('pageNum')) {
                this.pageNum(consts.pageNum);
            } else {
                this.pageNum(0);
            }

            // this.rebuild(this.consts);
            processShifts = (rawShifts) => {
              

              this.FormatShifts(rawShifts);

              console.log(this.shifts, this.startingTime);

              

            };

            handleError = (error) => {
                console.log(error);
            };

            this.getShifts().then(processShifts, handleError);


            // shiftsDividedByWeek = FormatShifts(rawShifts);

            // this.weekOfShifts = BreakIntoDays(this.shiftsDividedByWeek[currentWeek]);

        };


        this.nextWeek = function () {
            
            this.weekOffset -= 1;

            this.startingTime += oneWeekInMs;

            this.shiftTimeline().rebuild(this.shifts[this.weekOffset], this.startingTime);

        }.bind(this);

        this.prevWeek = function () {

            this.weekOffset += 1;

            this.startingTime -= oneWeekInMs;

            this.shiftTimeline().rebuild(this.shifts[this.weekOffset], this.startingTime);

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

            // console.log(new Date(endingTimestamp * 1000));

            for (let i = 0; i < rawShifts.length; i++) {

                let shiftTimestamp = new Date(rawShifts[i]['time_in']).getTime() / 1000;

                if (shiftTimestamp < endingTimestamp && shiftTimestamp > startingTimestamp) {
                    shiftsInWeek.push(rawShifts[i]);

   
                } else if (shiftTimestamp < startingTimestamp) {
                    weeks.push(shiftsInWeek);
                    shiftsInWeek = [];
                    shiftsInWeek.push(rawShifts[i]);
                    startingTimestamp -= (oneWeekInMs / 1000);
                    endingTimestamp -= (oneWeekInMs / 1000);
                }

            }

            weeks.push(shiftsInWeek);

            for (let i = 0; i < weeks.length; i ++) {
                weeks[i] = this.BreakIntoDays(weeks[i]);                
            }

            this.shiftTimeline().build(weeks[0], weekStartingTime);

            this.shifts = weeks;

            this.startingTime = weekStartingTime;

            this.weekOffset = 0;

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

            const currentDayOfWeek = new Date().getDay()

            let timezoneOffset = new Date().getTimezoneOffset();

            let beginningOfWorkWeek = (new Date().setHours(0, 0, 0, 0)) - ((currentDayOfWeek) * oneDayInMs) - (this.currentWeek * oneWeekInMs);

            let newTimezoneOffset = new Date(beginningOfWorkWeek).getTimezoneOffset();

            if (timezoneOffset > newTimezoneOffset) {
                beginningOfWorkWeek -= (60000);
            } else if (timezoneOffset < newTimezoneOffset) {
                beginningOfWorkWeek += 3600000;

            }

            return beginningOfWorkWeek
        };

        this.getShifts = () => {

            let state = getHash();

            // if (state.hasOwnProperty('emp')) {

                // empId = parseInt(state.emp);

                let promise = new Promise((resolve, reject) => {

                    $.ajax({
                        url: shiftUrl + "?page=" + this.pageNum + "&per_page=50&employee=" + 1,
                        type: 'GET',
                        success: (data) => {
                            resolve(data.shifts);
                        },
                        error: (error) => {
                            reject(error);
                        },

                    });

                });
                return promise;

            // }

        };

        this.init();


    };


    $.fn.TimelineShifts = TimelineShifts;
});
