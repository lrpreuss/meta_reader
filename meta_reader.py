import os
import math
import re
import mimetypes
from pathlib import Path
from datetime import datetime
import ffmpeg
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image, ExifTags


class Arquivos:
    def __init__(self):
        self.paths = []

    def clean_dragged_path(self, path):
        path = path.strip().strip('"').strip("'")
        path = re.sub(r'^\s*&\s*', '', path)
        path = path.strip('"').strip("'")

        # Validação para caminhos de Windows
        if not re.match(r'^[a-zA-Z]:\\[\\\S|*\S]', path):
            raise ValueError("\nCaminho inválido. Arraste o arquivo novamente ou digite o caminho completo.")
        return path

    def add_file(self, file_path):
        try:
            cleaned_path = self.clean_dragged_path(file_path)
            path = Path(cleaned_path)

            if not path.exists():
                # Tentativa para caminhos de rede
                unc_path = Path(f"\\\\?\\{cleaned_path}")
                if not unc_path.exists():
                    raise FileNotFoundError(f"Arquivo não encontrado: {cleaned_path}")
                path = unc_path

            self.paths.append(path)
            print(f"Arquivo adicionado: {path.name}")
            return path

        except Exception as e:
            print(f"Erro ao processar arquivo: {str(e)}")
            print("Dica: Arraste o arquivo novamente ou digite o caminho completo manualmente.")


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.log(size_bytes, 1024))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def show_file_info(file_path):
    stats = os.stat(file_path)
    size = convert_size(stats.st_size)
    creation_time = datetime.fromtimestamp(stats.st_ctime).strftime('%d/%m/%y %H:%M:%S')
    modification_time = datetime.fromtimestamp(stats.st_mtime).strftime('%d/%m/%y %H:%M:%S')
    print(f"\nNome do arquivo: {file_path.name}")
    print(f"Tamanho: {size}")
    print(f"Data de criação (sistema): {creation_time}")
    print(f"Data de modificação (sistema): {modification_time}")


def get_media_metadata(file_path):
    try:
        probe = ffmpeg.probe(str(file_path))
        format_metadata = probe['format']
        show_file_info(file_path)
        print(f"Formato: {format_metadata['format_name']}")

        duration = float(format_metadata.get('duration', 0))
        minutes, seconds = divmod(duration, 60)
        print(f"Duração: {int(minutes)} min {int(seconds)} seg")

        for stream in probe['streams']:
            if stream['codec_type'] == 'audio':
                print(f"Taxa de amostragem: {stream.get('sample_rate', 'N/D')} Hz")
                print(f"Bit depth: {stream.get('bits_per_sample', 'N/D')} bits")
            elif stream['codec_type'] == 'video':
                print(f"Resolução: {stream.get('width')}x{stream.get('height')} px")
                print(f"FPS: {stream.get('r_frame_rate')}")

    except Exception as e:
        print(f"Erro ao obter metadados de mídia: {e}")


def get_pdf_metadata(file_path):
    try:
        reader = PdfReader(str(file_path))
        show_file_info(file_path)
        info = reader.metadata
        print(f"Criado por: {info.get('/Author', 'N/D')}")
        print(f"Modificado por: {info.get('/ModDate', 'N/D')}")
        print(f"Título: {info.get('/Title', 'N/D')}")
        print(f"Produtor: {info.get('/Producer', 'N/D')}")
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")


def get_docx_metadata(file_path):
    try:
        doc = Document(str(file_path))
        core = doc.core_properties
        show_file_info(file_path)
        print(f"Criado por: {core.author}")
        print(f"Última modificação por: {core.last_modified_by}")
        print(f"Título: {core.title}")
        print(f"Assunto: {core.subject}")
    except Exception as e:
        print(f"Erro ao ler DOCX: {e}")


def get_image_metadata(file_path):
    try:
        with Image.open(file_path) as img:
            show_file_info(file_path)
            print(f"Formato da imagem: {img.format}")
            print(f"Dimensões: {img.width} x {img.height}")
            print(f"Modo de cor: {img.mode}")

            # Tenta extrair EXIF
            exif = img.getexif()
            if exif:
                exif_data = {
                    ExifTags.TAGS.get(tag): value
                    for tag, value in exif.items()
                    if tag in ExifTags.TAGS
                }
                if 'Artist' in exif_data:
                    print(f"Autor: {exif_data['Artist']}")
                if 'Software' in exif_data:
                    print(f"Software: {exif_data['Software']}")
    except Exception as e:
        print(f"Erro ao ler imagem: {e}")


def main():
    print("Arraste o arquivo aqui e pressione ENTER:\n")
    dragged = input()
    arquivos = Arquivos()
    file_path = arquivos.add_file(dragged)

    if not file_path:
        return

    suffix = file_path.suffix.lower()
    mime_type, _ = mimetypes.guess_type(str(file_path))

    if mime_type and (mime_type.startswith("video") or mime_type.startswith("audio")):
        get_media_metadata(file_path)
    elif suffix == ".pdf":
        get_pdf_metadata(file_path)
    elif suffix == ".docx":
        get_docx_metadata(file_path)
    elif suffix in [".jpg", ".jpeg", ".png"]:
        get_image_metadata(file_path)
    else:
        print("Tipo de arquivo não suportado para extração de metadados.")


if __name__ == "__main__":
    main()