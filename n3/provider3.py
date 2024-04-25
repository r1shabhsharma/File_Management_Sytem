import xmlrpc.client
import os

def updateFile(fileName, content, localServer, port):
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{localServer}:{port}/")
        proxy.updateFile(fileName, content)
        print("File created successfully")
    except Exception as e:
        print(f"There is an error while updating file on local server {localServer}:{port}")

if __name__ == "__main__":
    # update the IP address to match the node private IP
    localServer = 'localhost'
    port = '8002'
    fileName = input("Enter file name: ")
    fileData = input("Enter file data: ")
    updateFile(fileName, {'content':fileData}, localServer, port)