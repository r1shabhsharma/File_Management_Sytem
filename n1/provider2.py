import xmlrpc.client
import threading

def updateFile(fileName, content, localServer, port):
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{localServer}:{port}/")
        token_acquired = proxy.acquire_token("provider2")  # Provider 2 identifier
        if token_acquired:
            threadInstance = threading.Thread(target=lambda: updateFileThread(proxy, fileName, content))
            threadInstance.start()
            threadInstance.join()
            proxy.pass_token()
        else:
            print("Failed to acquire token. The server is currently handling another request. Please try again later.")
    except Exception as e:
        print(f"There is an error while updating file on local server {localServer}:{port}", e)

def updateFileThread(proxy, fileName, content, replaceFile=False):
    result = proxy.updateFile(fileName, content, replaceFile)
    if result == "File updated successfully":
        print("File updated successfully")
    elif result == "User choice":
        choice = input('File with the same name already exists, what do you want to do? \n1. Replace the existing file with the new file\n2. Rename this new file\n3. Cancel the upload\nEnter your choice: ')
        if choice == '1':
            updateFileThread(proxy, fileName, content, True)
        elif choice == '2':
            newName = input('Enter the new file name: ')
            updateFileThread(proxy, newName, content)
        else:
            print('Cancelling the upload operation')
            return
    else:
        print("Error:", result)  # Print error message from server

if __name__ == "__main__":
    localServer = 'localhost'
    port = '8002'
    fileName = input("Enter file name: ")
    fileData = input("Enter file data: ")
    updateFile(fileName, {'content':fileData}, localServer, port)
