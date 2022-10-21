from time import time

class Timer:
    def __init__(self):
        self.start = time() # Armazena o tempo de inicio (em que ele foi instanciado)
        self.finish = None # Enquanto não tiver um valor, será None
        
        self.stopped_time = None # Enquanto não tiver um valor, será None

    def start(self): # Adiciona a possiblidade de começar o timer em um momento em que ele já foi instanciado
        self.start = time()

    def stop(self):
        self.finish = time() # Define um tempo para o fim
        self.stopped_time = self.finish - self.start # Calcula o tempo decorrido

    def get_stopped_time(self):
        return self.stopped_time

    def get_time_from_start(self):
        return time() - self.start # Retorna um float com o tempo decorrido em segundos
