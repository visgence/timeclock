$(function() {

	var ShiftList = function(vars) {

		var Shift = $.fn.Shift;
		var shiftUrl = "/timeclock/shifts/"

		var per_page = 25;

		this.shifts = ko.observableArray();

        this.currentPage = ko.observable();
        this.totalPages = ko.observable();
        this.pageNum = ko.computed(function() {
            return this.currentPage() +" of "+ this.totalPages() +" pages";
        }.bind(this));



		this.init = function(vars) {
			vars = vars || {};

			var __this = this;

			if (vars.hasOwnProperty('per_page'))
				per_page = vars.per_page;

			this.rebuild(vars);
		}.bind(this);

		this.rebuild = function(vars) {
			vars = vars || {};

			if (vars.hasOwnProperty('page'))
				this.currentPage(vars.page);

			if (vars.hasOwnProperty('totalPages'))
				this.totalPages(vars.totalPages);

			if (vars.hasOwnProperty('shifts')) {
				var newShifts = [];
				$.each(vars.shifts, function() {
					newShifts.push(new Shift(this));
				});

				this.shifts(newShifts);
			}
		}.bind(this);

        this.nextPage = function() {
            this.reload(this.currentPage()+1);
        }.bind(this);

        this.prevPage = function() {
            this.reload(this.currentPage()-1);
        }.bind(this);

        this.firstPage = function() {
            this.reload(1);
        }.bind(this);

        this.lastPage = function() {
            this.reload(this.totalPages());
        }.bind(this);

		this.reload = function(page, employee) {
			var __this = this;

			var args = {
				 'page': page
				,'per_page': per_page
				,'employee': employee
			}

			var promise = $.get(shiftUrl, args)
			.done(function(resp) {
				if(resp.hasOwnProperty("errors") && resp.errors.length > 0)
					console.error(resp.errors);	
				else if(resp.shifts)
					__this.rebuild(resp);
				else
					console.error("Something unexpected happend!");	
			})
			.fail(function(resp) {
				console.error(resp);
			});

			return promise;
		}.bind(this);

		this.init(vars);
	}

	$.fn.ShiftList = ShiftList;
});