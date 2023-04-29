// Get references to the input field, chat box, and game name button
const chatBox = document.getElementById("chatArea");
const gameNameButton = document.querySelector(".ga");
chatBox.style.overflow = "auto";


function checkKey(event, element) {
  if (event.key == "Enter" && !event.shiftKey) {
    sendMessage();
  }
}



// Define the sendMessage function
function sendMessage() {
  const userInput = document.getElementById("userInputField").value.trim(); // Get the user's input and remove any leading/trailing whitespace
  if (userInput === "") {
    return null; // If the user's input is empty, do nothing
  }

  const gameNameInput = document.getElementById("fileNameWithJson");
  const gameName = gameNameInput.value.trim(); // Get the game name from the hidden input field and remove any leading/trailing whitespace

  // Disable the input field and game name button while the message is being sent

  // Add the user's input to the chat box as a message
  chatBox.innerHTML += "<div class='message user-message'><span>Me: </span>" + userInput + "</div>";

  $.ajax({
    url: "/api/answer",
    type: 'POST',
    data: {
      "user_input": userInput,
      "game_name": gameName
    },
    // dataType: 'json', // added data type
    beforeSend: function () {
      document.getElementById("userInputField").disabled = true;
      document.getElementById("searchSendButton").classList.add("disabled")
      // userInputField.value = "";
      // document.getElementById("userInputField").innerHTML = ""


      chatBox.innerHTML += `<div class="stage">
      <div class="dot-pulse"></div>
      </div>`
    },
    success: function (response) {
      $('.stage').remove();
      const data = response
      chatBox.innerHTML += "<div class='message chatbot-message'><span>BGC: </span>" + data.response.replaceAll('\n', '<br>') + "</div>";
      document.getElementById("userInputField").disabled = false;
      document.getElementById("searchSendButton").classList.remove("disabled")
      chatBox.scrollTop = chatBox.scrollHeight;

    },
    error: function (err) {
      $('.stage').remove();
      chatBox.innerHTML += "<div class='message chatbot-message'><span>BGC: </span>Oops, something went wrong!</div>";
      document.getElementById("userInputField").disabled = false;
      document.getElementById("searchSendButton").classList.remove("disabled")
      chatBox.scrollTop = chatBox.scrollHeight;
    },
  })

  // Clear the input field and re-enable the input field and game name button
  document.getElementById("userInputField").value = "";
  document.getElementById("userInputField").focus();

  // Scroll to the bottom of the chat box
}

