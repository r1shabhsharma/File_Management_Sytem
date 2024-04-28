import xmlrpc.client

def requestFile(fileName, localServer):
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{localServer}/")
        token_acquired = proxy.acquire_token("user1")
        if token_acquired:
            fileData = proxy.getFile(fileName)
            if fileData['content'] != "File not found":
                print(f"\nFile found!")
                proxy.pass_token()
                return fileData
            else:
                print("\nFile not found :(")
                proxy.pass_token()
        else:
            print("Failed to acquire token. The server is currently handling another request. Please try again later.")
    except Exception as e:
        print(f"\nThere was an error while accessing the local server {localServer}: {e}")
    return {'content': "\nFile not found"}

if __name__ == "__main__":
    localServer = 'localhost:8002'  # Replace with the correct server address and port
    fileName = input('Enter a file name to search: ')
    fileData = requestFile(fileName, localServer)
    print(fileData['content'])
    print("\n")
