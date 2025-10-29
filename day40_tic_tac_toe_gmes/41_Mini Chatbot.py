"""                                                             Day =  41
                          
						                                     Mini Chatbot
"""


import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.geometry("500x600")

        self.chatbot_name = "Chatbot"
        self.context = {}

        # Create the chat history display area (scrollable)
        self.chat_display = scrolledtext.ScrolledText(self.root, state='disabled', width=60, height=20, wrap=tk.WORD)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Create the text entry field
        self.user_input = tk.Entry(self.root, width=45)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)
        self.user_input.bind("<Return>", self.handle_input)  # Bind Enter key to send message

        # Create a send button
        self.send_button = tk.Button(self.root, text="Send", command=self.handle_input)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Focus on the text input when the app starts
        self.user_input.focus()

    def handle_input(self, event=None):
        """Handles user input and displays the response from the chatbot."""
        user_message = self.user_input.get().strip()

        if user_message.lower() == "exit":
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"{self.chatbot_name}: Goodbye! Have a wonderful day!\n")
            self.chat_display.config(state=tk.DISABLED)
            self.root.after(1000, self.root.quit)  # Close the app after 1 second
            return

        self.display_message("You", user_message)
        response = self.generate_response(user_message)
        self.display_message(self.chatbot_name, response)

        # Clear the input field after sending the message
        self.user_input.delete(0, tk.END)

    def generate_response(self, user_input):
        """Generate a response based on user input."""
        user_input = user_input.lower()

        # Dictionary of responses
        responses = {
            "hello": "Hi there! How can I assist you today?",
            "how are you": "I'm doing great, thank you for asking! How can I help you today?",
            "your name": f"I'm {self.chatbot_name}, your virtual assistant.",
            "bye": "Goodbye! Have a wonderful day!",
            "weather": "I can't provide real-time weather info, but you can check your local weather app.",
            "time": f"The current time is: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "joke": "Why don't skeletons fight each other? They don't have the guts!",
            "quote": "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
            "age": "I am timeless! I'm just here to assist you with anything you need.",
            "thanks": "You're welcome! Let me know if you need anything else.",
            "news": "I can't fetch real-time news, but you can check your favorite news website.",
            "sports": "Do you want to talk about sports? I can discuss football, basketball, and more!",
            "music": "I love music! What genre are you into?",
            "movies": "I love movies too! What kind of movies do you like?",
            "animals": "I love animals! What's your favorite animal?",
            "books": "I enjoy reading too! Any particular genre you’re interested in?",
            "space": "Space is vast and mysterious! Are you interested in space exploration?",
            "history": "I can tell you historical facts or events. What period are you interested in?",
            "math": "What kind of math do you want to discuss? Algebra, calculus, or something else?",
            "learn": "I can help you learn various topics like programming, history, math, and more!",
            "philosophy": "Philosophy makes you think deeply. Do you have a favorite philosopher?",
            "good morning": "Good morning! Hope you have a fantastic day ahead!",
            "good night": "Good night! Sleep tight, and dream sweet dreams!",
            "favorite food": "I can't eat, but if I could, I’d try pizza, it’s a classic!",
            "languages": "I can communicate in multiple languages. Which one would you like to use?",
            "dreams": "Do you have any dreams you'd like to achieve? Let's talk about them!",
            "thank you": "You're welcome! I'm always here to help.",
            "math fact": "Did you know? Zero is the only number that cannot be represented by Roman numerals.",
            "current events": "I can’t provide live updates, but you can check a news site for the latest events.",
            "favorite color": "I think blue is a nice color, but I like all colors equally!",
            "favorite season": "I think spring is beautiful, but I appreciate every season!",
            "future predictions": "The future is unpredictable, but it's exciting. What do you think it holds?",
            "advice": "Do what makes you happy and never stop learning!",
            "fun fact": "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!",
            "hello there": "General Kenobi! How can I help you today?",
            "how old are you": "I don't age, but I get smarter every day!",
            "weather update": "I can't give you weather updates, but I suggest you check your local weather.",
            "space exploration": "Space is an amazing field of study! Want to learn more?",
            "tell a story": "Once upon a time, a curious chatbot wanted to help people with their questions. And here I am!"
        }

        # Loop through responses and match based on user input
        for key, response in responses.items():
            if key in user_input:
                return response

        return "I'm not sure how to respond to that. Could you please rephrase?"

    def display_message(self, sender, message):
        """Displays a message in the chat window."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)  # Scroll to the bottom


if __name__ == "__main__":
    root = tk.Tk()
    chatbot_app = ChatbotApp(root)
    root.mainloop()




########################################################################################################################

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_app = ChatbotApp(root)
    root.mainloop()


    def display_message(self, sender, message):
        """Displays a message in the chat window."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)  # Scroll to the bottom


        # Loop through responses and match based on user input
        for key, response in responses.items():
            if key in user_input:
                return response

        return "I'm not sure how to respond to that. Could you please rephrase?"


            "advice": "Do what makes you happy and never stop learning!",
            "fun fact": "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!",
            "hello there": "General Kenobi! How can I help you today?",
            "how old are you": "I don't age, but I get smarter every day!",
            "weather update": "I can't give you weather updates, but I suggest you check your local weather.",
            "space exploration": "Space is an amazing field of study! Want to learn more?",
            "tell a story": "Once upon a time, a curious chatbot wanted to help people with their questions. And here I am!"
        }

            "languages": "I can communicate in multiple languages. Which one would you like to use?",
            "dreams": "Do you have any dreams you'd like to achieve? Let's talk about them!",
            "thank you": "You're welcome! I'm always here to help.",
            "math fact": "Did you know? Zero is the only number that cannot be represented by Roman numerals.",
            "current events": "I can’t provide live updates, but you can check a news site for the latest events.",
            "favorite color": "I think blue is a nice color, but I like all colors equally!",
            "favorite season": "I think spring is beautiful, but I appreciate every season!",
            "future predictions": "The future is unpredictable, but it's exciting. What do you think it holds?",


          "math": "What kind of math do you want to discuss? Algebra, calculus, or something else?",
            "learn": "I can help you learn various topics like programming, history, math, and more!",
            "philosophy": "Philosophy makes you think deeply. Do you have a favorite philosopher?",
            "good morning": "Good morning! Hope you have a fantastic day ahead!",
            "good night": "Good night! Sleep tight, and dream sweet dreams!",
            "favorite food": "I can't eat, but if I could, I’d try pizza, it’s a classic!",
