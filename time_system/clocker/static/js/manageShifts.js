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

			setInputBindings();
		}

		function setInputBindings() {
			$('input.icon-input').on('input', function() {
				var currentVal = $(this).val();
				if (currentVal === "" && !$(this).is(':focus'))
					$(this).removeClass('icon-input-hide');	
				else
					$(this).addClass('icon-input-hide');	
			})
			.focus(function() { $(this).addClass('icon-input-hide'); })
			.focusout(function() { 
				if ($(this).val() === "")
					$(this).removeClass('icon-input-hide'); 
			}).trigger('input');
		}

		this.init();
	}	

	$.fn.ManageShifts = ManageShifts;
});