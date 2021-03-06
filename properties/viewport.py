import bpy
from bpy.props import IntProperty, EnumProperty, BoolProperty

DESC_CPU = "Usually better suited for viewport rendering than OpenCL."
DESC_OCL = (
    "Use the GPUs specified in the device panel. Note that rendering on the GPU leads to "
    "higher latency and sometimes requires kernel recompilations when editing the scene"
)


class LuxCoreViewportSettings(bpy.types.PropertyGroup):
    halt_time = IntProperty(name="Viewport Halt Time (s)", default=10, min=1,
                            description="How long to render in the viewport."
                                        "When this time is reached, the render is paused")

    devices = [
        ("CPU", "CPU", DESC_CPU, 0),
        ("OCL", "OpenCL", DESC_OCL, 1),
    ]
    device = EnumProperty(name="Device", items=devices, default="CPU")

    pixel_sizes = [
        ("1", "1x", "Use the native resolution of the monitor (1 rendered pixel = 1 displayed pixel)", 0),
        ("2", "2x", "Use half the resolution of the monitor (1 rendered pixel = 2x2 displayed pixels)", 1),
        ("4", "4x", "1 rendered pixel = 4x4 displayed pixels", 2),
        ("8", "8x", "1 rendered pixel = 8x8 displayed pixels", 3),
    ]
    pixel_size = EnumProperty(name="Pixel Size", items=pixel_sizes, default="1",
                              description="Scale factor for rendered pixels")

    mag_filters = [
        ("NEAREST", "Nearest (blocky)", "", 0),
        ("LINEAR", "Linear (smooth)", "", 1),
    ]
    mag_filter = EnumProperty(name="Filter", items=mag_filters, default="NEAREST",
                              description="Upscaling filter used when pixel size is larger than 1")

    reduce_resolution_on_edit = BoolProperty(name="Reduce first sample resolution", default=True,
                                             description="Render the first sample after editing the scene "
                                                         "with reduced resolution to provide a quicker response")
