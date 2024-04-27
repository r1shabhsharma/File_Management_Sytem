import hashlib
import os
import sys
import threading
import time
from xmlrpc.server import SimpleXMLRPCServer

hashCodes = set()

def getFileData(filePath):
    with open(filePath, 'r') as file:
        content = file.read()
    return content

def fileExists(filePath):
    return os.path.isfile(filePath)

class FileSystemRPC:
    # initialization function
    def __init__(self, serverId, fileDirectory):
        self.serverId = serverId
        self.fileDirectory = fileDirectory
        self.lock = threading.Lock()
        self.hashFiles = []

    def generate_hash(self, content):
        # Generate a hash value based on the content using SHA-256
        hash_object = hashlib.sha256(content.encode())
        hash_value = hash_object.hexdigest()
        return hash_value

    # function for server to update the received file on its local storage
    def updateFile(self, fileName, fileData):
        print('Updating file:', fileName)
        with self.lock:
            currentPath = os.getcwd()
            serverPath = os.path.join(currentPath, 'local-files')
            # deliberately adding this to ensure time gap for better analysis
            time.sleep(5)

            filePath = os.path.join(serverPath, fileName)
            combined_data = fileName + fileData['content']
            fileHashCode = hashlib.sha256(combined_data.encode()).hexdigest()

            if filePath and fileHashCode in hashCodes:
                return 'A file with the same name and content already exists' 
            else:
                with open(filePath, 'w') as file:
                    file.write(fileData['content'])
                    hashCodes.add(fileHashCode)
                    return "File updated successfully"  # Return success message
                
    # Function to fetch the file
    def getFile(self, fileName):

        filePath = os.path.join(self.fileDirectory, fileName)
        if fileExists(filePath):
            print(f"\nFile found!")
            fileData = {'content': getFileData(filePath), 'source': "localhost"}
        else:
            print(f"\nFile not founddd!")
        return fileData

def startServer(serverId, port, fileDirectory):
    server = SimpleXMLRPCServer((address, port))
    server.register_instance(FileSystemRPC(serverId, fileDirectory))
    setHashCodes(fileDirectory)
    print(f"Server {serverId} now listening on port {port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nQuiting...")
        sys.exit(0)

# Assign hash codes of all files to the set
def setHashCodes(fileDirectory):
    files = os.listdir(fileDirectory)
    for fileName in files:
        filePath = os.path.join(fileDirectory, fileName)
        fileData = getFileData(filePath)
        combined_data = fileName + fileData
        hashValue = hashlib.sha256(combined_data.encode()).hexdigest()
        hashCodes.add(hashValue)
        print(hashCodes)

if __name__ == "__main__":
    address = 'localhost'
    port = 8002
    currentPath = os.getcwd()
    serverPath = os.path.join(currentPath, 'local-files')
    startServer(address, port, serverPath)
