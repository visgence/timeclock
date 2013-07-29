$(function() {
    $('#statusBtn').button().click(function() {
        console.log('submitting form');
        console.log($(this).parent('form.clocker-form'));
        $(this).closest('form.clocker-form').submit();
    });
});
