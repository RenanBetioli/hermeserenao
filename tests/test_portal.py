"""Regressions for the operations portal, without model calls."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
from app import server


class Markup(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.views = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'button' and 'data-view' in attrs:
            self.views.add(attrs['data-view'])


class PortalTest(unittest.TestCase):
    def test_navigation_has_real_destination_for_each_view(self):
        markup = Markup((server.STATIC / 'index.html').read_text())
        expected = {'overview', 'chat', 'library', 'activity', 'integrations', 'system'}
        self.assertTrue(expected.issubset(markup.views), expected - markup.views)
        for name in expected:
            self.assertIn('view-' + name, markup.ids)
        self.assertEqual(len(markup.ids), len(set(markup.ids)), 'duplicate element IDs')

    def test_open_document_returns_actual_text(self):
        doc = server.context_document('context/agentes/memoria.md')
        self.assertEqual(doc['path'], 'context/agentes/memoria.md')
        expected = (server.CONTEXT / 'agentes/memoria.md').read_text(encoding='utf-8')
        self.assertEqual(doc['content'], expected)

    def test_document_outside_context_is_rejected(self):
        for path in ('../.hermes/.env', 'context/../.env', '/etc/passwd', 'README.md'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                server.context_document(path)

    def test_document_missing_is_rejected(self):
        with self.assertRaises(ValueError):
            server.context_document('context/does-not-exist.md')


if __name__ == '__main__':
    unittest.main()
