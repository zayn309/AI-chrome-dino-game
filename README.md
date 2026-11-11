# AI Chrome Dino Game

A recreation of the offline **Chrome dinosaur runner** built with Pygame, plus an AI that learns to play it through **NEAT** (NeuroEvolution of Augmenting Topologies).

## How it works

- Each generation spawns a population of dinosaurs, and each dinosaur is controlled by its own small neural network.
- Each network gets three inputs: the next obstacle's x and y position and its distance from the dinosaur. Its output decides whether to jump.
- Fitness rewards survival and clearing obstacles, and penalises collisions and unnecessary jumps.
- The best networks are bred and mutated, and NEAT evolves both the weights and the structure of the networks over generations.

## Getting started

```bash
pip install pygame neat-python
cd "Chrome dino runner"
python main.py
```

NEAT hyperparameters such as population size, mutation rates, and activation functions are in [`Chrome dino runner/config.txt`](Chrome%20dino%20runner/config.txt).

## Tech stack

Python · Pygame · neat-python

## License

[MIT](LICENSE)
