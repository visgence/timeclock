$(function() {

	var Shift = function(vars) {
		
		this.id = ko.observable();
		this.time_in = ko.observable();
		this.time_out = ko.observable();
		this.hours = ko.observable();

		this.init = function(vars) {
			vars = vars || {};

			if (vars.hasOwnProperty('id'))
				this.id(vars.id);
			if (vars.hasOwnProperty('time_in'))
				this.time_in(vars.time_in);
			if (vars.hasOwnProperty('time_out'))
				this.time_out(vars.time_out);
			if (vars.hasOwnProperty('hours'))
				this.hours(vars.hours);

		}.bind(this);

		this.summary = function() {
			window.location = "/timeclock/summary/" + this.id();
		}.bind(this);

		this.init(vars);
	}

	$.fn.Shift = Shift;
})