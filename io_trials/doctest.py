import xarray as xr
import numpy as np
ds = xr.Dataset()
ds["mesh2d"] = xr.DataArray(
    data=0,
    attrs={
     "cf_role": "mesh_topology",
     "long_name": "Topology data of 2D mesh",
     "topology_dimension": 2,
     "node_coordinates": "node_x node_y",
     "face_node_connectivity": "face_nodes",
    }
)
ds = ds.assign_coords(
    node_x=xr.DataArray(
        data=np.array([0.0, 10.0, 10.0, 0.0, 20.0, 20.0]),
        dims=["node"],
    )
)
ds = ds.assign_coords(
    node_y=xr.DataArray(
        data=np.array([0.0, 0.0, 10.0, 10.0, 0.0, 10.0]),
        dims=["node"],
    )
)
ds["face_nodes"] = xr.DataArray(
    data=np.array([
        [0, 1, 2, 3],
        [1, 4, 5, -1]
    ]),
    coords={
        "face_x": ("face", np.array([5.0, 15.0])),
        "face_y": ("face", np.array([5.0, 5.0])),
    },
    dims=["face", "nmax_face"],
    attrs={
        "cf_role": "face_node_connectivity",
        "long_name": "Vertex nodes of mesh faces (counterclockwise)",
        "start_index": 0,
        "_FillValue": -1,
    }
)

print(ds)

