import pyray as pr
import numpy as np
import argparse

import createtrack
import createmodel

import matplotlib.pyplot as plt

def calculate_point_section(p1, p2, per):
    x_three_quarters = (per * p1[0] + p2[0]) / 10
    y_three_quarters = (per * p1[1] + p2[1]) / 10
    three_quarters_point = (x_three_quarters, y_three_quarters)
    return three_quarters_point


def offset_track(points, offset_distance=2.0):
    """
    Expands the track by shifting points outward along the normal.
    :param points: List of (x, y) track points.
    :param offset_distance: Distance to offset outward.
    :return: Offset track points (expanded version).
    """
    num_points = len(points)
    offset_points = np.zeros_like(points, dtype=np.float64)

    # Convert tuples to NumPy arrays
    points = np.array(points, dtype=np.float64)

    # Compute track center (centroid)
    center = np.mean(points, axis=0)

    for i in range(num_points):
        # Get previous and next points to calculate tangent
        prev_idx = (i - 1) % num_points
        next_idx = (i + 1) % num_points

        p1, p2 = np.array(points[prev_idx]), np.array(points[next_idx])

        # Compute tangent vector
        tangent = p2 - p1
        tangent /= np.linalg.norm(tangent)  # Normalize tangent

        # Compute normal (perpendicular to tangent)
        normal = np.array([-tangent[1], tangent[0]])

        # Ensure normal points outward (away from center)
        direction = points[i] - center
        if np.dot(normal, direction) < 0:
            normal = -normal  # Flip normal if pointing inward

        # Apply offset
        offset_points[i] = points[i] + offset_distance * normal

    return offset_points



def interpolate_large_gaps(points, num_samples=10, gap_threshold=5.0):
    """
    Interpolates between points only if they have a large gap.
    :param points: List of (x, y) track points.
    :param num_samples: Number of samples for interpolation if gap is large.
    :param gap_threshold: Minimum distance required to trigger interpolation.
    :return: List of track points including interpolated ones.
    """
    interpolated_points = [points[0]]  # Start with the first point

    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        distance = np.linalg.norm(np.array(p2) - np.array(p1))  # Euclidean distance

        if distance > gap_threshold:
            for t in np.linspace(0, 1, num_samples):  # Interpolate only for large gaps
                x = (1 - t) * p1[0] + t * p2[0]
                y = (1 - t) * p1[1] + t * p2[1]
                interpolated_points.append((x, y))
        else:
            interpolated_points.append(p2)  # Keep original point if gap is small

    return interpolated_points
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a procedurally generated racetrack')
    parser.add_argument('--track_3D', type=bool, default=False, help='Create 3D racetrack or not')
    parser.add_argument('--seed', type=int, help='Specificy int32 seed')
    parser.add_argument('--screen_x', type=int, default=100, help='The screen width for raylib')
    parser.add_argument('--screen_y', type=int, default=100, help='The screen height for raylib')
    args = parser.parse_args()

    seed = np.random.randint(0, 2**32)
    if args.seed:
        seed = args.seed
    np.random.seed(seed)

    track = createtrack.CreateTrack(num_points=10, x_bounds=[0,100], y_bounds=[0,100], corner_cells=15,seed=seed)
    points = track.create_racetrack(args.track_3D)
    
    # convert the race track points into x, y list for plotting
    points = interpolate_large_gaps(points, num_samples=10, gap_threshold=7.0)
    offset_points = offset_track(points, offset_distance = 5.0)

    print(offset_points)

    np.save("track_.npy", np.array(points))
    np.save("track_offset_.npy", np.array(offset_points))


    # Generate interpolated track points
    data = np.array(points)
    data_offset = np.array(offset_points)
    x, y = data[:, 0], data[:, 1]
    x1, y1 = data_offset[:, 0], data_offset[:, 1]
    plt.plot(x, y, marker='o', linestyle='-')
    plt.plot(x1, y1, marker='o', linestyle='--')
    plt.savefig("track_.png")


    # plt.plot(points)
    # plt.show()

    if args.track_3D == False :
        pr.init_window(args.screen_x, args.screen_y, "Racetrack")
        pr.set_target_fps(60)
        cam = pr.Camera2D((0, 0), (0, 0), 0, 2)

        while not pr.window_should_close():
            pr.begin_drawing()
            pr.clear_background(pr.BLACK)
            pr.draw_text("Seed: {}".format(seed), 10, 10, 20, pr.RAYWHITE)
            pr.begin_mode_2d(cam)
            for i in range(len(points)-1):
                pr.draw_line_ex(list(points[i]), list(points[i+1]),1, pr.RAYWHITE)
            pr.end_mode_2d() # pr.end_mode_2d(cam)
            pr.end_drawing()
        pr.close_window()        
    # else:
    #     vista = createmodel.CreateModel()
    #     vista.create_mesh_line(points=points)

    #     pr.init_window(args.screen_x, args.screen_y, "Racetrack")
    #     pr.set_target_fps(60)
    #     cam = pr.Camera3D([0, 40, 100], [50.0, 0.0, 50.0], [0.0, 1.0, 0.0], 90.0, 0)

    #     while not pr.window_should_close():
    #         pr.update_camera(cam, pr.CAMERA_ORBITAL)
    #         pr.begin_drawing()
    #         pr.clear_background(pr.BLACK)
    #         pr.draw_text("Seed: {}".format(seed), 10, 10, 20, pr.RAYWHITE)
    #         pr.begin_mode_3d(cam)
    #         pr.draw_grid(500, 3.0)
    #         for i in range(len(points)-1):
    #             pr.draw_cylinder_ex(list(points[i]), list(points[i+1]), 1, 1, 6, pr.RED)
    #         pr.end_mode_3d() # pr.end_mode_3d(cam)
    #         pr.end_drawing()
    #     pr.close_window()  