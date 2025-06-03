from confluent_kafka import Consumer
import json

conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'json-consumer-group-2',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
print("🔌 Subscribing to Kafka topic...")
consumer.subscribe(['pg.public.products'])

print("🟢 Listening for new changes on 'pg.public.products'...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("❌ Error: {}".format(msg.error()))
            continue

        try:
            data = json.loads(msg.value().decode('utf-8'))
            op = data.get("op")

            if op in ("c", "u", "d"):
                print(f"🔔 Change detected (op = {op}):")
                print(json.dumps(data, indent=2))
            else:
                # Snapshot, ignore
                continue

        except Exception as e:
            print(f"⚠️  Failed to parse message: {e}")
            continue

except KeyboardInterrupt:
    print("⛔ Stopping consumer.")
finally:
    consumer.close()
