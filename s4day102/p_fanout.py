#fanout是指发送方式,它是广播类型,在执行前,必须有接收者
import pika
import sys

credentials = pika.PlainCredentials('root', '123')

parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #连接通道

channel.exchange_declare(exchange='logs',type='fanout')#声明发送的方式是广播,
#exchange_declare声明发送方式,参数exchange 给方式方式取别名,type是发送方式类型
#fanout是广播类型

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
#sys.argv[1:]表示通过执行脚本后获取脚本后的参数
#or  的作用是如果''.join()是空,就选择or后面的即'info :Hello'

channel.basic_publish(exchange='logs',#用logs代指设置好的方式
                      routing_key='',#因为是广播,所有没有声明队列,
                      body=message)#body是发送的信息
#basic_publish发送信息,及其设置,广播是向开启的所有接受者发信息,所有没有指明队列
print(" [x] Sent %r" % message)
connection.close()