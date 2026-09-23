"""Lossless publication-format tests; numerical experiment code is unchanged."""
import unittest,copy
from research.triad.archive import pack,unpack
from research.triad_loop.transfer import run
class ArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.record=run('archive-test','normal',7,'addition_blank',48)
    def test_roundtrip(self): self.assertEqual(unpack(pack(self.record)),self.record)
    def test_measurement_corruption_rejected(self):
        p=pack(self.record);p['record']['observations'][0]['value']+=.01
        with self.assertRaises(ValueError):unpack(p)
    def test_event_corruption_rejected(self):
        p=pack(self.record);p['event_payloads'][0][1]['biological_units']=1
        with self.assertRaises(ValueError):unpack(p)
    def test_unknown_format_rejected(self):
        p=pack(self.record);p['archive_format']='unknown'
        with self.assertRaises(ValueError):unpack(p)
    def test_original_format_accepted_without_mutation(self):
        r=copy.deepcopy(self.record);self.assertEqual(unpack(r),self.record);self.assertEqual(r,self.record)
if __name__=='__main__':unittest.main()
