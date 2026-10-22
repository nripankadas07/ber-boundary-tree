import unittest
from ber_boundary_tree import analyze

class BER(unittest.TestCase):
    def test_nested_boundaries_and_classes(self):
        r=analyze(bytes.fromhex('3009020105a1040402abcd'));ns=r['nodes'];self.assertEqual(len(ns),4)
        self.assertEqual([x['parent']for x in ns],[None,0,0,2]);self.assertEqual([x['end']for x in ns],[11,5,11,11]);self.assertEqual(ns[2]['class'],'context');self.assertEqual(ns[3]['preview_hex'],'abcd')
        for n in ns:
            if n['parent']is not None:
                p=ns[n['parent']];self.assertGreaterEqual(n['offset'],p['value_offset']);self.assertLessEqual(n['end'],p['end'])
    def test_high_tag_and_minimal_length_flag(self):
        r=analyze(bytes.fromhex('9f81000100'));self.assertEqual(r['nodes'][0]['tag_number'],128)
        r=analyze(bytes.fromhex('048101aa'));self.assertFalse(r['all_lengths_minimal']);self.assertEqual(r['nodes'][0]['length'],1)
        r=analyze(b'\x04\x81\x80'+b'x'*128);self.assertTrue(r['all_lengths_minimal'])
    def test_truncation_at_every_prefix(self):
        b=bytes.fromhex('3009020105a1040402abcd')
        for i in range(1,len(b)):
            with self.assertRaises(ValueError):analyze(b[:i])
    def test_parent_boundary_indefinite_and_bad_tags_reject(self):
        for h in ['3003040201aa','30800000','0000','9f020100','9f80010100','04850000000000','1f81']:
            with self.assertRaisesRegex(ValueError,'offset'):analyze(bytes.fromhex(h))
    def test_empty_siblings_and_primitive_values_are_not_parsed(self):
        self.assertEqual(analyze(b'')['nodes'],[])
        r=analyze(bytes.fromhex('040230ff020100'));self.assertEqual(len(r['nodes']),2);self.assertEqual(r['nodes'][0]['preview_hex'],'30ff')
    def test_resource_limits(self):
        with self.assertRaises(ValueError):analyze(b'x'*131073)
        with self.assertRaises(ValueError):analyze(bytes.fromhex('0500')*5001)
        b=b''
        for _ in range(34):b=b'\x30'+bytes([len(b)])+b
        with self.assertRaises(ValueError):analyze(b)

if __name__=='__main__':unittest.main()
