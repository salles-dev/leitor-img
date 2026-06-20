Markdown


# 🔍 Leitor de Texto Nativo (Snipping OCR)

Um utilitário leve e ultraveloz escrito em Python para capturar regiões da tela e extrair textos (OCR) diretamente para a área de transferência (`Ctrl + V`). 

Ao contrário de outras soluções pesadas que exigem a instalação de motores externos (como o Tesseract OCR), este script utiliza a **API nativa de OCR do Windows 10/11**. Isso garante uma inicialização instantânea e **0% de consumo residual de CPU/RAM**, já que o processo é encerrado por completo após cada captura.

---

## 🛠️ Pré-requisitos & Instalação

Como o projeto utiliza as ferramentas do próprio sistema operacional, a lista de dependências é bastante reduzida.

1. Certifique-se de que você tem o **Python 3.10 ou superior** instalado.
2. Abra o terminal na pasta do projeto e instale os módulos necessários:

```bash
pip install pyautogui pyperclip winrt-Windows.Media winrt-Windows.Graphics
Nota: O motor de OCR utiliza os idiomas instalados no seu perfil do Windows. Se precisar reconhecer textos em inglês, espanhol, etc., certifique-se de que possui esses pacotes de idioma instalados nas configurações de idioma do seu Windows.

🚀 Como Configurar o Atalho (Sem abrir o terminal)
Para usar a ferramenta de forma prática no dia a dia, o ideal é configurar um atalho global do Windows para que ela seja executada em segundo plano de forma 100% invisível.

Passo 1: Criar o Atalho do Windows
Clique com o botão direito no arquivo LEITORTEXTO.py.

Vá em Enviar para > Área de trabalho (criar atalho).

Passo 2: Configurar para rodar em modo invisível
Vá até a sua Área de Trabalho, clique com o botão direito no atalho criado e escolha Propriedades.

Na aba Atalho, altere o campo Destino para chamar o executável de segundo plano do Python (pythonw), envolvendo o caminho do script em aspas. Exemplo:

   pythonw "C:\Caminho\Para\O\Seu\Projeto\LEITORTEXTO.py"
No campo Executar, altere de Janela normal para Minimizado.

Passo 3: Definir a Tecla de Atalho
Ainda na janela de propriedades, clique no campo Tecla de atalho.

Pressione a combinação desejada no seu teclado (ex: Ctrl + Shift + T ou Ctrl + Alt + P).

Clique em Aplicar e depois em OK.

💻 Fluxo de Utilização
Você pressiona o atalho de teclado que configurou.

O Windows ativa o script instantaneamente em segundo plano (sem abrir janelas pretas de terminal).

Uma película escura cobrirá a tela. Clique e arraste o mouse para selecionar o texto desejado dentro do retângulo vermelho.

Ao soltar o botão do mouse, a janela desaparece, o texto é processado pelo motor do Windows e copiado automaticamente para a sua área de transferência.

O processo do Python morre sozinho. Basta dar um Ctrl + V onde quiser colar o texto extraído.