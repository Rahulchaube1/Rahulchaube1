# Rahul Chaube — Interactive 3D Profile

A lightweight interactive developer profile built with **Three.js**.

## Experience

- Interactive WebGL scene with a central AI/system core
- Orbit controls and subtle auto-rotation
- Project nodes for **Blyx**, **AR Studio**, and **MapNepal**
- Clickable project information panels
- Responsive mobile layout
- Reduced renderer pixel ratio for better performance on high-DPI screens
- No framework or build step required

## Run locally

Open `index.html` through a local static server:

```bash
python -m http.server 8080
```

Then visit `http://localhost:8080/3d-profile/`.

## Stack

- Three.js
- WebGL
- Vanilla HTML/CSS/JavaScript
- ES modules

## Design principle

The 3D layer is deliberately a **visual layer**, not a replacement for the GitHub README. GitHub profile READMEs are optimized for fast scanning and project discovery; the 3D experience provides the optional immersive layer for visitors who want to explore further.
