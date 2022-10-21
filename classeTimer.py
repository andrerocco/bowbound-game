import time


class Timer:
    def __init__(self):
        self.start = time.time() # Armazena o tempo de inicio
        self.finish = None # Enquanto não tiver um valor, será None

    def getTimer(self):
        return time.time() - self.start # Retorna o tempo atual do level

    def setFinish(self):
        self.finish = time.time() - self.start # Quando o jogador passa de level usará esse metodo para gravar o tempo

    def getLevelTime(self):
        return self.start - self.finish # Retorna o tempo total do level para o uso dos scores