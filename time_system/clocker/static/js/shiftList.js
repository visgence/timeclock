$(() => {

    const ShiftList = function (consts) {

        const Shift = $.fn.Shift;

        this.shifts = ko.observableArray();

        this.init = function (consts) {
            consts = consts || {};

            if (consts.hasOwnProperty('per_page')) {
                per_page = consts.per_page;
            }

            this.rebuild(consts);
        }.bind(this);

        this.rebuild = function (shifts) {

            if (shifts.length > 0) {
                const newShifts = [];
                $.each(shifts, function () {
                    newShifts.push(new Shift(this));
                });

                this.shifts(newShifts);
            } else {
                this.shifts([]); // wipes previous shifts if there are no new ones.
            }

        }.bind(this);

    };

    $.fn.ShiftList = ShiftList;
});
