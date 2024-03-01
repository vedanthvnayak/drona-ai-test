$(document).ready(function() {
    $('#send-btn').click(function() {
        sendMessage();
    });

    // Function to handle voice input
    function startVoiceInput() {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.start();
        recognition.onresult = function(event) {
            var transcript = event.results[0][0].transcript;
            $('#user-input').val(transcript);
            recognition.stop();
            sendMessage(); // Send the message after voice input
        };
    }

    // Add event listener to the microphone button
    $('#voice-btn').click(function() {
        startVoiceInput();
    });

    // Function to send message
    function sendMessage() {
        var userInput = $('#user-input').val();
        if (userInput !== '') {
            $('#chat-container').append('<p class="bubble you"><strong style="color:green;">You:</strong> ' + userInput + '</p>');
            $('#user-input').val('');
            $.ajax({
                type: 'POST',
                url: '/chat',
                data: {user_input: userInput},
                success: function(response) {
                    var botResponse = response.response;
                    $('#chat-container').append('<p class="bubble me"><strong style="color:blue;">Drona:</strong> ' + botResponse + '</p>');
                    speak(botResponse);
                }
            });
        }
    }

    // Function to speak the bot's response
    function speak(text) {
        var utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
    }
});
