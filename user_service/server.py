import logging
from concurrent import futures

import grpc
import user_pb2
import user_pb2_grpc


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        logging.info(f"Received GetUser request for user_id: {request.user_id}")

        if request.user_id == "1":
            return user_pb2.User(user_id="1", name="Alice", level=10)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with id '{request.user_id}' not found.")
            return user_pb2.User()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)

    server.add_insecure_port("[::]:50051")

    server.start()
    logging.info("User Service listening on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
