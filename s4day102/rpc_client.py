#进行一对一的收发消息的队列
#client客户端发送指令,服务端执行指令,并把结果返回给客户端,即客户端通过一个队列发送,在通过一个队列接收

# 1.声明一个队列，作为reply_to返回消息结果的队列
# 2.  发消息到队列，消息里带一个唯一标识符uid，reply_to
# 3.  监听reply_to 的队列，直到有结果
import queue

import pika
import uuid

class CMDRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('root', '123')#证书
        parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)#参数
        self.connection = pika.BlockingConnection(parameters) #建立连接
        self.channel = self.connection.channel() #建立通道

        result = self.channel.queue_declare(exclusive=True) #生成一个不指定名称的queue对象
        self.callback_queue = result.method.queue #命令的执行结果的queue,获取rabbitmq分配给queue对象的名字

        #声明要监听callback_queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)#设置接收数据的配置(回调函数名,queue队列名,on_ack是否确认)

    def on_response(self, ch, method, props, body):
        """
        收到服务器端命令结果后执行这个函数
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        if self.corr_id == props.correlation_id:
            self.response = body.decode("gbk") #把执行结果赋值给Response

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4()) #唯一标识符号
        self.channel.basic_publish(exchange='',#进行一对一发送
                                   routing_key='rpc_queue2',#要发送时通过的队列名,在client端没有,在server肯定要有,且先启动server端
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),#properties设置额外要发送的信息,同时方便在接收端读取
                                   body=str(n)) #body要发送的信息
        #basic_publish是设置发送的配置,同时还能进行发送信息

        while self.response is None:
            self.connection.process_data_events()  #检测监听的队列里有没有新消息，如果有，收，如果没有，返回None
            #检测有没有要发送的新指令
        return self.response

cmd_rpc = CMDRpcClient()

print(" [x] Requesting fib(30)")
response = cmd_rpc.call('ipconfig')

print(response)
