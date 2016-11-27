import unittest
from nose_parameterized import parameterized
from homephones.dialhelper import evalute_number


class TestDialhelper(unittest.TestCase):

    TEST_EVALUATE_VALID = [
        ("01348202020", "+441348202020"),
        ("03331221935", "+443331221935"),
        ("03333400111", "+443333400111"),
        ("303030", "+441348303030")
    ]

    @parameterized.expand(TEST_EVALUATE_VALID)
    def test_evaluate_number(self, dialed, expected):
        output = evalute_number(dialed=dialed)
        self.assertIsNotNone(output)
        self.assertEqual(output, expected)
