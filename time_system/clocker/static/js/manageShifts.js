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

			//setInputBindings();
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

			$('.date-input').bootstrapDP({
		         'autoclose': true
		        ,'orientation': 'top'
		        ,'format': 'yyyy-mm-dd'
			}).on('hide', function(e) {
				$(e.target).trigger('input');
			});

			$('.time-input').timepicker({
				 'showMeridian': false	
				,'showSeconds': true
				,'defaultTime': false
				,'minuteStep': 1
			})
			.on("show.timepicker", function(e){
				$(e.target).val(e.time.value);
			})
			.on("changeTime.timepicker", function(e) {
				if (e.time.value === "")
					$(e.target).val("0:00:00");
				else
					$(e.target).val(e.time.value);
			}).val("");
		}

		this.init();
	}	

	$.fn.ManageShifts = ManageShifts;
});