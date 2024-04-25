import hashlib
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
import sys
import threading
import time

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


            if fileExists(os.path.join(self.fileDirectory, fileName)):
                content_hash = self.generate_hash(fileData['content'])
                # Append the hash to the original file name
                hashed_filename = f"{fileName}_{content_hash}"
                filePath = os.path.join(serverPath, hashed_filename)
            else:
                filePath = os.path.join(serverPath, fileName)

            print('done')
            with open(filePath, 'w') as file:
                file.write(fileData['content'])
        return "File updated successfully"

        
            # # Generate hash of the file content
            # content_hash = self.generate_hash(fileData['content'])
            # # Append the hash to the original file name
            # hashed_filename = f"{fileName}_{content_hash}"
            # filePath = os.path.join(serverPath, hashed_filename)

            # print('Doneeee')

            # # Check if a file with the same content already exists
            # if fileExists(filePath):
            #     return "File already exists"
            # else:
            #     with open(filePath, 'w') as file:
            #         file.write(fileData['content'])
            #     return "File updated successfully"

    # function to get the file
    # It searches for the file in a ring topology
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
    print(f"Server {serverId} now listening on port {port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nQuiting...")
        sys.exit(0)

if __name__ == "__main__":
    address = 'localhost'
    port = 8002
    currentPath = os.getcwd()
    serverPath = os.path.join(currentPath, 'local-files')
    startServer(address, port, serverPath)
