import unittest

from projects.physics.harmonic_oscillator.run import simulate


class HarmonicOscillatorTests(unittest.TestCase):
    def test_simulate_returns_expected_shape(self):
        trajectory = simulate(steps=10, dt=0.1)
        self.assertEqual(len(trajectory), 11)
        self.assertTrue(all(len(point) == 4 for point in trajectory))

    def test_energy_stays_bounded_for_small_dt(self):
        trajectory = simulate(steps=200, dt=0.01)
        energies = [energy for _, _, _, energy in trajectory]
        self.assertLess(max(energies) - min(energies), 0.02)


if __name__ == "__main__":
    unittest.main()
