from time import time

class Timer:
    def __init__(self):
        self.__start = time() # Armazena o tempo de inicio (em que ele foi instanciado)
        self.__finish = None # Enquanto não tiver um valor, será None
        
        self.__stopped_time = None # Enquanto não tiver um valor, será None

    def start(self): # Adiciona a possiblidade de começar o timer em um momento em que ele já foi instanciado
        self.__start = time()

    def stop(self):
        self.__finish = time() # Define um tempo para o fim
        self.__stopped_time = self.__finish - self.__start # Calcula o tempo decorrido

    def reset(self):
        self.__init__()

    def set_time(self, set_time):
        self.__start = time() - set_time
    
    # Getters
    @property
    def stopped_time(self):
        return self.__stopped_time
    
    def get_time(self):
        return time() - self.__start # Retorna um float com o tempo decorrido em segundos
    
    def get_formated_time(self):
        time_seconds = self.get_time()
        minutes, seconds = divmod(time_seconds, 60)
        return "{:0>2}:{:05.2f}".format(int(minutes),seconds)