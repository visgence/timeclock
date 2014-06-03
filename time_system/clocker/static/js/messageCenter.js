$(function() {
    "use strict";

    var MessageCenter = function(vars) {
            
        this.errors = ko.observableArray();
        this.error = ko.observable();
        this.success = ko.observable();
        this.warning = ko.observable();

        //Optional buttons to display in the warning message
        this.warningButtons = ko.observableArray();

        //Determines if all messages should be cleared when any particular message is set.
        var dismissOnSet = true;

        this.hasSuccess = ko.computed(function() {
            return this.success() ? true : false;
        }.bind(this));

        this.hasWarnings = ko.computed(function() {
            return this.warning() ? true : false;
        }.bind(this));

        this.hasErrors = ko.computed(function() {
            var hasErrors = false;
            if(this.errors() && this.errors().length > 0) hasErrors = true;
            if(this.error()) hasErrors = true;
            return hasErrors
        }, this);

        
        this.init = function(vars) {
            vars = vars || {};
            if(vars.hasOwnProperty('dismissOnSet') && typeof(vars.dismissOnSet) === 'boolean')
                dismissOnSet = vars.dismissOnSet;

        }.bind(this);


       
        /** Sets the error messages appropriately based on the format the errorData is given.
         *
         *  If the format of the errorData is not recognized then a generic error message is given.
         *  'Something unexpected occured.'
         *  
         *  errorData can match the following formats:
         *      errorData = <String error>
         *          or
         *      errorData = {
         *          errors: <String error>
         *            or
         *          errors: [
         *              <String errors>
         *                  and/or
         *              {
         *                  <key>: <String Error>,
         *                      and/or
         *                  <key>: <Array of string errors>
         *              }
         *          ]
         *      }
         *
         *      EX: 
         *          errorData = {
         *              "errors": [
         *                  "Invalid credentials",
         *                  {
         *                      "password": ["Passwords do not match", "Invalid characters"],
         *                      "username": "Please provide a username"
         *                  }
         *              ]
         *          }
         *
         *          This will result in errors being set to the following:
         *              [
         *                  "Invalid credentials", 
         *                  "password - Passwords do not match",
         *                  "password - Invalid characters",
         *                  "username - Please provide a username"
         *              ]
         *
         */ 
        this.setErrors = function(errorData) {

            if(dismissOnSet)
                this.dismissMessages();

            if(errorData.hasOwnProperty('errors')) {
                var errors = errorData.errors;
                if(errors.length >= 0) {
                    if(errors.length == 1 && typeof(errors[0]) === 'string')
                        this.error(errors[0]);
                    else {
                        var newErrors = [];
                        $.each(errors, function(i, error) {
                           
                            //Just push if it's a string. Else we need to process a list of error strings.
                            if(typeof(error) === 'string')
                                newErrors.push(error);
                            else if(typeof(error) === 'object') {
                                var errorKeys = $.map(error, function(val, key) { return key; });
                                $.each(errorKeys, function(i, key) {

                                    if(typeof(error[key]) === 'string')
                                        newErrors.push(key + ' - ' + error[key]);
                                    else {
                                        $.each(error[key], function(i, errorString) {
                                            newErrors.push(key + ' - ' + errorString);
                                        });
                                    }
                                });
                            }
                        });
                        this.errors(newErrors);
                        this.error("Please fix the following errors.");
                    }
                }
                else
                    this.error('Something unexpected occured.');
            }
            else if(typeof(errorData) === 'string')
                this.error(errorData);
            else
                this.error('Something unexpected occured.');
        }.bind(this);

        this.setWarning = function(msg, buttons) {
            if(dismissOnSet)
                this.dismissMessages();

            this.warning(msg); 

            if($.isPlainObject(buttons))
                this.warningButtons.push(buttons);
            else if($.isArray(buttons)) {
                var btns = [];
                $.each(buttons, function(i, btn) {
                    //Handle this checking a little bit better
                    if(!btn instanceof Object)
                        throw("Buttons must be objects!");
                    else
                        btns.push(btn); 
                });
                this.warningButtons(btns); 
            }
        }.bind(this);
        
        this.setSuccess = function(msg) {
            if(dismissOnSet)
                this.dismissMessages();
            
            this.success(msg); 
        }.bind(this);

        this.dismissMessages = function() {
            this.dismissSuccess();
            this.dismissWarnings();
            this.dismissErrors();
        }.bind(this);

        this.dismissWarnings = function() {
            this.warning('');
            this.warningButtons([]);
        }.bind(this);
        
        this.dismissSuccess = function() {
            this.success('');
        }.bind(this);
        
        this.dismissErrors = function() {
            this.error('');
            this.errors([]);
        }.bind(this);


        //Returns the appropriate bootstrap button style. Defaults to btn-default unless the btn has a style declared.
        this.buttonStyle = function(btn) {
            return (btn && btn.hasOwnProperty('style')) ? "btn-"+btn.style : "btn-default";
        }.bind(this);

        //If any added button in any message is clicked it should call this.  If the button
        //has some specific callable then that is called first then all messages are dismissed which is default
        //behavior.
        this.buttonAction = function(btn) {
            this.dismissMessages();
            
            //TODO: make sure this is done safely and properly
            if(btn.hasOwnProperty('action'))
                btn.action();
        }.bind(this);

        this.init(vars);
    };

    $.fn.MessageCenter = MessageCenter;
});
