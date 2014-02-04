
function show_progress(id, state) {
    if(state) {
        $(id).removeClass('hidden');
        $(id).addClass('make-visible');
        $(id).addClass('working');
    }
    else {
        $(id).removeClass('make-visible');
        $(id).removeClass('working');
        $(id).addClass('hidden');
    }

}
function validate_form(formid) {
    var validated = true;
    $(formid + ":input").each(function(){
        var input = $(this);
        if(!input.checkValidity()) {
            validated = false;
            input.css('border-color', '#E9322D');
            input.css('box-shadow', '0 0 6px #F8B9B7');
        }
    });
    return validated;
}


function setup_dbconfig_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $.each(json.errors, function (item, text) {
            if( item == 'reachability') {
                $('#test-connection-result').addClass('make-visible');
                $('#test-connection-result').removeClass('hidden');
                $('#test-connection-result').html('Fail');
            }
            else {
              $('#id_'+item).addClass('error-field');
            }
          }); //for each
        }
        else{
            $('#test-connection-result').addClass('make-visible');
            $('#test-connection-result').removeClass('hidden');
            $('#test-connection-result').html('OK');
            $('#create-schema').removeAttr('disabled');
        }//else
        show_progress('#test-connection-working', false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#test-connection-working', false); }
    };
    $('#dbconfig-form').ajaxForm(options);
}

function set_test_con_handler() {
    $('#test-connection').click(function(){
        show_progress('#test-connection-working', true);
        $('.error-field').each( function() { $(this).removeClass('error-field');} );
        $('#dbconfig-form').submit();
    });
}


function set_create_db_schema_handler() {
    $('#create-schema').click(function(){
        show_progress('#create-schema-working', true);
        params = {};
        var url = '/createschema/'
        $.post(url, params)
          .success(function(msg){
              show_progress(false);
              document.location.href = '/login/';
          })
          .error(function(xhr, textStatus, errorThrown){
                show_progress('#create-schema-working', false);
                $('#create-schema-result').addClass('make-visible');
                $('#create-schema-result').removeClass('hidden');
                $('#create-schema-result').html('Failed');
            });
    });
}

function setup_activate_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $.each(json.errors, function (item, text) {
              $('#id_'+item).addClass('error-field');
          }); //for each
        }
        else {
            show_progress("#activation-working", false);
            document.location.href = '/configure/';
        }
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#activation-working', false); }
    };
    $('#activate-form').ajaxForm(options);
}

function set_activation_handler() {
    $('#activate-next').click(function(){
        show_progress('#activation-working', true);
        $('#activate-form').submit();
        return false;
    });
}

function set_lb_show(ele, form) {
    $(ele).click(function(){
        $(form).css('display', 'block');
        $('#fade').css('display', 'block');
    });
}
function set_lb_hide(ele, form) {
    $(ele).click(function(){
        $(form).css('display', 'none');
        $('#fade').css('display', 'none');
    });
}


function set_dnsconfig_forms() {
    $('#ed_services').click(function() {
        $('#service_name').html('Services');
        current_url = '1';
        $('#serviceid').attr('value', current_url);
    });
    $('#ed_euportal').click(function() {
        $('#service_name').html('End User Portal');
        current_url = '2';
        $('#serviceid').attr('value', current_url);
    });
    $('#ed_portal').click(function() {
        $('#service_name').html('Portal');
        current_url = '3';
        $('#serviceid').attr('value', current_url);
    });
    $('#ed_enrollment').click(function() {
        $('#service_name').html('Enrollment');
        current_url = '4';
        $('#serviceid').attr('value', current_url);
    });
    set_lb_show('#ed_services', '#hform_services');
    set_lb_show('#ed_euportal', '#hform_services');
    set_lb_show('#ed_portal', '#hform_services');
    set_lb_show('#ed_enrollment', '#hform_services');
}
function set_dns_form_submit(){
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#dns-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#dns-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#dns-errors').html('');
        }
        show_progress("#dnsconfig-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#dnsconfig-working', false); }
    };
    $('#form-dnsconfig').ajaxForm(options);
    $('#dnssubmit').click(function(){
        if(validate_form("#form-dnsconfig")) {
            show_progress('#dnsconfig-working', true);
            $('#form-dnsconfig').submit();
        }
        return false;
    });
}

function set_admin_email_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#ademail-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#ademail-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#ademail-errors').html('');
        }
        show_progress("#adminemail-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#adminemail-working', false); }
    };
    $('#form-adminemail').ajaxForm(options);
    $('#adminemail-submit').click(function(){
        if(validate_form("#form-adminemail")) {
            show_progress('#adminemail-working', true);
            $('#form-adminemail').submit();
        }
        return false;
    });
}

function set_soln_name_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#slnname-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#slnname-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#slnname-errors').html('');
        }
        show_progress("#soln-name-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#soln-name-working', false); }
    };
    $('#form-soln-name').ajaxForm(options);
    $('#soln-name-submit').click(function(){
        if(validate_form("#form-soln-name")) {
            show_progress('#soln-name-working', true);
            $('#form-soln-name').submit();
        }
        return false;
    });
}

function set_portal_logo_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#logo-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#logo-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#logo-errors').html('');
        }
        show_progress("#portal-logo-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#portal-logo-working', false); }
    };
    $('#form-portal-logo').ajaxForm(options);
    $('#portal-logo-submit').click(function(){
        if(validate_form("#form-portal-logo")) {
            show_progress('#portal-logo-working', true);
            $('#form-portal-logo').submit();
        }
        return false;
    });
}

function set_proxy_cert_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#proxy-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#proxy-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#proxy-errors').html('');
        }
        show_progress("#proxy-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#proxy-working', false); }
    };
    $('#form-proxy').ajaxForm(options);
    $('#proxysubmit').click(function(){
        if(validate_form("#form-proxy")) {
            show_progress('#proxy-working', true);
            $('#form-proxy').submit();
        }
        return false;
    });
}


function set_mdm_cert_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#mdm-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#mdm-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
          $('#mdm-errors').html('');
        }
        show_progress("#mdm-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#mdm-working', false); }
    };
    $('#form-mdm').ajaxForm(options);
    $('#mdmsubmit').click(function(){
        if(validate_form("#form-mdm")) {
            show_progress('#mdm-working', true);
            $('#form-mdm').submit();
        }
        return false;
    });
}

function set_smtp_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#smtp-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#smtp-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#smtp-errors').html('');
        }
        show_progress("#smtp-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#smtp-working', false); }
    };
    $('#form-smtp').ajaxForm(options);
    $('#smtp-submit').click(function(){
        if(validate_form("#form-smtp")) {
            show_progress('#smtp-working', true);
            $('#form-smtp').submit();
        }
        return false;
    });
}



function set_bing_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#bing-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#bing-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#bing-errors').html('');
        }
        show_progress("#bing-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#bing-working', false); }
    };
    $('#form-bing').ajaxForm(options);
    $('#bing-submit').click(function(){
        if(validate_form("#form-bing")) {
            show_progress('#bing-working', true);
            $('#form-bing').submit();
        }
        return false;
    });
}

function set_gcm_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#gcm-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#gcm-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#gcm-errors').html('');
        }
        show_progress("#gcm-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#gcm-working', false); }
    };
    $('#form-gcm').ajaxForm(options);
    $('#gcm-submit').click(function(){
        if(validate_form("#form-gcm")) {
            show_progress('#gcm-working', true);
            $('#form-gcm').submit();
        }
        return false;
    });
}

function set_sms_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#sms-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#sms-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#sms-errors').html('');
        }
        show_progress("#sms-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#sms-working', false); }
    };
    $('#form-sms').ajaxForm(options);
    $('#sms-submit').click(function(){
        if(validate_form("#form-sms")) {
            show_progress('#sms-working', true);
            $('#form-sms').submit();
        }
        return false;
    });
}

function set_macconfig_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#mac-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#mac-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#mac-errors').html('');
        }
        show_progress("#mac-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#mac-working', false); }
    };
    $('#form-macconfig').ajaxForm(options);
    $('#mac-submit').click(function(){
        if(validate_form("#form-macconfig")) {
            show_progress('#mac-working', true);
            $('#form-macconfig').submit();
        }
        return false;
    });
}

function set_winconfig_form() {
    success_callback = function(json) {
        if (json.errors != undefined) {
          $('#win-errors').html('');
          $.each(json.errors, function (item, text) {
              $('#win-errors').append('<li>'+ item + " : " + text +'</li>');
          }); //for each
        }
        else {
            $('#win-errors').html('');
        }
        show_progress("#win-working", false);
    } //success_callback
    var options = {
        success: success_callback,
        error: function() { show_progress('#win-working', false); }
    };
    $('#form-winconfig').ajaxForm(options);
    $('#win-submit').click(function(){
        if(validate_form("#form-wincconfig")) {
            show_progress('#win-working', true);
            $('#form-winconfig').submit();
        }
        return false;
    });
}


function set_mac_radio_toggle() {
    $('#radio-mac-yes').click(function(){
        $('#mac-form-row').removeClass('blocked');
    });
    $('#radio-mac-no').click(function(){
        $('#mac-form-row').addClass('blocked');
    });
}

function set_win_radio_toggle() {
    $('#radio-win-yes').click(function(){
        $('#win-form-row').removeClass('blocked');
    });
    $('#radio-win-no').click(function(){
        $('#win-form-row').addClass('blocked');
    });
}


/*
 * Startup, setting handlers etc
 */

$(document).ready(function() {
    set_handlers();
});

function set_handlers() {
    setup_dbconfig_form();
    set_test_con_handler();
    set_create_db_schema_handler();
    set_activation_handler();
    setup_activate_form();
} // set_handlers


$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

/*
 * End Startup, setting handlers etc
 */

