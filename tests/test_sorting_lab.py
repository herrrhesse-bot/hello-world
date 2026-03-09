import unittest

from projects.algorithms.sorting_lab.run import insertion_sort, merge_sort


class SortingLabTests(unittest.TestCase):
    def test_insertion_sort_matches_builtin(self):
        data = [5, -1, 3, 3, 0, 8]
        self.assertEqual(insertion_sort(data), sorted(data))

    def test_merge_sort_matches_builtin(self):
        data = [9, 2, -4, 7, 7, 1]
        self.assertEqual(merge_sort(data), sorted(data))


if __name__ == "__main__":
    unittest.main()
