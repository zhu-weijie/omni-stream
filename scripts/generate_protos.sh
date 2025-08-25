#!/bin/bash

set -e

PROTO_DIR=./protos

USER_SERVICE_DIR=./user_service
EVENT_SERVICE_DIR=./event_service
CHAT_SERVICE_DIR=./chat_service

mkdir -p $USER_SERVICE_DIR $EVENT_SERVICE_DIR $CHAT_SERVICE_DIR

python3 -m grpc_tools.protoc \
  -I$PROTO_DIR \
  --python_out=$USER_SERVICE_DIR \
  --pyi_out=$USER_SERVICE_DIR \
  --grpc_python_out=$USER_SERVICE_DIR \
  $PROTO_DIR/user.proto

python3 -m grpc_tools.protoc \
  -I$PROTO_DIR \
  --python_out=$EVENT_SERVICE_DIR \
  --pyi_out=$EVENT_SERVICE_DIR \
  --grpc_python_out=$EVENT_SERVICE_DIR \
  $PROTO_DIR/event.proto

python3 -m grpc_tools.protoc \
  -I$PROTO_DIR \
  --python_out=$CHAT_SERVICE_DIR \
  --pyi_out=$CHAT_SERVICE_DIR \
  --grpc_python_out=$CHAT_SERVICE_DIR \
  $PROTO_DIR/chat.proto

echo "Protobuf Python files generated successfully."
