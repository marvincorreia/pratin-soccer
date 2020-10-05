# Pratinhos Soccer

Jogo de caricas, mais conhecido por "**Pratin**" em Cabo Verde.

# Sobre
Projeto educacional de **desenvolvimento de jogos** utilizando a
biblioteca pygame no Python.

# Pré requisitos

- [Git](https://git-scm.com/)
- [Python 3.7](https://www.python.org/downloads/release/python-370/)

# Instalação

### Clonando o repositório ###
Antes de configurar o ambiente virtual para o projeto, primeiro deve-se ter clonado
o repositório no github para sua máquina local e entrar na pasta raiz do projeto.

```
https://github.com/marvincorreia/pratin-soccer.git
cd pratin-soccer
```

### Pipenv ###
O projeto tem como dependência principal o python 3.7
 e utiliza para esse efeito o gerenciador de dependências chamado [pipenv](https://pypi.org/project/pipenv/),
criado por Kenneth Reitz e que se tornou no recurso oficial recomendado para 
gerenciar dependências no Python.

O *pipenv* pode ser instalado através do *pip* via terminal ou bash:

```
pip install pipenv
``` 
ou 
```
sudo apt install pipenv
```

O projeto possui 2 ficheiros, [Pipfile](https://github.com/marvincorreia/pratin-soccer/blob/master/Pipfile) 
e [Pipfile.lock](https://github.com/marvincorreia/pratin-soccer/blob/master/Pipfile.lock),
onde estão documentados as dependencias do projeto.

Após ter clonado o repositório basta configurar o ambiente virtual usando o pipenv,
apartir do diretorio raiz do projeto:

**OBS:** *Apartir deste ponto os comandos devem ser executados dentro da pasta raiz do projeto **/pratin-soccer** *

***Criar ambiente virtual python para o projeto:***
 
```
pipenv --python 3.7
```

output:

```
Successfully created virtual environment!
Virtualenv location:C:\Users\Marvin Correia\.virtualenvs\pratin-soccer-n2ymFxe7
```

Instalar as dependencias especificadas no ficheiro Pipfile.lock para o ambiente:

```
pipenv sync
```

Após o download dos packages de dependencia, o ambiente estará configurada para rodar
a aplicação web.

# Testando o jogo
Estando no diretório raiz do projeto */pratin-soccer* execute
```
pipenv run python pratin-soccer.py
```
Agora é só jogar...

Jogabilidade:

![Game Play](https://github.com/marvincorreia/pratin-soccer/blob/master/data/game_play/gameplay.png)

Menu:

![Menu](https://github.com/marvincorreia/pratin-soccer/blob/master/data/game_play/menu.png)

Bolas e estádios:

![Ball-Stadium](https://github.com/marvincorreia/pratin-soccer/blob/master/data/game_play/ball-stadium.png)

Equipas:

![Teams](https://github.com/marvincorreia/pratin-soccer/blob/master/data/game_play/team.png)

Créditos:

![Credits](https://github.com/marvincorreia/pratin-soccer/blob/master/data/game_play/credits.png)


