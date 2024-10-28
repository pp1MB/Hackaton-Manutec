# Hackaton Tractian - Manutec

## Descrição

Este projeto é uma aplicação de gerenciamento de tarefas que permite aos usuários carregar áudios para transcrição, visualizar e gerenciar uma checklist de tarefas, e realizar buscas por ferramentas. A interface foi desenvolvida usando Python e Tkinter, oferecendo uma experiência de usuário intuitiva e interativa.

## Funcionalidades

- **Transcrição de Áudio**: Carregue arquivos de áudio (somente `.ogg`) e obtenha a transcrição das instruções contidas no áudio.
- **Geração de checklist**: Seja com a descrição do audio gerada, ou um texto proprio, gere tasks automaticamente, com a API do Chat GPT.
- **Checklist de Tarefas**: Visualize e marque tarefas em uma checklist. 
- **Busca de Ferramentas**: Pesquise ferramentas específicas e veja os resultados na interface.
- **Gerenciador de ferramentas**: Gerencie quem está utilizando as ferramentas em qual horário com o executável no terminal.

## Tecnologias Utilizadas

- Python
- Tkinter (para a interface gráfica)
- Pydub (para manipulação de áudio)

## Requisitos

Antes de executar o projeto, certifique-se de ter o seguinte instalado:

- Python 3.x
- Pydub
- ffmpeg (necessário para manipulação de arquivos de áudio)
- PIL
- tkinter (para exibição da interface)
- openai (Para GPT API)
