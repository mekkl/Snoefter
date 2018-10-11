import multiprocessing
import time
import requests
import threading
import logging
from datetime import datetime
import sys

 
class Producer():
 
    def __init__(self, task_queue, num_consumers, url, num_requests=5, runtime=15):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.url = url
        self.runtime = runtime
        self.num_consumers = num_consumers
        self.num_requests = num_requests
        self.timer = 0
        self._count_timer = 0

    def _start_timer(self):
        self._count_timer = time.time()
    
    def _get_time(self):
        self.timer += time.time() - self._count_timer
        self._count_timer = time.time()
        return self.timer
 
    def _work(self):
        '''
        DEF: 
        '''
        TIME_INTERVAL = 1
        current_time = self._get_time()
        if self.runtime > current_time:
            # TODO: change to class attribute
            make_n_request = int(.4 * current_time ** 2 + 3)
            make_n_request = 1 # TODO: remove
            thread = threading.Timer(TIME_INTERVAL, self._work)
            thread.daemon = True # DAEMON COMMENT
            thread.start()

            # Enqueue jobs
            for _ in range(make_n_request):
                self.task_queue.put(Task(self.url))
            print(f'Producer: {make_n_request} urls added to task_queue at {round(self._get_time(),2)} runtime')
        else:
            # Add a poison pill for each consumer
            for _ in range(self.num_consumers):
                self.task_queue.put(None)

    def run(self):
        self._start_timer()
        print(f'Producer: starting work...')
        self._work()

class Consumer(multiprocessing.Process):
    '''
    DEF: 
    '''
    def __init__(self, task_queue, result_queue, daemon=True):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.daemon = daemon
    
    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print(f'{proc_name}: received a poison pill - Terminating...')
                self.task_queue.task_done()
                break
            # DEBUG print(f'{proc_name}: {next_task}')
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
 
class Task:
    """The summary line for a class docstring should fit on one line.

    Attributes:
        url (str): Description of url

    """
    def __init__(self, url):
        """
        Note:
            ''

        Args:
            url (str): Description of `url`.

        """
        self.url = url
 
    def __call__(self):
        epoch_time = time.time() # start timer
        response = requests.get(self.url) # url to ping
        epoch_time = time.time() - epoch_time  # stop timer
        status = response.status_code
        timestamp = datetime.now()

        task_result = f' timestamp: {timestamp}, status_code: {status}, request_epoch_(sec): {epoch_time}'

        return task_result
 
    def __str__(self):
        return f'requesting {self.url}'
 
 
class HttpTraffic:

    def __init__(self, url, runtime, timeout = 10):
        self.runtime = runtime
        self.url = url
        self._count_timer = 0
        self.timer = 0
        self.timeout = timeout
    
    def _start_timer(self):
        self._count_timer = time.time()
    
    def _get_time(self):
        self.timer += time.time() - self._count_timer
        self._count_timer = time.time()
        return self.timer

    def _setup(self):
        # Establish communication queues
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()

        # SETUP CONSUMER
        num_consumers = multiprocessing.cpu_count() * 2
        print(f'Creating {num_consumers} consumers...')
        consumers = [
            Consumer(tasks, results)
            for i in range(num_consumers)
        ]

        # SETUP PRODUCER
        producer = Producer(tasks, num_consumers, url=self.url, runtime=self.runtime)

        return tasks, results, producer, consumers

    def start(self):
        # SETUP
        _, results, producer, consumers = self._setup()

        # START CONSUMERS
        for c in consumers:
            c.start()
        print(f'All consumers started..\n')

        # START PRODUCER
        producer.run()

        # Setup logger
        logging.basicConfig(filename='traffic_sim.log', level=logging.INFO)


        # Start printing/logging results
        while True:
            try:
                result = results.get(timeout=self.timeout)
                logging.log(logging.INFO, result)
                print('Result:', result)
            except Exception as _:
                print(f'timeout ({self.timeout} sec) for multiprocessing.Queue().get(timeout={self.timeout})')
                break

        print('done')


if __name__ == '__main__':

    try:
        MAX_RUNTIME = 1000
        URL = 'http://167.99.129.215:8081'
        simulator = HttpTraffic(URL, MAX_RUNTIME)
        simulator.start()
    except KeyboardInterrupt:
        sys.exit(0) # or 1, or whatever
    