$(function() {
    $('#statusBtn').button().click(function() {
        console.log('submitting form');
        console.log($(this).parent('form.clocker-form'));
        $(this).closest('form.clocker-form').submit();
    });


    $("#from").bootstrapDP({
        'autoclose': true
        ,'orientation': 'top'
        ,'endDate': new Date()
        ,'format': 'yyyy-mm-dd'
    })
    .on('changeDate', function(ev) {
        $('#to').bootstrapDP('setStartDate', ev.date);    
    });

    $("#to").bootstrapDP({
        'autoclose': true
        ,'orientation': 'top'
        ,'endDate': new Date()
        ,'format': 'yyyy-mm-dd'
    })
    .on('changeDate', function(ev) {
        $('#from').bootstrapDP('setEndDate', ev.date);    
    });


    $("#from-job").bootstrapDP({
        'autoclose': true
        ,'orientation': 'top'
        ,'endDate': new Date()
        ,'format': 'yyyy-mm-dd'
    })
    .on('changeDate', function(ev) {
        $('#to-job').bootstrapDP('setStartDate', ev.date);    
    });

    $("#to-job").bootstrapDP({
        'autoclose': true
        ,'orientation': 'top'
        ,'endDate': new Date()
        ,'format': 'yyyy-mm-dd'
    })
    .on('changeDate', function(ev) {
        $('#from-job').bootstrapDP('setEndDate', ev.date);    
    });
});
