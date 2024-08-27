import yaml
import grpc
from concurrent import futures
import time 
from services.file_service import serve

import services.fileservice_pb2_grpc
import services.fileservice_pb2

from chord_node import ChordNode

class FileServiceServicer(services.fileservice_pb2.FileServiceServicer):
    def __init__(self,node):
        self.node = node

    def UploadFile(self, request, context):
        return services.fileservice_pb2.FileResponse(message=f'Archivo {request.filename} subido correctamente')
    
    def DownloadFile(self, request, context):
        return services.fileservice_pb2.FileResponse(message= f'Archivo {request.filename} descargado correctamente')
    
    def FindSuccessor(self,request, context):
        successor = self.node.find_successor(request.id)
        return services.fileservice_pb2.NodeInfo(id=successor.id, ip = successor.ip, port = successor.port)
    
    def Notify(self,request,context):
        self.node.notify(request.predecessor_id)
        return services.fileservice_pb2.Empty()

    def serve():
        node = ChordNode (id=0, ip='127.0.0.1', port= 50051)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        services.fileservice_pb2_grpc.add_FileServiceServicer_to_server(FileServiceServicer(node), server)

        server.add_insecure_port('[::]:50051')
        server.start()
        print ("servidor iniciado en el puerto 50051")

        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)

if __name__ == "__main__":
  serve()


