import hashlib
import os
import sys
import threading
import time
import logging
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

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
        self.threadResponse = ''

    def generate_hash(self, content):
        # Generate a hash value based on the content using SHA-256
        hash_object = hashlib.sha256(content.encode())
        hash_value = hash_object.hexdigest()
        return hash_value
    
    def updateFileThread(self, fileName, fileData, replaceFile=False):
        logging.info('Trying to upload file: %s\nThread identifier of current process: %s', fileName, threading.get_ident())
        with self.lock:
            currentPath = os.getcwd()
            serverPath = os.path.join(currentPath, 'local-files')
            # deliberately adding this to ensure time gap for better analysis
            time.sleep(5)

            filePath = os.path.join(serverPath, fileName)
            fileHashCode = self.generate_hash(fileName + fileData['content'])
            
            for hashed_file_data in hashCodes:
                if fileHashCode == hashed_file_data.file_hash and filePath:
                    self.threadResponse= 'A file with the same name and content already exists'
                    logging.error(self.threadResponse)

            if fileExists(filePath):
                if not replaceFile:
                    self.threadResponse= 'User choice'
                    logging.error(self.threadResponse)
                    return
                for hashed_file_data in hashCodes:
                    if fileName == hashed_file_data.file_name:
                        hashed_file_data.file_hash = self.generate_hash(fileName + fileData['content'])
                        
            with open(filePath, 'w') as file:
                file.write(fileData['content'])
                hashCodes.add(FileData(fileName, fileHashCode))
                self.threadResponse= "File updated successfully"  # Return success message
                logging.error(self.threadResponse)
                    
    def updateFile(self, fileName, fileData, replaceFile=False):
        # Create a thread for file update process
        update_thread = threading.Thread(target=self.updateFileThread, args=(fileName, fileData, replaceFile))
        update_thread.start()
         # Wait for the thread to finish
        update_thread.join()
    
        # Return the response from thread
        return self.threadResponse

    def getFile(self, fileName):
        filePath = os.path.join(self.fileDirectory, fileName)
        if fileExists(filePath):
            logging.info('File found: %s', fileName)
            return {'content': getFileData(filePath)}
        else:
            logging.error('File not found: %s', fileName)
            return {'content': 'File not found'}

def startServer(serverId, port, fileDirectory):
    server = ThreadedXMLRPCServer((serverId, port))
    server.register_instance(FileSystemRPC(serverId, fileDirectory))
    setHashCodes(fileDirectory)
    logging.info('Server %s now listening on port %s...', serverId, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('Quitting...')
        sys.exit(0)

def setHashCodes(fileDirectory):
    files = os.listdir(fileDirectory)
    for fileName in files:
        filePath = os.path.join(fileDirectory, fileName)
        fileData = getFileData(filePath)
        combined_data = fileName + fileData
        hashValue = hashlib.sha256(combined_data.encode()).hexdigest()
        hashCodes.add(FileData(fileName, hashValue))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    serverId = 'localhost'
    port = 8002
    currentPath = os.getcwd()
    serverPath = os.path.join(currentPath, 'local-files')
    startServer(serverId, port, serverPath)
