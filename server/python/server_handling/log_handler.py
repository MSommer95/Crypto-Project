import matplotlib.pyplot as plt
import numpy as np


class LogHandler:

    @staticmethod
    def get_access_log(logs):
        try:
            counter_login = []
            access_log_path = f'./server_handling/logs/{logs}.log'
            with open(access_log_path, 'r') as f:
                for line in f:
                    counter_login.append(LogHandler.get_hour(line))

        except Exception as e:
            print(e)
        else:
            LogHandler.analyse_hours(counter_login)

    @staticmethod
    def get_hour(line):
        inside_brackets = line[line.find("[") + 1:line.find("]")]
        hour = inside_brackets.split(':')[1]
        return hour

    @staticmethod
    def analyse_hours(hours):
        hours = np.sort(hours)
        plt.hist(hours, 100,
                 density=True,
                 histtype='bar',
                 facecolor='b',
                 alpha=0.5)

        plt.show()
