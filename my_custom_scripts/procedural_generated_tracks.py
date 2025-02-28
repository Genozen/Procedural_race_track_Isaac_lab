## Author: Nathan Hung 02/28/2025
"""
    This script performce procedural generated path and cones
"""


import numpy as np
import argparse

from isaaclab.app import AppLauncher

# create argparser
parser = argparse.ArgumentParser(description="Procedural Track Generation")

# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)

# parse the arguments
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


"""Rest everything follows."""
import isaacsim.core.utils.prims as prim_utils
import isaaclab.sim as sim_utils
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR





def design_scene():

    track_num = 1
    track_points_inner = np.load(f"track_{track_num}.npy")
    track_points_outer = np.load(f"track_offset_{track_num}.npy")
    # print(track_points)


    """Designs the scene by spawning ground plane, light, objects and meshes from usd files."""
    # Ground-plane
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/defaultGroundPlane", cfg_ground)


    # spawn distant light
    cfg_light_distant = sim_utils.DistantLightCfg(
        intensity=3000.0,
        color=(0.75, 0.75, 0.75),
    )

    cfg_light_distant.func("/World/lightDistant", cfg_light_distant, translation=(1, 0, 10))


    # create a new xform prim for all objects to be spawned under
    prim_utils.create_prim("/World/Objects", "Xform")

    # spawn a red cone
    cfg_cone = sim_utils.ConeCfg(
        radius=0.15,
        height=0.5,
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 0.0)),
    )
    # cfg_cone.func("/World/Objects/Cone1", cfg_cone, translation=(-1.0, 1.0, 0.0))
    # cfg_cone.func("/World/Objects/Cone2", cfg_cone, translation=(-1.0, -1.0, 0.0))

    cone_num = 1
    ori_x = track_points_inner[0][0]
    ori_y = track_points_inner[0][1]
    scale = 0.3
    for i in track_points_inner:
        cfg_cone.func(f"/World/Objects/Cone{cone_num}", cfg_cone, translation=((i[0] - ori_x)*scale, (i[1] - ori_y)*scale, 0.0))
        cone_num+=1


    cone_num = 1
    # ori_x = track_points_outer[0][0]
    # ori_y = track_points_outer[0][1]
    # scale = 0.3
    for i in track_points_outer:
        cfg_cone.func(f"/World/Objects/Cone{cone_num}_B", cfg_cone, translation=((i[0] - ori_x)*scale, (i[1] - ori_y)*scale, 0.0))
        cone_num+=1


def main():

    """Main function."""

    # Initialize the simulation context
    sim_cfg = sim_utils.SimulationCfg(dt=0.01, device=args_cli.device)

    sim = sim_utils.SimulationContext(sim_cfg)

    # Set main camera
    sim.set_camera_view([2.0, 0.0, 2.5], [-0.5, 0.0, 0.5])


    # Design scene by adding assets to it
    design_scene()


    # Play the simulator
    sim.reset()

    # Now we are ready!
    print("[INFO]: Setup complete...")


    # Simulate physics
    while simulation_app.is_running():
        # perform step
        sim.step()



if __name__ == "__main__":
    # run the main function
    main()

    # close sim app
    simulation_app.close()