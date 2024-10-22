# Soap Bubble Simulator

This project simulates the colors of soap bubbles as a function of their thickness. It can be used to identify the thickness of soap bubbles in a picture by comparing the observed colors to the simulated ones.

## Features

- Real-time simulation of soap bubble interference patterns
- Interactive thickness adjustment using mouse input
- Spectral color calculation for accurate color representation
- Graph display of reflection intensity across the visible spectrum
- Toggle between dark and light background modes

## Requirements

To run this simulation, you'll need the following Python libraries:

```
pip install pygame numpy colour-science
```

## How It Works

The simulation uses thin-film interference physics to calculate the reflection intensity for different wavelengths of light. It then converts these intensities into visible colors using color science techniques.

Key components:

1. `thin_film_interference()`: Calculates reflection intensity based on wavelength, film thickness, and refractive index.
2. `new_avg()`: Converts spectral intensities to RGB colors using color science libraries.
3. `rings()`: Generates the interference pattern for the bubble.
4. `x_L()`: Calculates the path length of light through the film at different points on the bubble.

## Usage

Run the script to start the simulation:

```
python soap_bubble_simulator.py
```

- Click and drag the mouse vertically to adjust the thickness of the bubble film.
- Press the spacebar to toggle between dark and light background modes.
- Press 'Q' to quit the simulation.

## Applications

This simulator can be used to:

1. Understand the physics of thin-film interference
2. Estimate the thickness of soap bubbles in photographs
3. Generate accurate colors for computer graphics applications involving iridescent materials

## Extended Physical Explanations

[This section is intentionally left blank for future extended physical explanations about thin-film interference, light wave behavior, and the mathematics behind the soap bubble color phenomena.]

## Future Improvements

- Add ability to load and analyze real soap bubble images
- Implement more complex bubble shapes and multiple bubble interactions
- Optimize performance for smoother real-time updates

## License

[Insert your chosen license here]

## Contributors

[Your Name]

Feel free to contribute to this project by submitting pull requests or reporting issues!
