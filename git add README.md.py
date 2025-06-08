# Welcome Message Generator
import datetime

#Step 1st ask user details
name = input("What is your name: ")
hobby = input("Whats your hobby: ")

# Get the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
print(f"Current Date: {current_date}")


# step 2 generate a personalized welcome message

print("\n--- Welcome Message ---")
print(f"Hello {name}")
print(f"Welcome to the python programming")
print(f"Your Hobby is {hobby}")
print(f"Get ready to build something Amazing")
