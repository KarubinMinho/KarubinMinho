import unittest

from apps.utils.utils import SingleLinkedList


class TestLinkedListMethods(unittest.TestCase):
    """SingleLinkedList部分方法测试"""
    def setUp(self) -> None:
        self.link_list = SingleLinkedList()

    def test_add(self):
        self.link_list.add(20)
        self.link_list.add(30)
        self.assertEqual(self.link_list.head.data, 30)
        self.assertEqual(self.link_list.tail.data, 20)

    def test_append(self):
        self.link_list.append(20)
        self.link_list.append(30)
        self.assertEqual(self.link_list.head.data, 20)
        self.assertEqual(self.link_list.tail.data, 30)

    def test_insert(self):
        self.link_list.insert(2, 30)
        self.link_list.insert(0, 40)
        self.link_list.insert(len(self.link_list), 50)
        self.assertEqual(self.link_list.head.data, 40)
        self.assertEqual(self.link_list.tail.data, 50)

    def test_remove(self):
        self.link_list.append(20)
        self.link_list.append(30)
        self.link_list.add(40)
        self.link_list.add(10)
        self.link_list.insert(2, 50)
        self.link_list.insert(0, 60)
        self.link_list.insert(len(self.link_list), 70)
        self.link_list.remove(70)
        self.link_list.remove(60)
        self.assertEqual(self.link_list.tail.data, 30)
        self.assertEqual(self.link_list.head.data, 10)


if __name__ == '__main__':
    unittest.main()

