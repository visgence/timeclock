$(function() {

	var ManageShifts = function() {
		var ShiftList = $.fn.ShiftList;

		this.shiftList = ko.observable(new ShiftList());

		this.init = function() {
			this.shiftList().reload();
		}

		this.init();
	}	

	$.fn.ManageShifts = ManageShifts;
});