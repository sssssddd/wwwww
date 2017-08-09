#topic 表示按规则要求匹配接收方

import pika,sys
credentials = pika.PlainCredentials('alex', 'alex3714')

parameters = pika.ConnectionParameters(host='192.168.11.106',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

queue_obj = channel.queue_declare(exclusive=True) #不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
queue_name = queue_obj.method.queue#获取rabbitmq分配给queue的名子


log_levels = sys.argv[1:] # info warning errr
########注如果是要使接收端在任何匹配下都接收到数据用'#'
if not log_levels:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)


for level in log_levels:
    channel.queue_bind(exchange='topic_log',
                       queue=queue_name,
                       routing_key=level) #绑定队列到Exchange

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,queue=queue_name, no_ack=True)  #收数据的设置

channel.start_consuming() #等待接收数据