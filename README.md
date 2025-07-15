# Telegram Bot com FaceSwap e DeepFake (FOMM)

Este projeto é um bot para Telegram feito com Flask que permite:

✅ Trocar rostos em vídeos com [FaceFusion](https://github.com/facefusion/facefusion)  
✅ Gerar deepfakes realistas com [First Order Motion Model](https://github.com/AliaksandrSiarohin/first-order-model)

---

## 🚀 Como usar

### 1. Clone o projeto FOMM e baixe os modelos:

```bash
git clone https://github.com/AliaksandrSiarohin/first-order-model first-order-motion-model
mkdir -p first-order-motion-model/checkpoints
```

🔗 Baixe o modelo [vox-cpk.pth.tar (Google Drive)](https://drive.google.com/file/d/1kK_H1uRg4l_YTc0m4VxgG1vK3i0oD3Xo/view)  
Coloque-o em: `first-order-motion-model/checkpoints/vox-cpk.pth.tar`

---

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Certifique-se de que o `facefusion` está disponível no PATH, ou instale conforme a [documentação oficial](https://github.com/facefusion/facefusion).

---

### 3. Configure seu token do Telegram

Edite o arquivo `bot_config.py` e adicione seu token:

```python
TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"
```

---

### 4. Execute o servidor

```bash
python app.py
```

---

## 🤖 Comandos disponíveis no bot

- Envie um vídeo e depois uma imagem para fazer face swap com FaceFusion
- Envie `/deepfake` para iniciar o modo DeepFake com FOMM:
    - Primeiro, envie uma **imagem de rosto**
    - Depois, envie um **vídeo de referência (movimento)**
    - O bot retorna um deepfake com o rosto da imagem animado com os movimentos do vídeo

---

## 📁 Estrutura dos arquivos

- `app.py` - Webhook Flask para o Telegram
- `bot_config.py` - Token do Telegram
- `swap_face.py` - Lógica de FaceFusion
- `deepfake_fomm.py` - Lógica do modelo FOMM
- `requirements.txt` - Dependências
- `README.md` - Este guia

---