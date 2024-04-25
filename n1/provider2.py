import xmlrpc.client
import threading
import time

def updateFile(fileName, content, localServer, port):
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{localServer}:{port}/")
        threadInstance = threading.Thread(target= lambda:proxy.updateFile(fileName, content))
        threadInstance.start()
        threadInstance.join()
        # proxy.updateFile(fileName, content)
        print("File created successfully")
    except Exception as e:
        print(f"There is an error while updating file on local server {localServer}:{port}", e)

if __name__ == "__main__":
    # update the IP address to match the node private IP
    localServer = 'localhost'
    port = '8002'
    fileName = input("Enter file name: ")
    fileData = input("Enter file data: ")
    updateFile(fileName, {'content':fileData}, localServer, port)