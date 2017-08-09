
# import pika
#
# credentials = pika.PlainCredentials('root', '123')#
#
# parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
# connection = pika.BlockingConnection(parameters)
#
# channel = connection.channel() #队列连接通道
#
# #声明queue
# channel.queue_declare(queue='hello2')
#
# channel.basic_publish(exchange='',
#                       routing_key='hello2', #路由
#                       body='Hello World2  xiaoyang!')
#
# print(" [x] Sent 'Hello World!'")
#
#
# connection.close()
import pika  #pika 用于连接ribbitmq的,而ribbitmq是一个中间服务,是用于p与c连接的中间服务
credentials=pika.PlainCredentials('root','123') #证书,即要连接的ribbitmq的用户和用户密码
parameter=pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
#通过参数host赋值ip和credentials赋值证书确定要连接的ribbitmq对象,把它们整体当成pika的参数
conn=pika.BlockingConnection(parameter)  #通过pika的参数(要连接的准备对象)建立一个连接
channel=conn.channel()  #建立连接通道

channel.queue_declare(queue='hello2') #在连接通道中申明队列,并给队列取名hello2,用hello2代指该队列
channel.basic_publish(exchange='',    #exchange是发送信息的方式,是广播,组播,还是一对一,为空是一对一
                      routing_key='hello2',  #routing_key指定该通道中的队列
                      body='ni hao xiaoyang!') #body是要发送的信息
#channel.basic_publish  通过通道发送信息,
print('P sent successful')