import unittest

from projects.ml.noisy_sine_cnn import run


@unittest.skipUnless(run.torch_is_available(), "torch is not installed")
class NoisySineCNNTests(unittest.TestCase):
    def test_dataset_shapes(self):
        x_axis, features, targets = run.generate_noisy_sine_dataset(
            samples=12,
            sequence_length=24,
            noise_std=0.1,
            seed=3,
        )
        self.assertEqual(tuple(x_axis.shape), (24,))
        self.assertEqual(tuple(features.shape), (12, 1, 24))
        self.assertEqual(tuple(targets.shape), (12, 1, 24))

    def test_forward_pass_preserves_shape(self):
        _, features, _ = run.generate_noisy_sine_dataset(
            samples=4,
            sequence_length=32,
            noise_std=0.1,
            seed=5,
        )
        model = run.SineCNN()
        outputs = model(features)
        self.assertEqual(tuple(outputs.shape), (4, 1, 32))


if __name__ == "__main__":
    unittest.main()
