$(document).ready(function () {

    $('.text').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 500,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.10",
        autostart: true,
        cover: true
      });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    // mic button click event
    $("#MicBtn").click(function () { 
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.takecommand()()
    });

    // Background wake word listener
    function backgroundWakeListener() {
        eel.background_listen()(function(result) {
            if (result && result.toLowerCase().includes('lumina')) {
                $("#Oval").attr("hidden", true);
                $("#SiriWave").attr("hidden", false);
                eel.takecommand()();
            }
            // Continue listening in background
            setTimeout(backgroundWakeListener, 1000);
        });
    }
    backgroundWakeListener();

});