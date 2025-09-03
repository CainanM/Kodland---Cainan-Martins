-----

# KODLAND TEST: Jogo de Plataforma

Um jogo de plataforma 2D simples desenvolvido em Python com a biblioteca Pygame Zero. O objetivo é guiar o herói por uma fase cheia de inimigos e alcançar a porta no final para vencer.

-----

## 📜 Sobre o Jogo

Este projeto é um jogo de plataforma clássico onde o jogador controla um personagem que pode correr e pular. O desafio é navegar pelo cenário, subir em plataformas e desviar de diferentes tipos de inimigos, cada um com um comportamento único. O jogo possui um menu inicial, música, efeitos sonoros e telas de vitória e derrota.

-----

## ✨ Funcionalidades

  - **Movimentação Fluida:** Personagem com física básica, incluindo gravidade e pulo.
  - **Animações:** Sprites animados para o herói (parado, correndo, pulando) e para os inimigos.
  - **Inimigos com IA Simples:**
      - **Patrulheiro:** Move-se de um lado para o outro.
      - **Saltador:** Pula em intervalos regulares.
      - **Perseguidor:** Persegue o jogador quando ele se aproxima.
  - **Menu Interativo:** Menu principal com opções para iniciar, ativar/desativar música e sons, e sair.
  - **Múltiplos Estados de Jogo:** Menu, Jogando, Game Over e Vitória.
  - **Áudio:** Música de fundo e efeitos sonoros para pulo e derrota.

-----

## 🚀 Tecnologias Utilizadas

  - **Python 3**
  - **Pygame Zero:** Um framework para iniciantes construído sobre a biblioteca Pygame para facilitar o desenvolvimento de jogos.

-----

## 📂 Estrutura de Arquivos

Para que o jogo funcione corretamente, os arquivos de recursos (imagens, sons, etc.) devem estar organizados nas seguintes pastas dentro do diretório do projeto:

```
seu_projeto/
├── jogo.py      
├── images/
│   ├── hero_idle_0.png
│   ├── hero_run_0.png
│   ├── hero_run_left_0.png
│   ├── ... 
│   ├── enemy_patrol_0.png
│   ├── enemy_jumper_0.png
│   ├── enemy_chaser_0.png
│   ├── ... 
│   ├── door.png
│   └── background.png
├── sounds/
│   ├── jump.wav
│   └── death.wav
├── music/
│   └── background.mp3
└── fonts/
    └── upheaval.ttf
```
-----

## ⚙️ Como Executar

1.  **Pré-requisitos:** Certifique-se de ter o Python 3 instalado em seu sistema.

2.  **Instale o Pygame Zero:** Abra o seu terminal ou prompt de comando e execute o seguinte comando:

    ```bash
    pip install pgzero
    ```

3.  **Clone ou baixe o projeto:** Coloque todos os arquivos (código e pastas de recursos) em um mesmo diretório.

4.  **Execute o jogo:** Navegue até a pasta do projeto pelo terminal e execute o comando:

    ```bash
    pgzrun jogo.py
    ```

-----

## 🎮 Controles

  - **Seta Esquerda / Tecla A:** Mover para a esquerda
  - **Seta Direita / Tecla D:** Mover para a direita
  - **Barra de Espaço:** Pular

-----

## 👤 Autor

  * **Cainan Martins**
