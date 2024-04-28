import xmlrpc.client
import time

def updateFile(proxy, fileName, content, replaceFile=False):
    token_acquired = False
    attempts = 0
    max_attempts = 10  # Maximum number of attempts to acquire the token
    while not token_acquired and attempts < max_attempts:
        token_acquired = proxy.acquire_token("provider2")  # Provider 1 identifier
        if not token_acquired:
            print("Failed to acquire token. Retrying...")
            time.sleep(3)  # Wait for a short duration before retrying
            attempts += 1
            
    if token_acquired:
        print("Token Acquired")
        result = proxy.updateFile(fileName, content, replaceFile)
        if result == "File updated successfully":
            print("File updated successfully")
        elif result == "User choice":
            proxy.pass_token()
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
        proxy.pass_token()
    else:
        print("Failed to acquire token after multiple attempts. Please try again later.")

if __name__ == "__main__":
    localServer = 'localhost'
    port = '8002'
    proxy = xmlrpc.client.ServerProxy(f"http://{localServer}:{port}/")
    fileName = input("Enter file name: ")
    fileData = input("Enter file data: ")
    updateFile(proxy, fileName, {'content':fileData})
