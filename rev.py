import requests,json
from threading import Thread
from queue import Queue

        
class Worker(Thread):
  def __init__(self, tasks):
      Thread.__init__(self)
      self.tasks = tasks
      self.daemon = True
      self.start()

  def run(self):
      while True:
          func, args, kargs = self.tasks.get()
          try: func(*args, **kargs)
          except Exception as e: print(e)
          self.tasks.task_done()

class ThreadPool:
  def __init__(self, num_threads):
      self.tasks = Queue(num_threads)
      for _ in range(num_threads): Worker(self.tasks)

  def add_task(self, func, *args, **kargs):
      self.tasks.put((func, args, kargs))

  def wait_completion(self):
      self.tasks.join()
      
class Reverse:
        
    def __init__(self, iplist, server):
        self.endpoint = "http://167.99.72.29:8080/api/"
        self.api_key = "" # <- Paste ur apikey
        self.tmp_ip = []
        self.result = []
        self.ip = iplist
        self.server = server
        
    def test_network(self):
        try:requests.get(self.endpoint, timeout=10)
        except:raise Exception("Server Down")
        
    def reverse(self, ips):
        if ips not in self.tmp_ip:
            self.tmp_ip.append(ips)
            headers = {"X-API-KEY":self.api_key,'Content-Type': 'application/x-www-form-urlencoded'}
            data = {"ip" : ips, "server" : self.server}
            req = requests.post(self.endpoint + "reverse", json=data, headers=headers)
            js = json.loads(req.text)
            total = js["data"]["domain"]
            for x in js["data"]["domain"]:self.result.append(x);open(f"server-{self.server}.txt", "a+").write(x)
            print(f"Ip {ips} , have {len(total)} Domain")
        else:print("IP :" + ips + " SAME IP") 
        
    def execute(self, thread):
        pool = ThreadPool(int(thread))
        for url in self.ip:
            self.ip = url
            pool.add_task(self.reverse, self.ip)
        pool.wait_completion()
        print(f"Task Done , total : {len(self.result)} domain")
        
class Menu:
    
    def input_list(self):
        ip = open(input("list : "), encoding="utf8" ).read().splitlines()
        server = input("Choose Server (one-eleven): ")
        return ip , server
    
try:
    print("""Available Server : one,two,three,four,five,six,seven,eight,nine,ten,eleven \nCredit @Real_Zeru_nishimura""")
    menu = Menu()
    ip , server = menu.input_list()
    thread = input("Thread: ")
    rev = Reverse(ip, server).execute(int(thread))
except KeyboardInterrupt:
    print("Bye")
    exit()
