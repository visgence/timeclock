$(function() {
    $('#statusBtn').button().click(function() {
        console.log('submitting form');
        console.log($(this).parent('form.clocker-form'));
        $(this).closest('form.clocker-form').submit();
    });


    $("#from").datepicker({
        'autoclose': true
        ,'orientation': 'top'
        ,'endDate': new Date()
        ,'format': 'yyyy-mm-dd'
    })
    .on('changeDate', function(ev) {
        $('#to').datepicker('setStartDate', ev.date);    
    });

    $("#to").datepicker({
        'autoclose': true
        ,'orientation': 'top'
        ,'endDate': new Date()
        ,'format': 'yyyy-mm-dd'
    })
    .on('changeDate', function(ev) {
        $('#from').datepicker('setEndDate', ev.date);    
    });


    $("#from-job").datepicker({
        'autoclose': true
        ,'orientation': 'top'
        ,'endDate': new Date()
        ,'format': 'yyyy-mm-dd'
    })
    .on('changeDate', function(ev) {
        $('#to-job').datepicker('setStartDate', ev.date);    
    });

    $("#to-job").datepicker({
        'autoclose': true
        ,'orientation': 'top'
        ,'endDate': new Date()
        ,'format': 'yyyy-mm-dd'
    })
    .on('changeDate', function(ev) {
        $('#from-job').datepicker('setEndDate', ev.date);    
    });
});
