Original Credit: 
https://github.com/ChrisPHP/ProceduralRacetrack

Explaination:
https://www.youtube.com/watch?v=BTfghIWZFMw&ab_channel=Chris_PHP




More F1 race track-like:

https://www.linkedin.com/pulse/procedural-engine-sim-racing-track-generation-basic-luca-garattoni

```python
pip install raylib # for import pyray
pip install perlin-noise # for import perlin-noise
pip install pyvista
```

![image(1)](https://github.com/user-attachments/assets/22aa3e5c-01a9-4cbe-b138-372fb1ec39c3)


## How to Run?

1. Run </br>
```python procedural_path.py --screen_x=500 --screen_y=500```</br>

This will generate few things:
- `track_.npy` # the inner loop of the track
- `track_offset_.npy` # the outer loop of the track
- `track_.png` # a visual img of the track

2. Then run </br>
```python procedural_generated_tracks.py``` </br>

This script reads the `track_.npy` and `track_offset_.npy` and generates the cones corresponding to the track path in Isaac Lab environment


`offset_track()` in `procedural_path.py` takes the inner cones generated and offset them by a distance to form the outer cones, thus making a track.


## ToDos
- [ ] Fix normal vector flips on sharper turns
- [ ] Expose some parameters for users to tune track parameters
- [ ] Configure into IsaacLab training scheme
