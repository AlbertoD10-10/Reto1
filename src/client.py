from concurrent import futures
from threading import Thread
from typing import List

import grpc
import client_pb2
import client_pb2_grpc
import node_pb2
import node_pb2_grpc

CLIENT_PORT = 56000
NODE_STARTING_PORT = 60000

class ResponseReceiver(client_pb2_grpc.ClientServicer):
    def ClientLookupReply(self, request, context) -> node_pb2.Empty:
        if request.value:
            print(f'[Cliente]: clave {request.key} referenciando valor "{request.value}" encontrado numero nodo {request.node_id}')
        else:
            print(f'[Cliente]: clave {request.key} no encontrada, deveria estar presente numero nodo {request.node_id}')

        return node_pb2.Empty()

    def ClientInsertReply(self, request, context) -> node_pb2.Empty:
        print(f'[Cliente]: valor "{request.value}" identificado la clave "{request.key}" fue insertado numero nodo {request.node_insert}')
        return node_pb2.Empty()


def print_help() -> None:
    print("Implementacion simple de chord")
    print("Comandos:")
    print("insert <no_origen> <clave> <valor>")
    print("search <no_origen> <clave>")
    print("="*20)

def search(args: List[str]) -> None:
    id_busca: int = 0   # TODO change id_busca to something meaningful
    node_origin: int = int(args[1])
    key: str = args[1]
    node_origin_port: int = NODE_STARTING_PORT + node_origin


    with grpc.insecure_channel(f'localhost:{node_origin_port}') as channel:
        node_stub: node_pb2_grpc.NodeStub = node_pb2_grpc.NodeStub(channel)
        _ = node_stub.Lookup(node_pb2.LookupRequest(
            node_origin=node_origin,
            key=key,
            client_port=CLIENT_PORT
        ))

    # if node_response.value:
    #     print(f'[Cliente]: chave {chave} referenciando valor "{node_response.value}" encontrado no nó {node_response.node_id}')
    # else:
    #     print(f'[Cliente]: chave {chave} não encontrada, deveria estar presente no nó {node_response.node_id}')


def insert(args: List[str]) -> None:
    node_origin: int = int(args[0])
    chave: str = args[1]
    valor: str = args[2]
    node_origin_port: int = NODE_STARTING_PORT + node_origin
    print(f'Insert:\n no: {node_origin}\n clave: {chave}\n valor: {valor}')
    print(f' port: {node_origin_port}')

    with grpc.insecure_channel(f'localhost:{node_origin_port}') as channel:
        node_stub: node_pb2_grpc.NodeStub = node_pb2_grpc.NodeStub(channel)
        _ = node_stub.Insert(node_pb2.InsertRequest(
            node_origin=node_origin,
            key=chave,
            value=valor,
            client_port=CLIENT_PORT
        ))

    # print(f'[Cliente]: valor "{valor}" identificado pela chave "{chave}" foi inserido no nó {node_response.node_insert}')

def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    client_pb2_grpc.add_ClientServicer_to_server(ResponseReceiver(), server)
    server.add_insecure_port(f'localhost:{CLIENT_PORT}')
    server.start()
    server.wait_for_termination()

def run() -> None:
    server_thread = Thread(target=serve)
    server_thread.start()
    print_help()

    while True:
        cmd_input: str = input()
        cmd_split: List[str] = cmd_input.split()
        cmd: str = cmd_split[0]
        cmd_arguments: List[str] = cmd_split[1:]

        if cmd == 'search':
            search(cmd_arguments)
        elif cmd == 'insert':
            insert(cmd_arguments)
        elif cmd == 'end':
            break
        else:
            print(f'Comando {cmd} no reconocido')

if __name__ == '__main__':
    run()