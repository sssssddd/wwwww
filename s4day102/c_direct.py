#direct表示发送方式是组播,即给摸个组进行发送,但是必须接收方在线

import pika,sys
credentials = pika.PlainCredentials('root', '123')

parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

queue_obj = channel.queue_declare(exclusive=True) #不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
queue_name = queue_obj.method.queue
print('queue name',queue_name,queue_obj)

log_levels = sys.argv[1:] # info warning errr  #取脚本之后所有的参数

if not log_levels:#如果没有参数,则表示没有接收组,所以就报错了
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)


for level in log_levels:
    channel.queue_bind(exchange='direct_log',
                       queue=queue_name,
                       routing_key=level) #绑定队列到Exchange
#作用是只有接收方在其中一个组中都能接收到信息,可能有多个组,所以就用遍历
print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,queue=queue_name, no_ack=True)

channel.start_consuming()