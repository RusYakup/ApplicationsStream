#!/bin/bash

set -e

echo "Creating topics..."
/opt/bitnami/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 \
                                       --replication-factor 1 --partitions 1 \
                                       --topic new_applications
echo "Topics created successfully."