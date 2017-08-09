#进行一对一的收发消息的队列

#1 。 定义fib函数
#2. 声明接收指令的队列名rpc_queue
#3. 开始监听队列，收到消息后 调用fib函数
#4 把fib执行结果，发送回客户端指定的reply_to 队列
import subprocess
import pika

credentials = pika.PlainCredentials('root', '123')

parameters = pika.ConnectionParameters(host='192.168.11.143',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

channel.queue_declare(queue='rpc_queue2')#声明了一个队列,队列的名子是rpc_queue2

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def run_cmd(cmd):
    cmd_obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = cmd_obj.stdout.read() + cmd_obj.stderr.read()

    return result


def on_request(ch, method, props, body):
    cmd = body.decode("utf-8")
    #ch就是channel的对象所赋值
    print(" [.] run (%s)" % cmd)
    response = run_cmd(cmd)
    #props.correlation_id是接收到的properties中额外设置的数据
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to, #队列
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    #basic_publish发送设置配置和发送信息
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(on_request, queue='rpc_queue2')
#设置接收数据的配置,第一个参数是回调函数,queue是队列名称

print(" [x] Awaiting RPC requests")
channel.start_consuming()  #等待接收数据