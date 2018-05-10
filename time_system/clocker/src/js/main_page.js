$(() => {
    $('#statusBtn').button().click(() => {
        console.log('submitting form');
        console.log($(this).parent('form.clocker-form'));
        $(this).closest('form.clocker-form').submit();
    });


    $('#from').datepicker({
        autoclose: true,
        orientation: 'top',
        endDate: new Date(),
        format: 'yyyy-mm-dd',
    })
        .on('changeDate', (ev) => {
            $('#to').datepicker('setStartDate', ev.date);
        });

    $('#to').datepicker({
        autoclose: true,
        orientation: 'top',
        endDate: new Date(),
        format: 'yyyy-mm-dd',
    })
        .on('changeDate', (ev) => {
            $('#from').datepicker('setEndDate', ev.date);
        });


    $('#from-job').datepicker({
        autoclose: true,
        orientation: 'top',
        endDate: new Date(),
        format: 'yyyy-mm-dd',
    })
        .on('changeDate', (ev) => {
            $('#to-job').datepicker('setStartDate', ev.date);
        });

    $('#to-job').datepicker({
        autoclose: true,
        orientation: 'top',
        endDate: new Date(),
        format: 'yyyy-mm-dd',
    })
        .on('changeDate', (ev) => {
            $('#from-job').datepicker('setEndDate', ev.date);
        });
});
