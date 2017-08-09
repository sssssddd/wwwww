
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