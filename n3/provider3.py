import xmlrpc.client
import threading

def updateFile(fileName, content, localServer, port):
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{localServer}:{port}/")
        threadInstance = threading.Thread(target=lambda: updateFileThread(proxy, fileName, content))
        threadInstance.start()
        threadInstance.join()
    except Exception as e:
        print(f"There is an error while updating file on local server {localServer}:{port}", e)

def updateFileThread(proxy, fileName, content):
    result = proxy.updateFile(fileName, content)
    if result == "File updated successfully":
        print("File updated successfully")
    else:
        print("Error:", result)  # Print error message from server

if __name__ == "__main__":
    # update the IP address to match the node private IP
    localServer = 'localhost'
    port = '8002'
    fileName = input("Enter file name: ")
    fileData = input("Enter file data: ")
    updateFile(fileName, {'content':fileData}, localServer, port)