import xmlrpc.client

# Basic text based user interface for getting input from user.
def userInterface():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    print("What do you want to do?")
    print("1) Add content to the XML database")
    print("2) Get contents from XML database")
    print("3) Get data from wikipedia")
    print("4) Exit the program\n")
    choice = input("Enter your choice: ")
    choice = int(choice)
    
    if (choice == 1):
        topic = input("Topic: ")
        name = input("Name: ")
        text = input("Text: ")
        print("\n" + proxy.addData(topic, name, text) + "\n")
        return True
    elif (choice == 2):
        topic = input("Topic: ")
        result = proxy.getData(topic)
        if (result != []):
            for note in result:
                print("Name: {0}; Text content: {1}; Timestamp: {2}".format(note["name"], note["text"], note["timestamp"]))
        else:
            print("\nTopic with that name was not found\n")
        return True
    elif (choice == 3):
        topic = input("Topic: ")
        data = proxy.getWikipediaData(topic)
        print("\n" + data + "\n")
        add = input("Add to database? (Y/N): ")
        add = add.lower()
        
        if (add == "y"):
            print("\n" + proxy.addData(topic, "Wikipedia Link", data) + "\n")

        return True
    elif (choice == 4):
        # Stops the while loop
        return False
    else:
        print("Unexpected input '{0}'\n".format(choice))
        return True
        
if __name__ == "__main__":
    result = True
    
    while (result):
        result = userInterface()