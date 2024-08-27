import grpc
import services.fileservice_pb2_grpc 
import services.fileservice_pb2
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = services.fileservice_pb2_grpc .FileServiceStub(channel)
        response = stub.UploadFile(services.fileservice_pb2.FileRequest(filename="example.txt"))
        print("Upload response: ", response.message)

        response = stub.DownloadFile(services.fileservice_pb2.FileRequest(filename="example.txt"))
        print("Download response: ", response.message)

        id_to_find = 5
        response = stub.FindSuccessor(services.fileservice_pb2.NodeID(id = id_to_find))
        print(f"El sucesor del ID {id_to_find} es el nodo con ID {response.id} en {response.ip}:{response.port}")

if __name__ == "__main__":
    run()
