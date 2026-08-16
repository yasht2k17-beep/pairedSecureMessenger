from database import Database
from server.auth import Auth
from server.pair import PairManager
from server.message import Message
from server.filemanager import FileManager


def register(auth):

    username = input("Username: ")
    password = input("Password: ")

    if auth.register(username, password):
        print("Registration successful.")
    else:
        print("Username already exists.")


def login(auth):

    username = input("Username: ")
    password = input("Password: ")

    if auth.login(username, password):
        print("Login successful.")
        return True

    print("Invalid username or password.")
    return False


def pairMenu(auth, pair):

    username = auth.currentUser

    print("\n====== Pairing ======")
    print("1. Send Pair Request")
    print("2. Accept Pair Request")
    print("3. Reject Pair Request")
    print("4. Check Partner")
    print("5. Back")

    choice = input("Enter choice: ")

    if choice == "1":

        partner = input("Username to pair with: ")

        if pair.requestPair(username, partner):
            print("Pair request sent.")
        else:
            print("Could not send pair request.")

    elif choice == "2":

        requester = input("Username of requester: ")

        if pair.respondToPair(
            username,
            requester,
            "accept"
        ):
            print("Pair accepted.")
        else:
            print("No pending request found.")

    elif choice == "3":

        requester = input("Username of requester: ")

        if pair.respondToPair(
            username,
            requester,
            "reject"
        ):
            print("Pair request rejected.")
        else:
            print("No pending request found.")

    elif choice == "4":

        partner = pair.getPartner(username)

        if partner:
            print("Your partner:", partner)
        else:
            print("You are not paired with anyone.")


def messageMenu(auth, messages, pair):

    username = auth.currentUser
    partner = pair.getPartner(username)

    if partner is None:
        print("You are not paired with anyone.")
        return

    print("\n====== Messages ======")
    print("Partner:", partner)
    print("1. Send Message")
    print("2. View Messages")
    print("3. Back")

    choice = input("Enter choice: ")

    if choice == "1":

        msg = input("Message: ")

        if messages.send(
            username,
            partner,
            msg
        ):
            print("Message sent.")
        else:
            print("Message could not be sent.")

    elif choice == "2":

        conversation = messages.getMessages(
            username,
            partner
        )

        print("\n====== Conversation ======")

        if not conversation:
            print("No messages.")

        for message in conversation:

            print(
                f"[{message['timestamp']}] "
                f"{message['sender']}: "
                f"{message['message']}"
            )


def fileMenu(auth, files, pair):

    username = auth.currentUser
    partner = pair.getPartner(username)

    if partner is None:
        print("You are not paired with anyone.")
        return

    print("\n====== Files ======")
    print("1. Send File")
    print("2. View Files")
    print("3. Download File")
    print("4. Back")

    choice = input("Enter choice: ")

    if choice == "1":

        path = input("File path: ")

        if files.sendFile(
            username,
            partner,
            path
        ):
            print("File sent.")
        else:
            print("File could not be sent.")

    elif choice == "2":

        fileList = files.getFiles(
            username,
            partner
        )

        if not fileList:
            print("No files.")

        for file in fileList:

            print(
                f"ID: {file[0]} | "
                f"Sender: {file[1]} | "
                f"Receiver: {file[2]} | "
                f"Name: {file[3]} | "
                f"Time: {file[4]}"
            )

    elif choice == "3":

        fileID = input("File ID: ")

        try:
            fileID = int(fileID)

            path = files.downloadFile(
                fileID,
                username,
                partner
            )

            if path:
                print("Downloaded:", path)
            else:
                print("Download failed.")

        except ValueError:
            print("Invalid file ID.")


def userMenu(auth, pair, messages, files):

    while auth.currentUser:

        print("\n====== PAIRED ======")
        print("Logged in as:", auth.currentUser)
        print()
        print("1. Pairing")
        print("2. Messages")
        print("3. Files")
        print("4. Logout")

        choice = input("Enter choice: ")

        if choice == "1":

            pairMenu(
                auth,
                pair
            )

        elif choice == "2":

            messageMenu(
                auth,
                messages,
                pair
            )

        elif choice == "3":

            fileMenu(
                auth,
                files,
                pair
            )

        elif choice == "4":

            auth.logout()
            print("Logged out.")

        else:

            print("Invalid choice.")


def main():

    db = Database()

    auth = Auth(db)
    pair = PairManager(db)

    messages = Message(
        db,
        pair
    )

    files = FileManager(
        db,
        pair
    )

    while True:

        print("\n====== PAIRED SECURE MESSENGER ======")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":

            register(auth)

        elif choice == "2":

            if login(auth):

                userMenu(
                    auth,
                    pair,
                    messages,
                    files
                )

        elif choice == "3":

            print("Goodbye.")
            break

        else:

            print("Invalid choice.")


if __name__ == "__main__":
    main()