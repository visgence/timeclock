$(function() {

	var ShiftList = function(vars) {

		var Shift = $.fn.Shift;
		var shiftUrl = "/timeclock/shifts/"

		this.shifts = ko.observableArray();


		this.init = function(vars) {
			vars = vars || {};

			this.rebuild(vars);
		}.bind(this);

		this.rebuild = function(vars) {
			vars = vars || {};

			if (vars.hasOwnProperty('shifts')) {
				var newShifts = [];
				$.each(vars.shifts, function() {
					newShifts.push(new Shift(this));
				});

				this.shifts(newShifts);
			}
		}.bind(this);

		this.reload = function() {
			var __this = this;

			var promise = $.get(shiftUrl)
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