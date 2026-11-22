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
