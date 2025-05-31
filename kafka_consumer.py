from confluent_kafka import Consumer
import json

conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'json-consumer-group-new',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['pg.public.products'])

print("🟢 Listening for messages on 'pg.public.products'...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("❌ Error: {}".format(msg.error()))
            continue

        data = json.loads(msg.value().decode('utf-8'))
        print("✅ Received:")
        print(json.dumps(data, indent=2))

except KeyboardInterrupt:
    print("⛔ Stopping consumer.")
finally:
    consumer.close()
