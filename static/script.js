$(document).ready(function () {


  var soundOn = true;
  $("#toggle-sound-btn").click(function () {
    soundOn = !soundOn;
    if (!soundOn) {
      speechSynthesis.cancel(); // Stop current speech
    }
  });

  $(".stop-voice").click(
    function () {
        speechSynthesis.cancel(); // Stop current speech
    }
  );

  // Volume control
  $("#volume-control").on("input", function () {
    var volume = $(this).val() / 100;
    setVolume(volume);
  });

  // Function to set volume
  function setVolume(volume) {
    var utterance = new SpeechSynthesisUtterance();
    utterance.volume = volume;
    speechSynthesis.speak(utterance); // A dummy utterance to set the volume
  }

  $("#send-btn").click(function () {
    sendMessage();
  });

  // Function to handle voice input
  function startVoiceInput() {
    var recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();
    recognition.onresult = function (event) {
      var transcript = event.results[0][0].transcript;
      $("#user-input").val(transcript);
      recognition.stop();
      sendMessage(); // Send the message after voice input
    };
  }

  // Add event listener to the microphone button
  $("#voice-btn").click(function () {
    startVoiceInput();
  });

  // Add event listener to handle Enter key press
  $("#user-input").keypress(function (event) {
    if (event.which === 13) {
      // 13 is the key code for Enter
      event.preventDefault();
      sendMessage();
    }
  });

  // Function to send message
  function sendMessage() {
    var userInput = $("#user-input").val();
    if (userInput !== "") {
      $("#chat-container").append(
        '<p class="bubble you"><strong style="color:green;">You:</strong> ' +
          userInput +
          "</p>"
      );
      $("#user-input").val("");
      $.ajax({
        type: "POST",
        url: "/chat",
        data: { user_input: userInput },
        success: function (response) {
          var botResponse = response.response.replace(/\r?\n/g, "<br>");
          botResponse = botResponse.replace(/\*\*/g, "");
          $("#chat-container").append(
            '<p class="bubble me"><strong style="color:blue;">Drona:</strong> ' +
              botResponse +
              "</p>"
          );
          speak(botResponse);
        },
      });
    }
  }

  // Function to speak the bot's response
  function speak(text) {
    var utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
  }

  $("#about").click(function about(){
    var about = $("#about").text();
    speak(about);
  }).trigger('click');



});
