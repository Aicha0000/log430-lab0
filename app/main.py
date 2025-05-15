import random

def get_random_message():
    message= ["Keep it up :)", "You got this :)", "You're almost at the finish line :)", "It will be okay :)"]
    return random.choice(message)

def main():
    print("Hey you!")
    print(get_random_message())

if __name__ == "__main__":
    main()
