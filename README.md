# Typologus — Typological Space Visualizer

A web-based interactive 3D visualizer for sound object typology, based on the framework developed in:

- Valle, A. (2024). Towards a Semiotics of the Audible. *Signata*.
- Lombardo, V. & Valle, A. (2007). *Audio e Multimedia* (4th ed.). Apogeo.

The example dataset contains 60 sound objects from Varèse's *Poème électronique*, analyzed as part of the VEP project. Full project documentation and audio materials at: https://www.cirma.unito.it/vep/

## Usage

- Open `index.html` in a browser, or visit the [GitHub Pages URL](https://vanderaalle.github.io/Typologus)
- Drag and drop a JSON or CSV file to load your own dataset
- Use the templates in `data/` as a starting point for annotation
- Run `scripts/plot_typological_space.py` to generate publication-quality PDF figures

## Annotation format

Sound objects are described by a triplet (x, y, z):

- **x** ∈ [−2.5, +2.5]: profile/sustain axis
- **y** ∈ [0, 2]: calibre (mass)
- **z** ∈ [0, 3]: variation

See `data/sound_objects_template.json` for the full field reference.

## License

Data and visualizer: CC BY 4.0
Code: MIT
