// import './main.scss';

$(() => {

    const ShiftTimeline = function (vars) {

        const __this = this;
        const shiftUrl = '/timeclock/shifts';

        this.init = function () {
            DrawTimeline();
        };

        function DrawTimeline() {

            processRawShifts = (rawShifts) => {

                const shifts = formatShifts(rawShifts);

                buildTimelineData(shifts);

            };

            handleError = (error) => {
                alert(error);
            };

            getShifts().then(processRawShifts, handleError);

        }

        function buildTimelineData(shifts) {

            const dateLabels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

            const oneWeekInMs = 86400000;

            let timelineData = [];

            let startingTime = new Date().setHours(0, 0, 0, 0);

            let endingTime = startingTime + oneWeekInMs;

            var wat = startingTime;

            for (var day = 0; day < 8; day++) {

                times = []
                var currDay = new Date(wat).getDay()
                console.log(shifts);

                if (shifts[currDay]) {
                    for (var shift = 0; shift < shifts[currDay].length; shift++) {
                        var start_epoch = new Date(shifts[currDay][shift]['time_in']);
                        if (shifts[currDay][shift]['time_out']) {
                            var end_epoch = new Date(shifts[currDay][shift]['time_out']);
                        } else {
                            var end_epoch = new Date()
                        }
                        times.push({
                            "starting_time": (start_epoch - (day * -86400000)),
                            "ending_time": (end_epoch - (day * -86400000)),
                            "shift_id": shifts[currDay][shift]['id']
                        });
                    }
                }

                timelineData.push({
                    label: dateLabels[currDay],
                    times: times,
                });


                wat = wat - 86400000

            }

            drawTimeline(timelineData);

        }

        function DrawTimeline(timelineData) {

            console.log(timelineData);

            const oneWeekInMs = 86400000;

            let startingTime = new Date().setHours(0, 0, 0, 0)

            let endingTime = startingTime + oneWeekInMs;

            const chart = d3.timelines()
                .stack()
                .margin({
                    left: 80,
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
                .click(function (d, i, datum) {
                    window.location.href = "http://timeclock.visgence.com/timeclock/summary/" + d['shift_id']
                });

            d3.select('#shift-timeline').append("svg").attr("width", $('#shift-timeline').innerWidth())
                .attr("height", $('#shift-timeline').innerHeight())
                .datum(timelineData)
                .call(chart);
        }

        function breakIntoDays(shifts) {

            var days = [];

            var shiftDay;


            for (var i = 0; i < shifts.length; i++) {
                if (shifts[i]) {
                    shiftDay = new Date(shifts[i]['time_out']).getDay();
                    if (days[shiftDay]) {
                        days[shiftDay].push(shifts[i]);
                    } else {
                        days[shiftDay] = [shifts[i]];
                    }
                }
            }

            return days;
        }

        function getShifts() {

            const shifts = {
                "shifts": [{
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


            // return shifts['shifts']

            const state = getHash();

            if (state.hasOwnProperty('emp')) {

                const empId = parseInt(state.emp);

                const args = {
                    page: 1,
                    per_page: 50,
                    employee: empId,
                };

                var promise = new Promise((resolve, reject) => {

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

        function formatShifts(rawShifts) {


            var shiftsInPreviousSevenDays = [];

            var startingTimestamp = new Date()

            startingTimestamp.setHours(0, 0, 0, 0)

            startingTimestamp = startingTimestamp.getTime() / 1000 //seconds

            var endingTimestamp = startingTimestamp - 691200


            for (var i = 0; i < rawShifts.length; i++) {

                var shiftTimestamp = new Date(rawShifts[i]['time_in']).getTime() / 1000

                if (shiftTimestamp > endingTimestamp) {
                    shiftsInPreviousSevenDays.push(rawShifts[i])

                }

            }

            var formattedShifts = breakIntoDays(shiftsInPreviousSevenDays)

            return formattedShifts

        }

        function calculateStartingTime(shifts) {

            // for(var i = 0; i < shifts.length; i++){
            //     if(shifts[i]['time_out']){


            //     }
            // }

            console.log(shifts)


            return new Date(shifts[0]['time_in']).setHours(0, 0, 0, 0)
        }

        this.init();

    }

    $.fn.ShiftTimeline = ShiftTimeline;



});