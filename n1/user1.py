import xmlrpc.client
import os

# function to request a file with given name
def requestFile(fileName, localServer, filePath):
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{localServer}/")
        fileData = proxy.getFile(fileName, filePath)
        if fileData['content']!= "File not found":
            print(f"\nFile found!")
            if fileData['source'] != "localhost":
                proxy.updateFile(fileName, fileData, filePath)
            return fileData
    except Exception as e:
        print(f"\nThere is an error while accessing the local server {localServer}: {e}")
    return {'content':"\nFile not found"}

if __name__ == "__main__":
    # give the private IP address for the server
    localServer = 'localhost:8002'
    currentPath = os.getcwd()
    # filePath stores the folder endpoint which has the sent/received files
    filePath = os.path.join(currentPath, 'local-files')
    fileName = input('Enter a file name to search: ')
    fileData = requestFile(fileName, localServer, filePath)
    print(fileData['content'])
    print("\n")
    