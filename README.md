# 📂 Meta_Reader

O **meta_reader** surgiu da necessidade de analisar bit rate e bit depth de arquivos de áudio. No último ano, acrescentei as funcionalidades de ler metadados simples de .pdf e .docx; além dos metadados de vídeo e imagens que necessitei no meio do caminho.

---

## 🎯 Funcionalidades

- ✅ Suporte a arquivos de **áudio e vídeo** (`.mp3`, `.mp4`, etc.)
- ✅ Suporte a **documentos PDF e Word** (`.pdf`, `.docx`)
- ✅ Suporte a **imagens** (`.jpeg`, `.jpg`, `.png`)
- ✅ Mostra:
  - Nome do arquivo
  - Tamanho
  - Datas de criação e modificação
  - Duração, resolução e taxa de quadros (para mídia)
  - Autor e software (para documentos e imagens com EXIF)
  - Título, assunto e software usado para criação (quando disponível)
- ✅ Compatível com **drag and drop** no terminal (Windows)

---

## 🖥️ Como usar

1. Clone o repositório:
   
   git clone https://github.com/lrpreuss/meta_reader.git
   cd meta_reader

2. Instale as dependências:

   pip install -r requirements.txt

3. Execute o script:

   python meta_reader_dragdrop.py

4. Arraste um arquivo para dentro do terminal e pressione Enter. O código já é preparado para limpar os caminhos de aruqivo em sistemas operacionais Windows.

## 📖 Exemplo:

![exemplo_MetaReader](https://github.com/user-attachments/assets/e2e5453c-f7d2-418c-99c0-11c1c847a3a1)


🧪 Tipos de arquivos testados

* .mp3, .wav, .mp4, .mov
* .pdf, .docx
* .jpg, .jpeg, .png


📄 Licença
MIT License © lrpreuss


✨ Créditos

Desenvolvido por Laís Ravache Preuss

LinkedIn: [linkedin.com/in/lais-r-preuss](https://www.linkedin.com/in/lais-r-preuss/)

GitHub: [github.com/lrpreuss](https://github.com/lrpreuss)
