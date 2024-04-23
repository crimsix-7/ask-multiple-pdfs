css = '''
<style>
/* Overall body styling */
body {
    background-color: #fff; /* Keeping the background white for contrast */
    color: #4c4c4c; /* A softer shade for text for better readability */
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; /* Modern font */
}

/* Style the chat box messages */
.chat-message {
    padding: 0.8rem 1.5rem; /* Adjust padding for a less bulky appearance */
    border-radius: 18px; /* Rounded corners for a softer look */
    margin-bottom: 0.5rem; /* Less space between messages */
    display: flex;
    align-items: center; /* Align items vertically */
    box-shadow: 0 2px 4px 0 rgba(0,0,0,0.1); /* Soft shadow for depth */
    transition: background-color 0.3s ease; /* Smooth background transition */
}

/* User message styling */
.chat-message.user {
    background-color: #ffebee; /* A very light red/pinkish background for user messages */
    justify-content: flex-end; /* Align user messages to the right */
}

/* Bot message styling */
.chat-message.bot {
    background-color: #fff; /* White background for bot messages */
    border: 1px solid #ffb3b3; /* Soft red border for bot messages */
    justify-content: flex-start; /* Align bot messages to the left */
}

/* Avatar styling */
.chat-message .avatar img {
    width: 50px; /* Smaller avatars */
    height: 50px; /* Fixed height for square aspect ratio */
    border-radius: 50%; /* Circular avatars */
    margin-right: 1rem; /* Space between avatar and message */
}

/* Message text styling */
.chat-message .message {
    flex: 1; /* Allow message text to fill the space */
    margin: 0; /* Reset margins */
}

/* User text color */
.user .message {
    color: #5c1010; /* A darker red for user text for readability */
}

/* Bot text color */
.bot .message {
    color: #5c1010; /* A darker red for bot text for readability */
}

/* Sidebar styling */
.stSidebar {
    background-color: #ffebee; /* Light red background for sidebar */
    color: #5c1010; /* Dark red text color for contrast */
}

/* Input field and button styling */
.stTextInput, .stButton>button {
    border-radius: 18px; /* Rounded corners for input and button */
    border: 1px solid #ffb3b3; /* Soft red border */
}

/* Button specific styling */
.stButton>button {
    background-color: #ff6666; /* A medium red for buttons */
    color: #fff; /* White text for buttons */
    padding: 0.5rem 1rem; /* Padding inside buttons */
    margin-top: 0.5rem; /* Space above the button */
    transition: background-color 0.3s ease; /* Smooth background transition for button */
}

/* Hover effects */
.stButton>button:hover {
    background-color: #e60000; /* Darker red on hover for button */
}

/* Adjust the file uploader to fit the red theme */
.stFileUploader {
    border: 2px dashed #ffb3b3; /* Dashed border for the file uploader */
    background-color: #fff; /* White background to stand out on the red sidebar */
    color: #5c1010; /* Text color to match the theme */
}

/* Remove Streamlit's branding for a cleaner look */
footer {
    display: none;
}

/* Additional responsive design adjustments */
@media (max-width: 768px) {
    .chat-message {
        flex-direction: column; /* Stack avatar and message on small screens */
    }

    .chat-message .avatar, .chat-message .message {
        width: 100%; /* Full width on small screens */
        text-align: center; /* Center text on small screens */
        margin-bottom: 0.5rem; /* Space between avatar and message on small screens */
    }
}
</style>
'''



bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
