import sqlite3
import tempfile
import unittest
from pathlib import Path
from server import read_history


class HistoryTest(unittest.TestCase):
    def test_conversion_no_duplicate_visits_and_read_only(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'History'
            with sqlite3.connect(path) as db:
                db.executescript('''
                    CREATE TABLE urls(id, url, title);
                    CREATE TABLE visits(id, url, visit_time);
                    CREATE TABLE keyword_search_terms(url_id, term);
                    INSERT INTO urls VALUES(1,'https://example.com/?q=test','<script>');
                    INSERT INTO visits VALUES(7,1,13344473600000000);
                    INSERT INTO keyword_search_terms VALUES(1,'test'),(1,'second');
                ''')
            db.close()
            before = path.read_bytes()
            rows = read_history(path)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][:5], [7, 'https://example.com/?q=test', '<script>', 1700000000000, 'example.com'])
            self.assertEqual(path.read_bytes(), before)
            with self.assertRaises(sqlite3.OperationalError):
                read_history(Path(folder) / 'missing')
            self.assertFalse((Path(folder) / 'missing').exists())


if __name__ == '__main__':
    unittest.main()
