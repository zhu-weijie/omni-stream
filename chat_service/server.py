import logging
from concurrent import futures
from datetime import datetime, UTC

import grpc

import chat_pb2
import chat_pb2_grpc

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    def Chat(self, request_iterator, context):
        last_user = ""
        logging.info("Client connected to chat service.")

        for request in request_iterator:
            logging.info(
                f"Received message from '{request.user_id}': {request.message}"
            )
            last_user = request.user_id

            response_message = chat_pb2.ChatMessage(
                user_id="Server",
                message=f"[Server echo]: {request.message}",
                timestamp=datetime.now(UTC).isoformat(),
            )
            yield response_message

        logging.info(f"Client '{last_user}' disconnected.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    logging.info("Chat Service listening on port 50053")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
