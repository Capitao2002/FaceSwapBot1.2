import subprocess
import logging
import os

logger = logging.getLogger(__name__)

def process_video(video_path, face_path, output_path):
    command = [
        "facefusion",
        "headless-run",
        "-t", video_path,
        "-s", face_path,
        "-o", output_path,
        "--execution-providers", "cpu"
    ]

    logger.info("🔧 Executando facefusion: %s", " ".join(command))

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info("✅ STDOUT:
%s", result.stdout)
        logger.info("✅ STDERR:
%s", result.stderr)

        if not os.path.exists(output_path):
            logger.error("❌ O vídeo de saída não foi gerado: %s", output_path)
            raise FileNotFoundError(f"Vídeo não gerado em: {output_path}")

    except subprocess.CalledProcessError as e:
        logger.error("❌ Erro no comando facefusion: %s", e)
        logger.error("STDOUT: %s", e.stdout)
        logger.error("STDERR: %s", e.stderr)
        raise