from time import sleep
import redis
import random

redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

class Daemon:
    class Message:
        RECIPIENTS = 0
        MESSAGE = 1

    def __init__(self):
        self.id = random.randint(1787, 9756)
        self.name = f'daemon:{self.id}'
        self.action_key = f'daemon:{self.id}:action'

    def run(self):
        redis_client.set(self.name, 'working')

        while(True):
            command = redis_client.get(self.action_key)
            if not command:
                sleep(1)
                continue
            data = command.split(':')

            recipients = data[self.Message.RECIPIENTS].split(',')

            for recipient in recipients:
                redis_client.set(
                    f'client:{recipient}:message',
                    data[self.Message.MESSAGE]
                )

            redis_client.delete(self.action_key)

    def kill(self):
        redis_client.delete(self.name)
