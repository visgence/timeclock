$(() => {
    const ShiftTimeline = function () {

        /* timeline.js
        Author: Jacob Bakarich
        Date: May 7, 2018

        This function takes a formatted array of shifts divided into week and weekday, and graphs
        the shifts on a d3-timeline graph. Since d3-timeline will automatically extend graph axes to 
        all the earliest and latest timestamps, all shifts must be further formatted to occur on the 
        same day, to correctly display shifts from 12am -11:59pm for each day.

        Documentation for d3-timeline availible at https://github.com/jiahuang/d3-timeline

        */

        const oneDayInMs = 86400000;

        this.shifts = [];
        this.currentWorkWeekStartingTime = 0;
        this.weekOffset = 0;

        this.rebuild = (weekOfShifts, startingTime) => {

            RemovePreviousTimeline();

            BuildTimelineData(weekOfShifts, startingTime);

        };

        this.build = (weekOfShifts, startingTime) => {

            BuildTimelineData(weekOfShifts, startingTime);
        };

        function BuildTimelineData(weekOfShifts, startingTime) {

            //  function takes a week of shifts, assigns them a date label, and normalizes to occur on the same day

            const dateLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

            const timelineData = [];

            for (let day = 0; day < 7; day++) {

                times = [];

                const date = new Date(startingTime + (day * oneDayInMs));

                if (weekOfShifts[day]) {
                    let startEpoch;
                    let endEpoch;

                    for (let shift = 0; shift < weekOfShifts[day].length; shift++) {

                        if (shift % 2 === 0) {
                            shiftColor = 'gray';
                        } else {
                            shiftColor = 'LightGray';
                        }

                        startEpoch = new Date(weekOfShifts[day][shift]['time_in']);

                        if (weekOfShifts[day][shift]['time_out']) {
                            endEpoch = new Date(weekOfShifts[day][shift]['time_out']);
                        } else {
                            endEpoch = new Date();
                        }

                        times.push({
                            starting_time: NormalizeTimestampToSameDay(startEpoch, day),
                            ending_time: NormalizeTimestampToSameDay(endEpoch, day),
                            shift_id: weekOfShifts[day][shift]['id'],
                            color: shiftColor,
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

            const zoom = d3.zoom(); //  needed to disable d3-timelines from blocking native scrolling

            const chart = d3.timelines()
                .stack()
                .margin({
                    left: 140,
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


            const svg = d3.select('#shift-timeline');
            svg.append('svg').attr('width', $('#shift-timeline').innerWidth())
                .attr('height', $('#shift-timeline').innerHeight())
                .datum(timelineData)
                .call(chart)
                .call(zoom)
                .on('wheel.zoom', null); // prevent scroll events from being blocked
        }

        function NormalizeTimestampToSameDay(timestamp, daysSinceInitial) {

            const normalizedTimestamp = (timestamp - (daysSinceInitial * oneDayInMs));

            return normalizedTimestamp;
        }


        function RemovePreviousTimeline() {
            if ($('svg')) {
                $('svg').remove();
            }
        }


    };

    $.fn.ShiftTimeline = ShiftTimeline;
});
