import logging
import time
from concurrent import futures
from datetime import datetime, UTC

import grpc

import event_pb2
import event_pb2_grpc


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class EventServiceServicer(event_pb2_grpc.EventServiceServicer):
    def SubscribeToGameEvents(self, request, context):
        logging.info(f"Received subscription request for game_id: {request.game_id}")

        for i in range(1, 6):
            event = event_pb2.GameEvent(
                event_id=f"event-{i}",
                description=f"Player scores in game {request.game_id}!",
                timestamp=datetime.now(UTC).isoformat(),
            )
            logging.info(f"Streaming event {event.event_id} to client...")
            yield event
            time.sleep(2)

        logging.info(f"Finished streaming events for game_id: {request.game_id}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    event_pb2_grpc.add_EventServiceServicer_to_server(EventServiceServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    logging.info("Event Service listening on port 50052")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
