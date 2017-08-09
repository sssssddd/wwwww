#direct表示发送方式是组播,即给摸个组进行发送,但是必须接收方在线

import pika
import sys

credentials = pika.PlainCredentials('root', '123')

parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

channel.exchange_declare(exchange='direct_log',type='direct')

log_level =  sys.argv[1] if len(sys.argv) > 1 else 'info'#指明是哪个组,即要向哪个组发送信息

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange='direct_log',
                      routing_key=log_level,#指定组名,以组名代指队列名
                      body=message)
print(" [x] Sent %r" % message)
connection.close()