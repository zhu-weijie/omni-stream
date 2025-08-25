import logging
import sys
import threading
import time
from datetime import datetime, UTC

import grpc

sys.path.append("chat_service")
import chat_pb2
import chat_pb2_grpc

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def receive_messages(stub, user_id):
    try:

        def initial_request_generator():
            yield chat_pb2.ChatMessage(
                user_id=user_id, message=f"{user_id} has joined the chat."
            )
            while not stop_event.is_set():
                time.sleep(0.1)

        response_iterator = stub.Chat(initial_request_generator())

        for response in response_iterator:
            logging.info(f"[{response.user_id}]: {response.message}")

    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.CANCELLED:
            logging.info("Stream cancelled by the client.")
        else:
            logging.error(f"An RPC error occurred in receiving thread: {e}")


def run_client(user_id):
    with grpc.insecure_channel("chat_service:50053") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        global stop_event
        stop_event = threading.Event()

        def request_generator():
            try:
                while not stop_event.is_set():
                    message = input("Enter message (or 'quit'): ")
                    if message.lower() == "quit":
                        stop_event.set()
                        break

                    yield chat_pb2.ChatMessage(
                        user_id=user_id,
                        message=message,
                        timestamp=datetime.now(UTC).isoformat(),
                    )
            except EOFError:
                stop_event.set()

        try:
            response_iterator = stub.Chat(request_generator())

            logging.info("--- Connected to chat. Type 'quit' to exit. ---")

            for response in response_iterator:
                logging.info(f"[{response.user_id}]: {response.message}")

        except grpc.RpcError as e:
            logging.error(f"An RPC error occurred: {e}")
        finally:
            logging.info("--- Disconnected from chat ---")
            stop_event.set()


if __name__ == "__main__":
    user = input("Please enter your name: ")
    run_client(user)
