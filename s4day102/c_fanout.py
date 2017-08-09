import pika
credentials = pika.PlainCredentials('root', '123')#证书

parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
connection = pika.BlockingConnection(parameters)#连接

channel = connection.channel() #连接通道
channel.exchange_declare(exchange='logs', type='fanout')#声明收发方式
#channel.exchange_declare(exchange='logs',type='fanout')发和接收方的声明方式要一样

queue_obj = channel.queue_declare(exclusive=True) #不指定queue名字,rabbit会随机分配一个名字,
# exclusive=True会在使用此queue的消费者断开后,自动将queue删除,即每一个queue_obj是唯一的
#queue_obj=channel.queue_declare(exclusive=True)它没有指明queue的名字,所以我们取它的对象,通过该对象取到它的名字
#queue_name=queue_obj.method.queue  取到随机生成的队列名称

#channel.queue_declare(queue='hello3') 它指明了queue的名字
queue_name = queue_obj.method.queue  #获取队列的名称
print('queue name',queue_name,queue_obj)

channel.queue_bind(exchange='logs',queue=queue_name) #绑定队列到Exchange
#channel.queue_bind让声明的队列与广播进行绑定,因为发送端没有队列,队列在接收方,所以要让接收方的队列能收到广播发送的信息,就让它们绑定
print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,queue=queue_name, no_ack=True)
#basic_consume接收信息的配置,callback是回调函数名,queue是队列名,no_ack表示信息不必确认,就被消费完毕了
channel.start_consuming() #等待接收信息