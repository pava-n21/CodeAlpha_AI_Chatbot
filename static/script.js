const chatBox = document.getElementById("chat-box");

const userInput = document.getElementById("user-input");

const sendButton = document.getElementById("send-button");


/* =========================================
   ADD MESSAGE TO CHAT
========================================= */

function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message");


    /* USER MESSAGE */

    if (sender === "user") {

        messageDiv.classList.add("user-message");

    }


    /* BOT MESSAGE */

    else {

        messageDiv.classList.add("bot-message");

        const avatar = document.createElement("div");

        avatar.classList.add("avatar-small");

        avatar.textContent = "🤖";

        messageDiv.appendChild(avatar);
    }


    const contentDiv = document.createElement("div");

    contentDiv.classList.add("message-content");

    contentDiv.textContent = message;


    messageDiv.appendChild(contentDiv);

    chatBox.appendChild(messageDiv);


    /* Scroll to latest message */

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* =========================================
   SEND MESSAGE
========================================= */

async function sendMessage() {

    const message = userInput.value.trim();


    /* Don't send empty message */

    if (!message) {

        return;
    }


    /* Display user message */

    addMessage(message, "user");


    /* Clear input */

    userInput.value = "";


    /* Disable button while processing */

    sendButton.disabled = true;

    sendButton.style.opacity = "0.7";


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        /* Display bot response */

        addMessage(data.response, "bot");


    }

    catch (error) {

        console.error("Error:", error);

        addMessage(
            "Sorry! Something went wrong. Please try again.",
            "bot"
        );

    }


    finally {

        /* Enable button */

        sendButton.disabled = false;

        sendButton.style.opacity = "1";


        /* Focus input */

        userInput.focus();
    }
}


/* =========================================
   SEND BUTTON CLICK
========================================= */

sendButton.addEventListener(
    "click",
    sendMessage
);


/* =========================================
   ENTER KEY
========================================= */

userInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();
        }

    }
);


/* =========================================
   INITIAL INPUT FOCUS
========================================= */

window.addEventListener(
    "load",
    function() {

        userInput.focus();

    }
);