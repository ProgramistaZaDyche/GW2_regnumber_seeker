import requests as req
import threading
import time


def communicate(name, sought_number, email):
    # If the connection could not be established, try again
    loop = True
    while loop:
        try:
            r = req.get(f"https://account.arena.net/ws/username?_t=1631470870652&email={email}&displayname={name}")
        except:
            # Give some time to the server
            time.sleep(0.05)
            continue
        loop = False
        answer = r.content[11:15].decode()
        #print(answer)
        if answer == sought_number:
            with open(f'{len(name)}char_names.txt', 'a') as f:
                f.write(name + " " + sought_number + " " + email + "\n")
                print(f"I have found new name! - {name}")


def prepare_string(names_to_be, row, sought_number, email, prefix="", suffix=""):
    # Only 'a's
    name = "".join(names_to_be)
    watek = threading.Thread(target=communicate, args=(prefix+name+suffix, sought_number, email,))
    watek.start()

    for character in range(ord('a'), ord('{')):
        if row < len(names_to_be) - 1:
            prepare_string(names_to_be, row + 1, sought_number, email, prefix, suffix)

        names_to_be[row] = chr(ord(names_to_be[row]) + 1)
        if names_to_be[row] == '{': continue

        name = "".join(names_to_be)
        watek = threading.Thread(target=communicate, args=(prefix+name+suffix, sought_number,email,))
        watek.start()

    names_to_be[row] = 'a'


length_of_strings = int(input("How long do you want your name to be?\n"))
while length_of_strings < 3 or length_of_strings > 27:
    length_of_strings = int(input("Name's length needs to be between 3 and 27 characters!\n"))

# Email is not being checked.
email_address = input("What is your email address?\n")
prefix = input("Enter wanted prefix.\n")
while len(prefix) >= length_of_strings:
    prefix = input("Prefix is too long, try again.\n")

suffix = input("Enter wanted suffix.\n")
while len(suffix) >= length_of_strings:
    suffix = input("Suffix is too long, try again.\n")

while len(prefix) + len(suffix) >= length_of_strings:
    print("Prefix and suffix have to be shorter than the name!")
    prefix = ("Enter new prefix.\n")
    suffix = ("Enter new suffix.\n")
# Neither prefix or suffix are checked whether they are a-z characters.

sought_number = input("What number do you seek?\n")
while not sought_number.isnumeric():
    sought_number = input("It needs to be a number!\n")
while len(sought_number) != 4:
    sought_number = input("The number needs to have exactly 4 digits, try again.\n")

list_of_chars = ['a']*(length_of_strings - len(prefix) - len(suffix))
print("Seeeking...")
prepare_string(list_of_chars, 0, sought_number, email_address, prefix, suffix,)
print("Thank you for your patience, the communication with the server will end shortly.")
