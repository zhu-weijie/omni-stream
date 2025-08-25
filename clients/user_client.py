import logging
import sys

import grpc


sys.path.append("user_service")
import user_pb2
import user_pb2_grpc


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_client(user_id):
    with grpc.insecure_channel("user_service:50051") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        logging.info(f"--- Client requesting user with id: {user_id} ---")

        try:
            request = user_pb2.UserRequest(user_id=user_id)

            response = stub.GetUser(request)

            logging.info(f"gRPC response received: \n{response}")

        except grpc.RpcError as e:
            logging.error(f"An RPC error occurred: {e}")


if __name__ == "__main__":
    run_client("1")

    print("\n" + "=" * 30 + "\n")

    run_client("2")
