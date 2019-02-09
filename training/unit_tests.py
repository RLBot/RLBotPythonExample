import unittest

from rlbot.training.training import Pass, Fail
from rlbottraining.exercise_runner import run_playlist

from hello_world_training import StrikerPatience

class PatienceTest(unittest.TestCase):
    def test_patience_required(self):
        result_iter = run_playlist([StrikerPatience(name='patience required')])
        results = list(result_iter)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.exercise.name, 'patience required')
        self.assertIsInstance(result.grade, Fail)

    def test_no_patience_required(self):
        result_iter = run_playlist([StrikerPatience(name='no patience required', car_start_x=-1000)])
        results = list(result_iter)
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result.exercise.name, 'no patience required')
        self.assertIsInstance(result.grade, Pass)

if __name__ == '__main__':
    unittest.main()
