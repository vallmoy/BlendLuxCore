import bpy
from ..bin import pyluxcore
from .. import utils
from . import CacheEntry

def convert(blender_obj, scene, context, luxcore_scene):
    """
    datablock is of type bpy.types.Object
    """

    print("converting object:", blender_obj.name)
    luxcore_name = utils.to_luxcore_name(blender_obj.name)
    props = pyluxcore.Properties()

    if blender_obj.data is None:
        print("No mesh data")
        return props

    modifier_mode = "PREVIEW" if context else "RENDER"
    apply_modifiers = True
    mesh = blender_obj.to_mesh(scene, apply_modifiers, modifier_mode)

    if mesh is None or len(mesh.tessfaces) == 0:
        print("No mesh data after to_mesh()")
        return props

    mesh_definitions = __convert_mesh_to_shapes(luxcore_name, mesh, luxcore_scene)
    bpy.data.meshes.remove(mesh, do_unlink=False)

    # TODO: Remove test material
    props.Set(pyluxcore.Property("scene.materials.test.type", "matte"))
    props.Set(pyluxcore.Property("scene.materials.test.kd", [0.0, 0.7, 0.7]))

    for lux_object_name, material_index in mesh_definitions:
        transformation = utils.matrix_to_list(blender_obj.matrix_world)
        material_name = "test"
        __define_luxcore_object(props, lux_object_name, material_name, transformation)

    return props


def __define_luxcore_object(props, lux_object_name, lux_material_name, transformation=None):
    # This prefix is hardcoded in Scene_DefineBlenderMesh1 in the LuxCore API
    luxcore_shape_name = "Mesh-" + lux_object_name
    prefix = "scene.objects." + lux_object_name + "."
    props.Set(pyluxcore.Property(prefix + "material", lux_material_name))
    props.Set(pyluxcore.Property(prefix + "shape", luxcore_shape_name))
    if transformation:
        props.Set(pyluxcore.Property(prefix + "transformation", transformation))


def __convert_mesh_to_shapes(name, mesh, luxcore_scene):
    faces = mesh.tessfaces[0].as_pointer()
    vertices = mesh.vertices[0].as_pointer()

    uv_textures = mesh.tessface_uv_textures
    if len(uv_textures) > 0 and mesh.uv_textures.active and uv_textures.active.data:
        texCoords = uv_textures.active.data[0].as_pointer()
    else:
        texCoords = 0

    vertex_color = mesh.tessface_vertex_colors.active
    if vertex_color:
        vertexColors = vertex_color.data[0].as_pointer()
    else:
        vertexColors = 0

    # TODO
    transformation = None # if self.use_instancing else self.transformation

    return luxcore_scene.DefineBlenderMesh(name, len(mesh.tessfaces), faces, len(mesh.vertices),
                                           vertices, texCoords, vertexColors, transformation)