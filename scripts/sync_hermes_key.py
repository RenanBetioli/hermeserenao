#!/usr/bin/env python3.13
"""Copy only the Hermes API key into a private project .env (never prints it)."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / ".env"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="replace an existing local .env")
    args = parser.parse_args()

    if TARGET.exists() and not args.force:
        print(".env já existe; não sobrescrevi. Use --force se quiser recriá-lo.")
        return 2
    try:
        env_path = subprocess.check_output(
            ["hermes", "config", "env-path"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        source = Path(env_path).expanduser()
        lines = source.read_text(encoding="utf-8").splitlines()
    except (OSError, subprocess.CalledProcessError):
        print("Não consegui localizar o arquivo de configuração de segredos do Hermes.")
        return 1

    key = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("API_SERVER_KEY="):
            key = stripped.split("=", 1)[1].strip().strip("'\"")
            break
    if not key:
        print("API_SERVER_KEY não encontrado no Hermes. Configure o API Server primeiro.")
        return 1

    content = f"HERMES_API_SERVER_KEY={key}\nHERMES_API_BASE_URL=http://127.0.0.1:8642\n"
    fd = os.open(TARGET, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as output:
        output.write(content)
    os.chmod(TARGET, 0o600)
    print(".env local criado com permissão restrita; a chave não foi exibida.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
