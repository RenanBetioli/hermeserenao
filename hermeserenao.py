#!/usr/bin/env python3.13
"""CLI do hermeserenao."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app.server import status_payload, ask_payload, list_context, list_skills, recent_events  # noqa: E402


def main():
    p = argparse.ArgumentParser(description="hermeserenao - infraestrutura local de agente")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    serve = sub.add_parser("serve")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--host", default="127.0.0.1")
    qa = sub.add_parser("ask")
    qa.add_argument("question")
    args = p.parse_args()

    if args.cmd == "check":
        print(json.dumps(status_payload(), ensure_ascii=False, indent=2))
    elif args.cmd == "ask":
        r = ask_payload(args.question)
        if not r["answers"]:
            print("Sem trechos correspondentes na base de contexto.")
            return
        for a in r["answers"]:
            print(f'{a["source"]}:{a["line"]}  score={a["score"]}')
            print("  " + a["text"].replace("\n", " "))
    elif args.cmd == "serve":
        from app.server import run_server
        print(f"hermeserenao em http://{args.host}:{args.port}")
        run_server(args.port, args.host)


if __name__ == "__main__":
    main()
