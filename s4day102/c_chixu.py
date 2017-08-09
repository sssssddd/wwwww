
# import pika
#
# credentials = pika.PlainCredentials('root', '123')
#
# parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
# connection = pika.BlockingConnection(parameters)
#
# channel = connection.channel() #队列连接通道
#
#
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % ch, method, properties, body)
#
# channel.basic_consume(callback, #取到消息后，调用callback 函数
#                       queue='hello2',
#                       no_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming() #阻塞模式
################
"""
import pika
credentials=pika.PlainCredentials('root','123')#证书
parameters=pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)#参数
conn=pika.BlockingConnection(parameters)#通过参数建立连接
channel=conn.channel()  #通过连接建立通道

def callback(ch,method,prop,body):
    print('ch is %s ,method is (%s),prop is (%s),body is %s'%(ch,method,prop,body))
    #ch 是pika的连接对象,method是连接的客户设置信息,
    #prop代指properties参数, body 是P端发送来的信息,是bytes类型

channel.basic_consume(callback, #取到消息后,调用callback函数
                      queue='hello2',
                      no_ack=True) #它表示不必通过消息确认,就从队列中删除信息
#channel.basic_consume  用于在通道中接收信息,queue 指定接收信息的队列,它是设置接收信息的配置要求
print('Waiting for messages')
channel.start_consuming() #等待P端传来的数据,如果得到数据,就执行callback函数,它才是真正的等待接收,它是阻塞模式
conn.close()
"""
###########信息的持久化,指的是如果接收发没有接收数据,则数据一直在队列中,只有接收方接收数据同时把数据从
###########从队列中删除,才会消失
import pika
import time

credentials = pika.PlainCredentials('root', '123')#证书

parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)#参数
connection = pika.BlockingConnection(parameters)#连接ribbitmq服务

channel = connection.channel() #连接通道


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(2)
    print('msg handle done...',body)
    print(method.delivery_tag) #method.delivery_tag 表示接收相关设置中,method.delivery_tag默认为1
    ch.basic_ack(delivery_tag=method.delivery_tag) #把通道中的指定队列的接收到的数据删除掉,即消息已消费完毕
#根据接收者处理数据的能力不同,发送给接收者的任务个数不同,在设置接收信息之前,设置接收者处理任务的情况
channel.basic_qos(prefetch_count=1)#使用basic.qos方法,prefetch_count=1表示rabbitmq同一时刻,给接收者
#发送的任务不会超过1个消息,即接收者只能处理完数据后才能接收新的数据
channel.basic_consume(callback, #取到消息后，调用callback 函数
                      queue='task1',)#接收的队列
                      #no_ack=True) #消息处理后，不向rabbit-server确认消息已消费完毕
#basic_consume表示接收的相关设置
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming() #阻塞模式 start_consuming等待接收数据