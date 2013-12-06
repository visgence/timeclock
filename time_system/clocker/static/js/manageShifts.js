$(function() {
	"use strict";

	var ManageShifts = function(vars) {
		var __this = this;
		var ShiftList = $.fn.ShiftList;
		var employeeUrl = "/timeclock/employees/";

		this.shiftList = ko.observable();
		this.employees = ko.observableArray();
		this.selectedEmployee = ko.observable();
		this.managingEmployee = ko.observable();

		this.managingSelf = ko.computed(function() {
			var selectedEmp = this.selectedEmployee();
			var managingEmp = this.managingEmployee();
			var managing = false;

			if (selectedEmp && managingEmp && selectedEmp.id == managingEmp.id)		
				managing = true;

			return managing;
		}.bind(this));

		this.init = function(vars) {
			vars = vars || {};

			if (vars.hasOwnProperty('managingEmployee'))
				this.managingEmployee(vars.managingEmployee);

			var startingPage = 1;
			var shiftListData = {
				'per_page': 25
			};

			this.shiftList(new ShiftList(shiftListData));
			this.selectedEmployee.subscribe(function(employee) {
				__this.shiftList().reload(startingPage, employee.id);
			})

			loadEmployees();

			//TODO: this will change once I get more time to do something more proper
			$(window).on('shift-updated', function() {
				__this.shiftList().reload(__this.shiftList().currentPage(), __this.selectedEmployee().id);
			});

			//setInputBindings();
		}


		function loadEmployees() {
			$.get(employeeUrl, function(resp) {
				$.each(resp.employees, function(i, emp) {
					__this.employees.push(emp);	
					if (emp.id === __this.managingEmployee().id)
						__this.selectedEmployee(emp);
				});
			});
		};

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

		this.init(vars);
	}	

	$.fn.ManageShifts = ManageShifts;
});