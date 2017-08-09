#topic 表示按规则要求匹配接收方

import pika
import sys

credentials = pika.PlainCredentials('root', '123')

parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

channel.exchange_declare(exchange='topic_log',type='topic')

#log_level =  sys.argv[1] if len(sys.argv) > 1 else 'info'
log_level =  sys.argv[1] if len(sys.argv) > 1 else 'all.info'

message = ' '.join(sys.argv[1:]) or "all.info: Hello World!"

channel.basic_publish(exchange='topic_log',
                      routing_key=log_level,
                      body=message)
print(" [x] Sent %r" % message)
connection.close()