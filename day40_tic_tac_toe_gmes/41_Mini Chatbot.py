def get_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return "Hi there! How can I assist you?"
    elif "how are you" in user_input:
        return "I'm doing great! How can I help you today?"
    elif "your name" in user_input:
        return "I'm Chatbot, your virtual assistant."
    elif "bye" in user_input:
        return "Goodbye! Have a wonderful day!"
    else:
        return "I'm not sure how to respond to that."

def chatbot():
    print("Hello! I'm Chatbot. Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ").lower()
        if "exit" in user_input:
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = get_response(user_input)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
	chatbot()
