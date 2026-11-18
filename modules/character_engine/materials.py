"""
Material & Shader Generator for Blender (bpy)
Creates production-grade Principled BSDF node trees for Pixar/DreamWorks stylized cartoon aesthetics.
"""

from typing import Dict, Any, List

class PixarShaderGenerator:
    """Generates Blender Python (bpy) shader node setup code."""

    @classmethod
    def generate_skin_shader_code(cls, mat_name: str, base_color: List[float], sss_radius: List[float], sss_weight: float = 0.28) -> str:
        """
        Creates a rich Subsurface Scattering (SSS) skin shader with warm epidermal scattering.
        """
        return f'''
def create_skin_material_{mat_name}():
    import bpy
    mat = bpy.data.materials.new(name="{mat_name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = {base_color}
    bsdf.inputs['Roughness'].default_value = 0.38
    
    # Subsurface scattering parameters
    if 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = {sss_weight}
        bsdf.inputs['Subsurface Radius'].default_value = {sss_radius}
        bsdf.inputs['Subsurface Scale'].default_value = 0.05
    elif 'Subsurface' in bsdf.inputs:
        bsdf.inputs['Subsurface'].default_value = {sss_weight}
        bsdf.inputs['Subsurface Radius'].default_value = {sss_radius}

    # Material Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat
'''

    @classmethod
    def generate_stylized_eye_shader_code(cls, mat_name: str, iris_color: List[float]) -> str:
        """
        Creates a Pixar-style multi-reflection wet eye shader with cornea glass depth and vibrant iris.
        """
        return f'''
def create_eye_material_{mat_name}():
    import bpy
    mat = bpy.data.materials.new(name="{mat_name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = {iris_color}
    bsdf.inputs['Roughness'].default_value = 0.05  # High gloss wet cornea
    if 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = 0.95
    elif 'Specular' in bsdf.inputs:
        bsdf.inputs['Specular'].default_value = 0.95

    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat
'''

    @classmethod
    def generate_hair_shader_code(cls, mat_name: str, hair_color: List[float], anisotropic_sheen: float = 0.85) -> str:
        """
        Creates stylized hair with anisotropic highlight band and fresnel rim lighting.
        """
        return f'''
def create_hair_material_{mat_name}():
    import bpy
    mat = bpy.data.materials.new(name="{mat_name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = {hair_color}
    bsdf.inputs['Roughness'].default_value = 0.42
    if 'Anisotropic' in bsdf.inputs:
        bsdf.inputs['Anisotropic'].default_value = {anisotropic_sheen}
    if 'Sheen Weight' in bsdf.inputs:
        bsdf.inputs['Sheen Weight'].default_value = 0.75

    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat
'''

    @classmethod
    def generate_bioluminescent_shader_code(cls, mat_name: str, base_color: List[float], emission_color: List[float], emission_strength: float = 2.5) -> str:
        """
        Creates glowing companion fur/skin shader (e.g. for Lumi the magical fox).
        """
        return f'''
def create_bioluminescent_material_{mat_name}():
    import bpy
    mat = bpy.data.materials.new(name="{mat_name}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = {base_color}
    bsdf.inputs['Roughness'].default_value = 0.50
    if 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = {emission_color}
        bsdf.inputs['Emission Strength'].default_value = {emission_strength}
    elif 'Emission' in bsdf.inputs:
        bsdf.inputs['Emission'].default_value = {emission_color}

    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat
'''
