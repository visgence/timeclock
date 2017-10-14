$(() => {

    $('#statusBtn').button().click(() => {
        console.log('submitting form');
        console.log($(this).parent('form.clocker-form'));
        $(this).closest('form.clocker-form').submit();
    });


    $('#from').datetimepicker({
        format: 'YYYY-MM-DD',
    })
        .on('dp.change', (ev) => {
            $('#to').data('DateTimePicker').minDate(ev.date);
        });

    $('#to').datetimepicker({
        format: 'YYYY-MM-DD',
    })
        .on('dp.change', (ev) => {
            $('#from').data('DateTimePicker').maxDate(ev.date);
        });


    $('#from-job').datetimepicker({
        // endDate: new Date(),
        format: 'YYYY-MM-DD',
    })
        .on('dp.change', (ev) => {
            $('#to-job').data('DateTimePicker').minDate(ev.date);
        });

    $('#to-job').datetimepicker({
        // endDate: new Date(),
        format: 'YYYY-MM-DD',
    })
        .on('dp.change', (ev) => {
            $('#from-job').data('DateTimePicker').maxDate(ev.date);
        });
});
