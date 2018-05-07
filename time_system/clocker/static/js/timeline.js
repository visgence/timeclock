// import './main.scss';
$(() => {
    const ShiftTimeline = function () {

        const __this = this;
        let empId = ''
        const shiftUrl = '/timeclock/shifts';
        const oneDayInMs = 86400000;
        const oneWeekInMs = 604800000;
        let isDrawingTimeline = false;

        // const TimelineShifts = $.fn.TimelineShifts;

        this.shifts = ko.observableArray();
        this.currentWorkWeekStartingTime = ko.observable();
        this.weekOffset = 0;
        // this.timelineShifts = ko.observable();

        this.init = function () {

            isDrawingTimeline = true;


        };

        this.rebuild = (weekOfShifts, startingTime) => {

            removePreviousTimeline();

            BuildTimelineData(weekOfShifts, startingTime);


        };

        this.build = (weekOfShifts, startingTime) => {

            BuildTimelineData(weekOfShifts, startingTime);
        };


        function BuildTimelineData(weekOfShifts, startingTime) {

            const dateLabels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

            let timelineData = [];


            for (let day = 0; day < 7; day++) {

                times = [];

                const date = new Date(startingTime + (day * oneDayInMs));

                // console.log(weekOfShifts);

                if (weekOfShifts[day]) {
                    let start_epoch;
                    let end_epoch;

                    for (let shift = 0; shift < weekOfShifts[day].length; shift++) {

                        if (shift % 2 === 0) {
                            shiftColor = 'gray';
                        } else {
                            shiftColor = 'LightGray';
                        }

                        start_epoch = new Date(weekOfShifts[day][shift]['time_in']);

                        if (weekOfShifts[day][shift]['time_out']) {
                            end_epoch = new Date(weekOfShifts[day][shift]['time_out']);
                        } else {
                            end_epoch = new Date();
                        }

                        times.push({
                            'starting_time': NormalizeTimestampToSameDay(start_epoch, day),
                            'ending_time': NormalizeTimestampToSameDay(end_epoch, day),
                            'shift_id': weekOfShifts[day][shift]['id'],
                            'color': shiftColor
                        });

                    }
                }

                timelineData.push({
                    label: dateLabels[day] + ' (' + (date.getMonth() + 1) + '/' + (date.getDate()) + ')',
                    times: times,
                });


            }

            DrawTimelineGraph(timelineData, startingTime);

        }

        function DrawTimelineGraph(timelineData, startingTime) {

            const endingTime = startingTime + oneDayInMs;

            const chart = d3.timelines()
                .stack()
                .margin({
                    left: 130,
                    right: 30,
                    top: 0,
                    bottom: 5,
                }).tickFormat({
                    format: d3.timeFormat('%I:%M %p'),
                    tickSize: 5,
                })
                .showTimeAxisTick()
                .beginning(new Date(startingTime))
                .ending(new Date(endingTime))
                .click((d, i, datum) => {
                    window.location.href = 'http://timeclock.visgence.com/timeclock/summary/' + d['shift_id'];
                });

            let svg = d3.select('#shift-timeline');
            svg.append('svg').attr('width', $('#shift-timeline').innerWidth())
                .attr('height', $('#shift-timeline').innerHeight())
                .datum(timelineData)
                .call(chart);

            isDrawingTimeline = false;
        }

        function NormalizeTimestampToSameDay(timestamp, daysSinceInitial) {

            const normalizedTimestamp = (timestamp - (daysSinceInitial * oneDayInMs));

            return normalizedTimestamp
        }

        function updateLabels(moreWeeks, prevWeeks) {
            if (!moreWeeks) {
                $('#next-week-button').hide();
            } else {
                $('#next-week-button').show();
            }

            if (!prevWeeks) {
                $('#prev-week-button').hide();
            } else {
                $('#prev-week-button').show();
            }

        }

        function removePreviousTimeline() {
            if ($('svg')) {
                $('svg').remove();
            }
        }

        this.init();

    };

    $.fn.ShiftTimeline = ShiftTimeline;
});