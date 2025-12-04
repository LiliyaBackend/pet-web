# Connection details for the ActiveMQ broker
import time

import stomp

BROKER_HOST = 'localhost'
BROKER_PORT = 61613

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print(f"Error: {frame}")

    def on_message(self, frame):
        if frame.cmd != 'MESSAGE':
            print(f"Received invalid message frame {frame}")
            return

        order = frame.body
        print(f"Received order: {order}")


# The auto_content_length parameter should be set to False to send Text message instead of Binary
conn = stomp.Connection([("localhost", 61613)], auto_content_length=False)
conn.set_listener('', MyListener(conn))
conn.connect('admin', 'admin', wait=True)
conn.subscribe(destination="shop06.orders.for.approve.json", id='1')

try:
    print("Waiting for messages... Press Ctrl+C to exit.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Disconnect from the broker
    conn.disconnect()
