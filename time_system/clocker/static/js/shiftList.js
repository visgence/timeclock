$(() => {

    const ShiftList = function (consts) {

        const Shift = $.fn.Shift;

        // let per_page = 25;

        this.shifts = ko.observableArray();

        this.currentPage = ko.observable();
        this.startingTimestamp = ko.observable();
        this.endingTimestamp = ko.observable();
        this.totalPages = ko.observable();
        this.pageNum = ko.computed(function() { //eslint-disable-line
            return this.currentPage() + ' of ' + this.totalPages() + ' pages';
        }.bind(this));


        this.init = function (consts) {
            consts = consts || {};

            if (consts.hasOwnProperty('per_page')) {
                per_page = consts.per_page;
            }

            this.rebuild(consts);
        }.bind(this);

        this.rebuild = function (shifts) {
            // consts = consts || {};

            // if (consts.hasOwnProperty('page')) {
            //     this.currentPage(consts.page);
            // }

            // if (consts.hasOwnProperty('totalPages')) {
            //     this.totalPages(consts.totalPages);
            // }


            if (shifts.length > 0) {
                const newShifts = [];
                $.each(shifts, function () {
                    newShifts.push(new Shift(this));
                });

                this.shifts(newShifts);
            }
        }.bind(this);

        this.nextPage = function () {
            this.reload(this.currentPage() + 1);
        }.bind(this);

        this.prevPage = function () {
            this.reload(this.currentPage() - 1);
        }.bind(this);

        this.firstPage = function () {
            this.reload(1);
        }.bind(this);

        this.lastPage = function () {
            this.reload(this.totalPages());
        }.bind(this);

        // this.reload = function (startingTimestamp, endingTimestamp, employee) {
        //     const __this = this;

        //     const startingTimestampInSeconds = startingTimestamp / 1000;

        //     const endingTimestampInSeconds = endingTimestamp / 1000;

        //     const args = {
        //         employee: employee,
        //         starting_timestamp: startingTimestampInSeconds,
        //         ending_timestamp: endingTimestampInSeconds,
        //     };

        //     const promise = $.get(shiftUrl, args)
        //         .done((resp) => {
        //             if (resp.hasOwnProperty('errors') && resp.errors.length > 0) {
        //                 console.error(resp.errors);
        //             } else if (resp.shifts) {
        //                 __this.rebuild(resp);
        //             } else {
        //                 console.error('Something unexpected happend!');
        //             }
        //         })
        //         .fail((resp) => {
        //             console.error(resp);
        //         });

        //     return promise;
        // }.bind(this);

        // this.init(consts);
    };

    $.fn.ShiftList = ShiftList;
});
