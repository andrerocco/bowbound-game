# Bowbound

_Read this in other languages: [English](./README.md), [Português (Brasil)](./README.pt-BR.md)_

Bowbound é um jogo de plataforma 2D construído com PyGame que testa sua agilidade, mira e solução de problemas. Controle um arqueiro e, utilizando sua besta e diferentes flechas, acerte em todos os alvos do nível para conseguir utilizar a porta de saída do nível. Cada nível possui um número de flechas limitado e diferentes tipos de flechas se comportam de maneiras diferentes, portanto, use-as com sabedoria!

Assista a um vídeo de demonstração do jogo através do link abaixo:
[![Bowbound - Demo Gameplay](https://i.ibb.co/4NmXSgG/maxresdefault.jpg)](https://www.youtube.com/watch?v=VmcU-zHWFkY "Bowbound - Demo Gameplay")

O jogo foi construído como o projeto final da disciplina de Programação Orientada a Objetos II (INE5404) ministrada pelos professores [Jônata Tyska](https://www.linkedin.com/in/jonata-tyska-phd/) e [Mateus Grellert](https://www.linkedin.com/in/mateus-grellert-29503356/) do curso de Ciência da Computação da Universidade Federal de Santa Catarina (UFSC).

Internamente, o jogo foi desenvolvido com base nos conceitos da Orientação a Objetos. Diferentes padrões de projeto (como Singleton, Data Access Object, States) foram implementados na sua construção, o que, em conjunto com o uso da Orientação a Objetos, promove a reutilização de código e a manutenibilidade do projeto. Veja mais sobre detalhes de implementação no [relatório de desenvolvimento](./UML/Relat%C3%B3rio%20de%20Desenvolvimento.pdf). Veja o diagrama de classes do projeto em [UML](./UML/Diagrama%20de%20Classes.pdf).

## Como executar o jogo

Para executar o jogo, você precisa ter o Python 3.6 ou superior instalado em sua máquina. Você pode baixar o Python [aqui](https://www.python.org/downloads/). Após a instalação, siga os seguintes passos:

1. Clone o repositório do jogo para sua máquina `git clone https://github.com/andrerocco/bowbound-game.git`
2. Entre na pasta do jogo `cd bowbound-game`
3. Instale as dependências do jogo `pip install -r requirements.txt`
4. Execute o arquivo `main.py` localizado na em `Game\data\main.py`

## Construído com

- [Python](https://www.python.org/) - A linguagem de programação usada
- [PyGame](https://www.pygame.org/news) - A game engine usada