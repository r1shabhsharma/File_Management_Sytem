import xmlrpc.client

def requestFile(fileName, localServer):
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{localServer}/")
        fileData = proxy.getFile(fileName)
        if fileData['content'] != "File not found":
            print(f"\nFile found!")
            return fileData
        else:
            print("\nFile not found :(")
    except Exception as e:
        print(f"\nThere was an error while accessing the local server {localServer}: {e}")
    return {'content': "\nFile not found"}

if __name__ == "__main__":
    localServer = 'localhost:8002'  # Replace with the correct server address and port
    fileName = input('Enter a file name to search: ')
    fileData = requestFile(fileName, localServer)
    print(fileData['content'])
    print("\n")
