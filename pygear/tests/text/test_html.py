# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest
from datetime import datetime

from pygear.text import html
from pygear.system._os import upath


class TestUtilsHtml(unittest.TestCase):
    def check_output(self, function, value, output=None):
        """
        Check that function(value) equals output.  If output is None,
        check that function(value) equals value.
        """
        if output is None:
            output = value
        self.assertEqual(function(value), output)

    def test_strip_tags(self):
        f = html.strip_tags
        items = (
            ('<p>See: &#39;&eacute; is an apostrophe followed by e acute</p>',
             'See: &#39;&eacute; is an apostrophe followed by e acute'),
            ('<adf>a', 'a'),
            ('</adf>a', 'a'),
            ('<asdf><asdf>e', 'e'),
            ('hi, <f x', 'hi, <f x'),
            ('234<235, right?', '234<235, right?'),
            ('a4<a5 right?', 'a4<a5 right?'),
            ('b7>b2!', 'b7>b2!'),
            ('</fe', '</fe'),
            ('<x>b<y>', 'b'),
            ('a<p onclick="alert(\'<test>\')">b</p>c', 'abc'),
            ('a<p a >b</p>c', 'abc'),
            ('d<a:b c:d>e</p>f', 'def'),
            ('<strong>foo</strong><a href="http://example.com">bar</a>', 'foobar'),
            # caused infinite loop on Pythons not patched with
            # http://bugs.python.org/issue20288
            ('&gotcha&#;<>', '&gotcha&#;<>'),
        )
        for value, output in items:
            self.check_output(f, value, output)

        # Some convoluted syntax for which parsing may differ between python versions
        output = html.strip_tags('<sc<!-- -->ript>test<<!-- -->/script>')
        self.assertNotIn('<script>', output)
        self.assertIn('test', output)
        output = html.strip_tags('<script>alert()</script>&h')
        self.assertNotIn('<script>', output)
        self.assertIn('alert()', output)

        # Test with more lengthy content (also catching performance regressions)
        for filename in ('strip_tags1.html', 'strip_tags2.txt'):
            path = os.path.join(os.path.dirname(upath(__file__)), 'files', filename)
            with open(path, 'r') as fp:
                content = fp.read()
                start = datetime.now()
                stripped = html.strip_tags(content)
                elapsed = datetime.now() - start
            self.assertEqual(elapsed.seconds, 0)
            self.assertIn("Please try again.", stripped)
            self.assertNotIn('<', stripped)
