# Typologus — Typological Space Visualizer

A web-based interactive 3D visualizer for sound object typology, based on the semiotic framework for the audible developed by Lombardo & Valle.

**Live demo:** https://vanderaalle.github.io/Typologus

---

## Theoretical background

The typological space is a 3-dimensional continuous space for the description and classification of sound objects, defined by three axes:

| Axis | Dimension | Range | Direction |
|------|-----------|-------|-----------|
| X | Profile / Sustain | −2.5 … +2.5 | sustained (neg) · anamorph (0) · iterative (pos) |
| Y | Calibre (Mass) | 0 … 2 | 0 = narrow/pitched · 2 = wide/noisy (top → bottom) |
| Z | Variation | 0 … 3 | 0 = stable · 3 = maximally varying |

The profile axis encodes both the temporal macroform (anamorphism · eumorphism · amorphism) and the sustain type (sustained · impulsive · iterative), which are orthogonal except at the impulsive/anamorphic coupling point (x = 0).

Every sound object receives a unique position (x, y, z) in the space, allowing differentiation within typological classes and description of transformation trajectories.

## References

- Valle, A. (2015). Towards a Semiotics of the Audible. *Signata. Annales des sémiotiques / Annals of Semiotics*, 6, pp. 65–89. https://doi.org/10.4000/signata.1063

- Lombardo, V. & Valle, A. (2024). *Audio e Multimedia* (5th ed.). Apogeo, Milan.

- Lombardo, V. & Valle, A. (2014). Typological space for sound objects. [internal reference]

---

## Example dataset — Varèse: *Poème électronique*

The example dataset (`data/sound_objects.json`) contains 60 annotated sound objects from Edgar Varèse's *Poème électronique* (1958), analyzed as part of the **VEP project** (Varèse Poème électronique).

Full project documentation, score, and audio materials:

**https://www.cirma.unito.it/vep/**

---

## Using the visualizer

Open `index.html` in any modern browser, or visit the GitHub Pages URL above.

### Controls

| Action | Result |
|--------|--------|
| Drag | Rotate |
| Scroll | Zoom |
| Right-drag | Pan |
| Click a point | Show object details |

### Sidebar

- **Load data** — drag and drop a JSON or CSV file to load your own dataset
- **Search** — filter by name, mass, or variation description
- **Profile / Sustain filters** — show/hide by category
- **Point size** — adjust marker size
- **Labels** — toggle ID labels on/off
- **Axis grid** — toggle reference grid
- **Reset view** — return to default camera position
- **Export** — download current data as JSON or CSV

---

## Annotation format

Sound objects are described by a triplet `(x, y, z)` plus categorical descriptors.

### JSON

```json
[
  {
    "id": 1,
    "name": "sound name / file reference",
    "x": 0.0,
    "y": 0.0,
    "z": 0.0,
    "profile": "anamorph",
    "sustain": "impulsive",
    "mass": "pitched mass",
    "variation": "no variation",
    "profile_full": "anamorph, impulsive"
  }
]
```

### Allowed values

| Field | Values |
|-------|--------|
| `profile` | `anamorph` · `eumorph` · `amorph` · `mixed` |
| `sustain` | `sustained` · `impulsive` · `iterative` |
| `mass` | `pitched mass` · `fixed mass` · `varied mass` · `variable mass` |
| `variation` | `no variation` · `very low variation` · `low variation` · `medium variation` · `medium-high variation` · `high variation` |

Use the templates in `data/` as a starting point:

- `data/sound_objects_template.json`
- `data/sound_objects_template.csv`

---

## Publication-quality figures

The Python script `plot_typological_space.py` generates vectorial PDF figures (matplotlib, 300 dpi) suitable for publication.

```bash
# Install dependencies
pip install matplotlib numpy

# Run with built-in dataset
python plot_typological_space.py

# Run with custom dataset
python plot_typological_space.py mydata.json
```

Outputs:

- `typological_space_3d.pdf` — 3D scatter plot
- `typological_space_overview.pdf` — 3D view + 3 two-dimensional projections

---

## Repository structure

```
Typologus/
├── index.html                        # Interactive 3D visualizer
├── plot_typological_space.py         # Publication-quality PDF figures
├── README.md
└── data/
    ├── sound_objects.json            # Varèse: Poème électronique (60 objects)
    ├── sound_objects_template.json   # Blank annotation template
    └── sound_objects_template.csv    # Blank annotation template (CSV)
```

---

## License

- Visualizer code: [MIT License](LICENSE)
- Data and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

If you use Typologus in your research, please cite:

> Valle, A. (2015). Towards a Semiotics of the Audible. *Signata*, 6, pp. 65–89. https://doi.org/10.4000/signata.1063

> Lombardo, V. & Valle, A. (2024). *Audio e Multimedia* (5th ed.). Apogeo.
