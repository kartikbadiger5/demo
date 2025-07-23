$(document).ready(function () {
    
    
    // Display Speak Message

    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        // If .siri-message has no <li>, add one
        if ($('.siri-message li').length === 0) {
            $('.siri-message').html('<li>' + message + '</li>');
        } else {
            $(".siri-message li:first").text(message);
        }
        $('.siri-message').textillate('start');
    }

    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }


    
});