$(function() {

	var ManageShifts = function() {
		var ShiftList = $.fn.ShiftList;

		this.shiftList = ko.observable();

		this.init = function() {

			var startingPage = 1;
			var shiftListData = {
				'per_page': 25
			};

			this.shiftList(new ShiftList(shiftListData));
			this.shiftList().reload(startingPage);
		}

		this.init();
	}	

	$.fn.ManageShifts = ManageShifts;
});