$(function() {
    $('#statusBtn').button().click(function() {
        console.log('submitting form');
        console.log($(this).parent('form.clocker-form'));
        $(this).closest('form.clocker-form').submit();
    });
    
    $( "#from" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 1,
        dateFormat: 'yy-mm-dd',
        onClose: function( selectedDate ) {
            $( "#to" ).datepicker( "option", "minDate", selectedDate );
        }
    });
    $( "#to" ).datepicker({
        efaultDate: "+1w",
        hangeMonth: true,
        numberOfMonths: 1,
        dateFormat: 'yy-mm-dd',
        onClose: function( selectedDate ) {
            $( "#from" ).datepicker( "option", "maxDate", selectedDate );
        }
    });


    $( "#from-job" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 1,
        dateFormat: 'yy-mm-dd',
        onClose: function( selectedDate ) {
            $( "#to-job" ).datepicker( "option", "minDate", selectedDate );
        }
    });
    $( "#to-job" ).datepicker({
        efaultDate: "+1w",
        hangeMonth: true,
        numberOfMonths: 1,
        dateFormat: 'yy-mm-dd',
        onClose: function( selectedDate ) {
            $( "#from-job" ).datepicker( "option", "maxDate", selectedDate );
        }
    });
});
