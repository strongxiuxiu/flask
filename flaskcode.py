from threading import Thread
from flask import Flask
app = Flask(__name__)


task_information = [] # 新建task_information列表用来作为任务信息存放的列表
task_ack = []  # 新建task_ack列表用来作为任务确认的列表

@app.route('/')
def hello_world():

    global task_information   #  设置全局变量是为了task1和task2都可以共同去使用它。
    global task_ack
    task_information.append('data')  # 主要的程序接受到任务后，将它需要处理的信息放入任务信息管道当中
	return 'Hello World!'


def task1():
	while 1:
		if task_information: # 这个位置处理循环的处理task_information里面的信息
			print(task_information) # 这里的打印换成实际的工作，更新数据库，或者别的什么处理
			task_information.clear() # 处理完成后，清除任务信息的全局变量。
			task_ack.append(1)
		else:
			time.sleep(5)
    return 'Hello World1!'

def task2():
	while 1:
		if task_ack:  # 如果处理任务后的数据，确认之后，我们继续下一步操作
			print(task_ack) # 这里的打印换成实际的工作，写入日志，或者别的什么处理
			task_ack.clear() # 处理结果成功，清除任务确认的全局变量。
		else:
			time.sleep(5)	
    return 'Hello World2!'

class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
	
if __name__ == "__main__":
    t1 = MyThread(task1, args=())
    t2 = MyThread(task2, args=())

    t1.start()
    t2.start()
	app.run() 


	
