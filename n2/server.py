import hashlib
import os
import sys
import threading
from xmlrpc.server import SimpleXMLRPCServer

class FileData:
    def __init__(self, file_name, file_hash):
        self.file_name = file_name
        self.file_hash = file_hash

    def __eq__(self, other):
        return self.file_name == other.file_name and self.file_hash == other.file_hash
    
    # This hash is different from the file content hashing we use to check duplication
    def __hash__(self):
        # This is done because when we add custom objects to a set, Python needs a way to determine whether two objects are equal and to quickly locate objects in the data structure.
        return hash((self.file_name, self.file_hash))

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

    def generate_hash(self, content):
        # Generate a hash value based on the content using SHA-256
        hash_object = hashlib.sha256(content.encode())
        hash_value = hash_object.hexdigest()
        return hash_value

    # function for server to update the received file on its local storage
    def updateFile(self, fileName, fileData, replaceFile=False):
        print('Trying to Upload file:', fileName)
        with self.lock:
            currentPath = os.getcwd()
            serverPath = os.path.join(currentPath, 'local-files')
            # deliberately adding this to ensure time gap for better analysis
            time.sleep(5)

            filePath = os.path.join(serverPath, fileName)
            fileHashCode = self.generate_hash(fileName + fileData['content'])
            

            for hashed_file_data in hashCodes:
                if fileHashCode == hashed_file_data.file_hash and filePath:
                    return 'A file with the same name and content already exists'
            
            if fileExists(filePath):
                if not replaceFile:
                    return 'User choice'
                for hashed_file_data in hashCodes:
                    print(hashed_file_data.file_name)
                    if(fileName == hashed_file_data.file_name):
                        hashed_file_data.file_hash = self.generate_hash(fileName + fileData['content'])
                        
            with open(filePath, 'w') as file:
                file.write(fileData['content'])
                hashCodes.add(FileData(fileName, fileHashCode))
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
        hashCodes.add(FileData(fileName, hashValue))

if __name__ == "__main__":
    address = 'localhost'
    port = 8002
    currentPath = os.getcwd()
    serverPath = os.path.join(currentPath, 'local-files')
    startServer(address, port, serverPath)
