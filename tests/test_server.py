import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import server
from app.architecture import svg


class ServerTest(unittest.TestCase):
    def test_status_tem_componentes(self):
        data = server.status_payload()
        ids = {c["id"] for c in data["components"]}
        self.assertIn("agent", ids)
        self.assertIn("context", ids)
        self.assertTrue(all(c["state"] in {"ok", "demo", "off"} for c in data["components"]))

    def test_contexto_e_skills(self):
        self.assertGreaterEqual(len(server.list_context()), 5)
        self.assertGreaterEqual(len(server.list_skills()), 1)

    def test_ask_com_citacao(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(server, "EVENTS", Path(tmp) / "events.jsonl"):
                result = server.ask_payload("segredos memoria persistente")
        self.assertTrue(result["answers"])
        first = result["answers"][0]
        self.assertIn("source", first)
        self.assertIn("line", first)
        self.assertTrue(first["source"].startswith("context/"))

    def test_provider_selecionavel(self):
        from app.providers import get_provider
        with patch.dict("os.environ", {"HERMESERENAO_PROVIDER": "deterministic"}):
            self.assertEqual(get_provider().name, "deterministic")

    def test_hermes_api_provider_formata_resposta_e_autentica(self):
        from app.providers.hermes_api import HermesAPIProvider
        import json
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self):
                return json.dumps({"choices": [{"message": {"content": "Resposta teste"}}]}).encode()
        with patch("app.providers.hermes_api.urllib.request.urlopen", return_value=Response()) as call:
            provider = HermesAPIProvider(base_url="http://127.0.0.1:8642", api_key="local-test-key")
            result = provider.answer("pergunta", [{"source": "context/x.md", "line": 3, "text": "trecho"}])
        self.assertEqual(result["answer"], "Resposta teste")
        self.assertEqual(result["mode"], "hermes-api")
        req = call.call_args.args[0]
        self.assertEqual(req.get_header("Authorization"), "Bearer local-test-key")
        payload = json.loads(req.data)
        self.assertEqual(payload["model"], "hermes-agent")
        self.assertIn("context/x.md:3", payload["messages"][-1]["content"])

    def test_hermes_api_provider_requires_local_key(self):
        from app.providers.hermes_api import HermesAPIProvider
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "API server key"):
                HermesAPIProvider(base_url="http://127.0.0.1:8642", api_key=None).answer("oi", [])

    def test_chat_payload_retrieves_context_and_returns_answer(self):
        fake = type("FakeProvider", (), {"answer": lambda self, question, hits, history=None: {
            "question": question, "answer": "Resposta com fonte [context/seguranca/segredos.md:3]",
            "sources": [{"source": h["source"], "line": h["line"]} for h in hits], "mode": "hermes-api"
        }})()
        messages = [{"role": "user", "content": "como tratar segredos?"}]
        with patch("app.server.HermesAPIProvider", return_value=fake):
            result = server.chat_payload(messages)
        self.assertEqual(result["mode"], "hermes-api")
        self.assertTrue(result["sources"])
        self.assertTrue(result["sources"][0]["source"].startswith("context/"))

    def test_retrieve_com_citacao(self):
        self.assertTrue(server.retrieve("segredos memoria"))
        self.assertTrue(server.retrieve("segredos memoria")[0]["source"].startswith("context/"))

    def test_svg_valido(self):
        out = svg()
        self.assertTrue(out.startswith("<svg"))
        self.assertIn("</svg>", out)
        self.assertIn("hermeserenao", out)

    def test_eventos_sao_json(self):
        for row in server.recent_events():
            self.assertIn("kind", row)


if __name__ == "__main__":
    unittest.main()
