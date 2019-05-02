import time
from google.cloud import pubsub_v1
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gapi_key.json"

project_id = 'striped-impulse-239003'
topic_name = 'cve-search-topic'
subscription_name = "cve-search"


def callback_pub(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        print(message_future.result())


def publish():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        data = data.encode('utf-8')

        message_future = publisher.publish(topic_path, data=data)
        message_future.add_done_callback(callback_pub)

    print('published 10 messages')


def callback_sub(message):
    print('Received message: {}'.format(message))
    message.ack()


def subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    subscriber.subscribe(subscription_path, callback=callback_sub)

    print('Listening for messages on {}'.format(subscription_path))

    # keep this method alive to receive response from callback
    while True:
        time.sleep(60)

# publish()
subscribe()
