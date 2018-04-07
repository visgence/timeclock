// import './main.scss';

$(() => {

    const ShiftTimeline = function (lets) {

        const __this = this;
        const shiftUrl = '/timeclock/shifts';
        const oneDayInMs = 86400000;

        this.init = function () {
            GetTimelineData();
        };

        function GetTimelineData() {

            processRawShifts = (rawShifts) => {

                const WeekOfShifts = FormatShifts(rawShifts);

                BuildTimelineData(WeekOfShifts);
            };

            handleError = (error) => {
                alert(error);
            };

            GetShifts().then(processRawShifts, handleError);

        }

        function BuildTimelineData(WeekOfShifts) {

            const dateLabels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

            let timelineData = [];

            const startingTime = CalculateStartingTime();

            for (let day = 0; day < 7; day++) {

                times = []

                const date = new Date(startingTime + (day * oneDayInMs));

                if (WeekOfShifts[day]) {
                    let start_epoch;
                    let end_epoch;

                    for (let shift = 0; shift < WeekOfShifts[day].length; shift++) {

                        if (shift % 2 === 0) {
                            shiftColor = 'gray';
                        } else {
                            shiftColor = 'LightGray';
                        }

                        start_epoch = new Date(WeekOfShifts[day][shift]['time_in']);

                        if (WeekOfShifts[day][shift]['time_out']) {
                            end_epoch = new Date(WeekOfShifts[day][shift]['time_out']);
                        } else {
                            end_epoch = new Date();
                        }

                        times.push({
                            'starting_time': NormalizeTimestampToSameDay(start_epoch, day),
                            'ending_time': NormalizeTimestampToSameDay(end_epoch, day),
                            'shift_id': WeekOfShifts[day][shift]['id'],
                            'color': shiftColor
                        });

                    }
                }

                timelineData.push({
                    label: dateLabels[day] + ' (' + (date.getMonth() + 1) + '/' + (date.getDay() + 1) + ')',
                    times: times,
                });

            }

            DrawTimelineGraph(timelineData);

        }

        function DrawTimelineGraph(timelineData) {

            const oneDayInMs = 86400000;

            const startingTime = CalculateStartingTime();

            let endingTime = startingTime + oneDayInMs;

            const chart = d3.timelines()
                .stack()
                .margin({
                    left: 130,
                    right: 30,
                    top: 0,
                    bottom: 5
                }).tickFormat({
                    format: d3.timeFormat('%I:%M %p'),
                    tickSize: 5,
                })
                .showTimeAxisTick()
                .beginning(new Date(startingTime))
                .ending(new Date(endingTime))
                .click((d, i, datum) => {
                    window.location.href = 'http://timeclock.visgence.com/timeclock/summary/' + d['shift_id']
                });

            d3.select('#shift-timeline').append('svg').attr('width', $('#shift-timeline').innerWidth())
                .attr('height', $('#shift-timeline').innerHeight())
                .datum(timelineData)
                .call(chart);
        }

        function BreakIntoDays(WeekOfShifts) {


            let days = [];

            for (let i = 0; i < 7; i++) {
                days[i] = [];
            }

            let shiftDay;


            for (let i = 0; i < WeekOfShifts.length; i++) {
                shiftDay = new Date(WeekOfShifts[i]['time_out']).getDay();
                days[shiftDay].push(WeekOfShifts[i]);
            }

            return days;
        }

        function GetShifts() {

            const WeekOfShifts = {
                "WeekOfShifts": [{
                        "deleted": false,
                        "hours": null,
                        "time_in": "04/06/2018 08:00:47",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": null,
                        "id": 18412
                    },
                    {
                        "deleted": false,
                        "hours": "4.05",
                        "time_in": "04/05/2018 13:54:16",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/05/2018 17:57:06",
                        "id": 18408
                    },
                    {
                        "deleted": false,
                        "hours": "3.75",
                        "time_in": "04/05/2018 08:15:01",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/05/2018 12:00:12",
                        "id": 18399
                    },
                    {
                        "deleted": false,
                        "hours": "0.83",
                        "time_in": "04/04/2018 18:55:42",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/04/2018 19:45:45",
                        "id": 18396
                    },
                    {
                        "deleted": false,
                        "hours": "0.34",
                        "time_in": "04/04/2018 18:24:24",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/04/2018 18:44:54",
                        "id": 18395
                    },
                    {
                        "deleted": false,
                        "hours": "3.02",
                        "time_in": "04/04/2018 14:09:23",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/04/2018 17:10:32",
                        "id": 18392
                    },
                    {
                        "deleted": false,
                        "hours": "2.24",
                        "time_in": "04/04/2018 11:54:40",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/04/2018 14:09:20",
                        "id": 18389
                    },
                    {
                        "deleted": false,
                        "hours": "3.70",
                        "time_in": "04/04/2018 08:12:46",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/04/2018 11:54:37",
                        "id": 18384
                    },
                    {
                        "deleted": false,
                        "hours": "1.15",
                        "time_in": "04/03/2018 16:14:05",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/03/2018 17:23:17",
                        "id": 18380
                    },
                    {
                        "deleted": false,
                        "hours": "6.87",
                        "time_in": "04/03/2018 09:22:00",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/03/2018 16:13:58",
                        "id": 18374
                    },
                    {
                        "deleted": false,
                        "hours": "1.13",
                        "time_in": "04/03/2018 08:14:10",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/03/2018 09:21:55",
                        "id": 18370
                    },
                    {
                        "deleted": false,
                        "hours": "1.00",
                        "time_in": "04/02/2018 16:00:46",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/02/2018 17:00:48",
                        "id": 18369
                    },
                    {
                        "deleted": false,
                        "hours": "1.00",
                        "time_in": "04/02/2018 08:00:38",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "04/02/2018 09:00:40",
                        "id": 18368
                    },
                    {
                        "deleted": false,
                        "hours": "2.56",
                        "time_in": "03/31/2018 13:30:12",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/31/2018 16:03:46",
                        "id": 18353
                    },
                    {
                        "deleted": false,
                        "hours": "0.88",
                        "time_in": "03/31/2018 09:35:19",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/31/2018 10:28:03",
                        "id": 18349
                    },
                    {
                        "deleted": false,
                        "hours": "4.50",
                        "time_in": "03/30/2018 07:57:47",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/30/2018 12:27:48",
                        "id": 18338
                    },
                    {
                        "deleted": false,
                        "hours": "5.27",
                        "time_in": "03/29/2018 12:00:15",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/29/2018 17:16:17",
                        "id": 18336
                    },
                    {
                        "deleted": false,
                        "hours": "3.01",
                        "time_in": "03/29/2018 08:25:56",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/29/2018 11:26:38",
                        "id": 18326
                    },
                    {
                        "deleted": false,
                        "hours": "3.08",
                        "time_in": "03/28/2018 14:05:47",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/28/2018 17:10:52",
                        "id": 18323
                    },
                    {
                        "deleted": false,
                        "hours": "4.41",
                        "time_in": "03/28/2018 08:13:55",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/28/2018 12:38:15",
                        "id": 18314
                    },
                    {
                        "deleted": false,
                        "hours": "1.12",
                        "time_in": "03/27/2018 15:55:16",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/27/2018 17:02:34",
                        "id": 18308
                    },
                    {
                        "deleted": false,
                        "hours": "6.58",
                        "time_in": "03/27/2018 09:20:10",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/27/2018 15:55:12",
                        "id": 18303
                    },
                    {
                        "deleted": false,
                        "hours": "1.14",
                        "time_in": "03/27/2018 08:10:00",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/27/2018 09:18:06",
                        "id": 18302
                    },
                    {
                        "deleted": false,
                        "hours": "1.16",
                        "time_in": "03/26/2018 15:55:41",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/26/2018 17:05:00",
                        "id": 18301
                    },
                    {
                        "deleted": false,
                        "hours": "0.97",
                        "time_in": "03/26/2018 14:57:14",
                        "employee": {
                            "username": "evan",
                            "first_name": "Evan",
                            "last_name": "Salazar",
                            "is_active": true,
                            "is_superuser": true,
                            "id": 5
                        },
                        "time_out": "03/26/2018 15:55:37",
                        "id": 18289
                    }
                ],
                "errors": [],
                "totalPages": 128,
                "page": 1
            }


            // return WeekOfShifts['WeekOfShifts']

            const state = getHash();

            if (state.hasOwnProperty('emp')) {

                const empId = parseInt(state.emp);

                const args = {
                    page: 1,
                    per_page: 50,
                    employee: empId,
                };

                let promise = new Promise((resolve, reject) => {

                    $.ajax({
                        url: shiftUrl,
                        type: 'GET',
                        args: args,
                        success: (data) => {
                            resolve(data.shifts);
                        },
                        error: (error) => {
                            reject(error);
                        }

                    });

                });

                return promise;

            }
        }

        function FormatShifts(rawShifts) {


            let shiftsInPreviousSevenDays = [];

            let startingTimestamp = CalculateStartingTime();

            startingTimestamp = startingTimestamp / 1000 //seconds

            let endingTimestamp = startingTimestamp + (oneDayInMs / 1000) * 7

            for (let i = 0; i < rawShifts.length; i++) {

                let shiftTimestamp = new Date(rawShifts[i]['time_in']).getTime() / 1000

                if (shiftTimestamp < endingTimestamp && shiftTimestamp > startingTimestamp) {
                    shiftsInPreviousSevenDays.push(rawShifts[i])

                }

            }

            let formattedShifts = BreakIntoDays(shiftsInPreviousSevenDays)

            return formattedShifts

        }

        function CalculateStartingTime() {

            const currentDayOfWeek = new Date().getDay()

            const beginningOfWorkWeek = (new Date().setHours(0, 0, 0, 0)) - (currentDayOfWeek * oneDayInMs);

            return beginningOfWorkWeek
        }

        function NormalizeTimestampToSameDay(timestamp, daysSinceInitial) {

            const normalizedTimestamp = (timestamp - (daysSinceInitial * oneDayInMs));

            return normalizedTimestamp
        }

        this.init();

    }

    $.fn.ShiftTimeline = ShiftTimeline;



});