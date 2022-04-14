# Alinha-PB

Alinha-PB foi desenvolvido para facilitar a conversão em fonemas de frases e o alinhamento fonético forçado, e para o treinamento e alinhamento dos modelos foram usados: HTKToolkit, Kaldi, Prosodylab-Aligner e Montreal Forced Aligner

Esse repositório contém modelos treinados para:
- HTK (treinado diretamente com HTKToolkit)
- ProsodyLab_Aligner (treinado usando o prosodylab aligner)
- Montreal_Forced_Aligner (treinado usando o montreal forced aligner)

na pasta Models, além do código fonte do site de conversão e alinhamento na pasta src.

Todos os modelos foram treinados usando a representação em ASCII dos fonemas.

## Rodando o site localmente
### Método Simples
A forma mais simples de executar o site localmente é utilizando docker. Para isso, inicialmente é necessário instalar Docker no seu dispositivo, o que pode ser feito seguindo os passos em https://docs.docker.com/engine/install/ para o seu sistema operacional. Feito isso uma imagem já configurada com o programa funcional pode ser obtida usando o comando ``docker pull jkruse27/alinhapb`` ou fazendo o push da imagem do repositório jkruse27/alinhapb no docker hub usando a interface gráfica. Com isso, basta executar usando o comando ``docker run -p 5000:5000 jkruse27/alinhapb`` ou através da interface gráfica (lembre de configurar na sessão de Ports nas configurações adicionais o Local Host como 5000). Com isso, o site já pode ser acessado entrando na url 127.0.0.1:5000  .

### Outro Método
Para instalar o site e executá-lo localmente (recomendado especialmente quando lidando com alinhamentos de áudios longos), basta instalar a versão para o sistema operacional desejado nos Releases, extraí-la e seguir os passos abaixo. O site roda em um servidor em Flask, logo enquanto o servidor roda no terminal o site é acessado pelo navegador.

Com exceção dos códigos do HTKToolskit, o site todo é feito em Python, portanto é necessário certificar-se de que você possui uma versão posterior a 3.6 de Python instalada na sua máquina. Para instalar as dependências necessárias, basta executar o comando 
É necessário ter o HTKToolkit instalado também, o que pode ser feito aqui https://htk.eng.cam.ac.uk/ e o Montreal Forced Aligner, o que pode ser obtido aqui https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner.

`pip install -r requirements.txt`

**!!Atenção!!** Tanto para windows quanto para linux é importante manter o executável em uma pasta própria e contendo somente ele.

**!!Atenção!!** Para o uso no Windows, a instalação do Python realizada pela Microsoft Store as vezes resulta em problemas na execução, portanto é importante instalá-lo a partir dos executáveis do site oficial ([https://www.python.org/]).

### Linux

Com as dependências já instaladas, para começar o site basta abrir um terminal, ir até a pasta na qual se encontra o executável 'server' e executá-lo (`./server`). Isso iniciará o servidor (pode demorar alguns segundos), de modo que agora é possível abrir o site em um navegador de sua escolha indo ao link 0.0.0.0:5000 (link aparecerá no terminal também assim que o servidor iniciar). É importante ressaltar que o terminal precisa ficar aberto e executando o servidor enquanto o site estiver sendo utilizado.

### Windows

A execução para Windows funciona de forma muito semelhante que a para Linux, mas ao invés de precisar abrir no terminal, basta executar o arquivo server.exe, que abrirá um terminal no qual o servidor rodará (pode demorar alguns segundos). A partir daí é só entrar no site pelo navegador de sua escolha através do link 127.0.0.1:5000 (link aparecerá no aplicativo também assim que o servidor iniciar).





Os executáveis foram testados apenas para Ubuntu 16.04 e Windows 10 usando Python3.7
