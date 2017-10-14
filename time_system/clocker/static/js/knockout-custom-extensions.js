$(() => {
    ko.extenders.required = function (target, overrideMessage) {
        if (!target.hasOwnProperty('hasError')) {
            target.hasError = ko.observable();
        }
        if (!target.hasOwnProperty('validationMessage')) {
            target.validationMessage = ko.observable();
        }

        target.validate = function () {
            let value = target();
            if (typeof(value) === 'string') {
                value = value.trim();
            }

            let error = false;
            if ($.isArray(value)) {
                error = value.length > 0 ? false : true;
            } else {
                error = value ? false : true;
            }
            target.hasError(error);
            target.validationMessage(error ? overrideMessage || '' : '');

            // Return inverse to say whether or not validation succeeded or failed for target
            return !target.hasError();
        };

        return target;
    };
});
