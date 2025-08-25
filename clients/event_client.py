import logging
import sys

import grpc


sys.path.append("event_service")
import event_pb2
import event_pb2_grpc


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_client():
    with grpc.insecure_channel("event_service:50052") as channel:
        stub = event_pb2_grpc.EventServiceStub(channel)
        game_id = "game-123"
        logging.info(f"--- Subscribing to events for game: {game_id} ---")

        try:
            request = event_pb2.EventRequest(game_id=game_id)

            response_stream = stub.SubscribeToGameEvents(request)

            logging.info("Successfully subscribed. Waiting for events...")
            for event in response_stream:
                logging.info(
                    f"Received event: {event.description} (ID: {event.event_id})"
                )

            logging.info("--- Event stream finished ---")

        except grpc.RpcError as e:
            logging.error(f"An RPC error occurred: {e}")


if __name__ == "__main__":
    run_client()
