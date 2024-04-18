import unittest
import numpy as np
from particle import PriorityQueue

class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.pq = PriorityQueue()

    def test_push_and_pop(self):
        self.pq.push('item1', 1)
        self.pq.push('item2', 2)
        self.pq.push('item3', 3)
        
        self.assertEqual(self.pq.items[0], 'item1')
        self.assertEqual(self.pq.items[1], 'item2')
        self.assertEqual(self.pq.items[2], 'item3')
        
        self.assertEqual(self.pq.priorities[0], 1)
        self.assertEqual(self.pq.priorities[1], 2)
        self.assertEqual(self.pq.priorities[2], 3)
        
        self.pq.pop()
        
        self.assertEqual(self.pq.items[0], 'item2')
        self.assertEqual(self.pq.items[1], 'item3')
        
        self.assertEqual(self.pq.priorities[0], 2)
        self.assertEqual(self.pq.priorities[1], 3)

if __name__ == '__main__':
    unittest.main()