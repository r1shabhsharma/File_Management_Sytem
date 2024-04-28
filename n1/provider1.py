import xmlrpc.client

def updateFile(proxy, fileName, content, replaceFile=False):
    result = proxy.updateFile(fileName, content, replaceFile)
    if result == "File updated successfully":
        print("File updated successfully")
    elif result == "User choice":
        choice = input('File with the same name already exists, what do you want to do? \n1. Replace the existing file with the new file\n2. Rename this new file\n3. Cancel the upload\nEnter your choice: ')
        if choice == '1':
            updateFile(proxy, fileName, content, True)
        elif choice == '2':
            newName = input('Enter the new file name: ')
            updateFile(proxy, newName, content)
        else:
            print('Cancelling the upload operation')
            return
    else:
        print("Error:", result)  # Print error message from server

if __name__ == "__main__":
    localServer = 'localhost'
    port = '8002'
    proxy = xmlrpc.client.ServerProxy(f"http://{localServer}:{port}/")
    fileName = input("Enter file name: ")
    fileData = input("Enter file data: ")
    updateFile(proxy, fileName, {'content':fileData})
