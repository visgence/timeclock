$(() => {
    'use strict';

    const ManageShifts = function (vars) {
        const __this = this;
        const ShiftList = $.fn.ShiftList;
        const employeeUrl = '/timeclock/employees/';

        const startingPage = 1;
        const shiftListData = {
            per_page: 25,
        };

        this.shiftList = ko.observable();
        this.employees = ko.observableArray();
        this.managingEmployee = ko.observable();

        this.employee = ko.observable();
        this.selectedEmployee = ko.computed({
            read: function () {
                return this.employee();
            },
            write: function (emp) {
                updateHash({emp: emp.id});
            },
        }, this);

        this.managingSelf = ko.computed(function() { //eslint-disable-line
            const selectedEmp = this.selectedEmployee();
            const managingEmp = this.managingEmployee();
            let managing = false;

            if (selectedEmp && managingEmp && selectedEmp.id === managingEmp.id) {
                managing = true;
            }
            return managing;
        }.bind(this));

        this.init = function (vars) {
            vars = vars || {};

            if (vars.hasOwnProperty('managingEmployee')) {
                this.managingEmployee(vars.managingEmployee);
            }
            this.shiftList(new ShiftList(shiftListData));

            // TODO: this will change once I get more time to do something more proper
            $(window).on('shift-updated', () => {
                __this.shiftList().reload(__this.shiftList().currentPage(), __this.selectedEmployee().id);
            });

            $(window).on('hashchange', hashchangeHandler);
            return loadEmployees().then(() => {
                $(window).trigger('hashchange');
            });
            // setInputBindings();
        };

        const hashchangeHandler = function (e) {
            const state = getHash();
            if (state.hasOwnProperty('emp')) {
                const empId = parseInt(state.emp);
                $.each(__this.employees(), (i, emp) => {
                    if (empId === emp.id) {
                        __this.employee(emp);
                        __this.shiftList().reload(startingPage, emp.id);
                        return false;
                    }
                });
            }
        }.bind(this);

        // Checks if the shift table should add a blank row to seperate groups of shifts by day
        this.shouldAddSeperator = function (index, nextIndex) {

            if (index >= this.shiftList().shifts().length || nextIndex >= this.shiftList().shifts().length) {
                return false;
            }
            const currentDate = new Date(this.shiftList().shifts()[index].time_in());
            const nextDate = new Date(this.shiftList().shifts()[nextIndex].time_in());

            if (currentDate.getDate() !== nextDate.getDate()) {
                return true;
            }
            return false;
        }.bind(this);


        function loadEmployees() {
            const state = getHash();
            // If we see that there is no preset employee hash we will default to the current user.
            let setUser = false;
            if (!state.hasOwnProperty('emp')) {
                setUser = true;
            }
            return $.get(employeeUrl, (resp) => {
                $.each(resp.employees, (i, emp) => {
                    __this.employees.push(emp);
                    if (setUser && emp.id === __this.managingEmployee().id) {
                        __this.selectedEmployee(emp);
                    }
                });
            });
        };

        function setInputBindings() { //eslint-disable-line
            $('input.icon-input').on('input', () => {
                const currentVal = $(this).val();
                if (currentVal === '' && !$(this).is(':focus')) {
                    $(this).removeClass('icon-input-hide');
                } else {
                    $(this).addClass('icon-input-hide');
                }
            })
                .focus(() => {
                    $(this).addClass('icon-input-hide');
                })
                .focusout(() => {
                    if ($(this).val() === '') {
                        $(this).removeClass('icon-input-hide');
                    }
                }).trigger('input');

            $('.date-input').bootstrapDP({
                autoclose: true,
                orientation: 'top',
                format: 'yyyy-mm-dd',
            }).on('hide', (e) => {
                $(e.target).trigger('input');
            });

            $('.time-input').timepicker({
                showMeridian: false,
                showSeconds: true,
                defaultTime: false,
                minuteStep: 1,
            })
                .on('show.timepicker', (e) => {
                    $(e.target).val(e.time.value);
                })
                .on('changeTime.timepicker', (e) => {
                    if (e.time.value === '') {
                        $(e.target).val('0:00:00');
                    } else {
                        $(e.target).val(e.time.value);
                    }
                }).val('');
        }
    };
    $.fn.ManageShifts = ManageShifts;
});
