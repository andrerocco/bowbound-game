# Essa implementação de singleton previne que a função inicializadora das instâncias seja chamada mais de uma vez.
# A implementação com o uso de __new__ faria com que, apesar de não ser possível criar mais de uma instância da classe,
# a função inicializadora fosse chamada para cada instância criada.

class Singleton(type):
    def __init__(self, name, bases, mmbs):
        super(Singleton, self).__init__(name, bases, mmbs)
        self._instance = super(Singleton, self).__call__()

    def __call__(self, *args, **kw):
        return self._instance