import bpy
from . registration import get_addon


decalmachine = None

def get_last_node(mat):
    if mat.use_nodes:
        tree = mat.node_tree
        output = tree.nodes.get("Material Output")
        if output:
            surf = output.inputs.get("Surface")
            if surf:
                if surf.links:
                    return surf.links[0].from_node


def lighten_color(color, amount):
    def remap(value, new_low):
        old_range = (1 - 0)
        new_range = (1 - new_low)
        return (((value - 0) * new_range) / old_range) + new_low

    return tuple(remap(c, amount) for c in color)


def adjust_bevel_shader(context, debug=False):
    '''
    go over all visible objects, to find all materials used by them
    for objects without any material a "white bevel" material is created, if use_bevel_shader is True
    for each of these materiasl try to find a "Bevel" node
        if use_bevel_shader is True, and none can be found check if the last node has a normal input without any links
            if so hook up a new bevel node

    if use_bevel_shader is True
        adjust the sample and radius values according to the m3 props
    if use_bevel_shader is False
        if white bevel material exists
            remove it 
        if it doesn't:
            remove the bevel node in the current mat, if it exists
    '''

    debug = True
    debug = False

    m3 = context.scene.M3

    if debug:
        print("\nadjusting bevel shader")
        print("use bevel:", m3.use_bevel_shader)

    visible_objs = [obj for obj in context.visible_objects if not any([obj.type == 'EMPTY', obj.display_type in ['WIRE', 'BOUNDS'], obj.hide_render])]
    # print("\nobjs:", [obj.name for obj in visible_objs])

    white_bevel = bpy.data.materials.get('white bevel')
    visible_mats = {white_bevel} if white_bevel else set()

    if debug:
        print("white bevel mat:", white_bevel)

    if debug:
        print("\nvisible objects")

    for obj in visible_objs:
        mats = [mat for mat in obj.data.materials if mat]

        # clear material stack if there are only empty slots
        if obj.data.materials and not mats:
            obj.data.materials.clear()

        if debug:
            print(obj.name, [mat.name for mat in mats])

        # create white bevel mat, if it doesnt exist yet, then add it to any object without materials
        if m3.use_bevel_shader and not mats:
            if not white_bevel:
                if debug:
                    print(" creating new white bevel material")

                white_bevel = bpy.data.materials.new('white bevel')
                white_bevel.use_nodes = True

            if debug:
                print(" assigning white bevel material")

            obj.data.materials.append(white_bevel)
            mats.append(white_bevel)
        
        # collect all visible materials in a set
        visible_mats.update(mats)

    # print("\nvisible mats:", [mat.name for mat in visible_mats])

    if debug:
        print("\nvisible materials")

    for mat in visible_mats:
        if debug:
            print(mat.name)

        tree = mat.node_tree
        bevel = tree.nodes.get('Bevel')

        # try to create bevel node
        if not bevel:
            if debug:
                print(" no bevel node found")

            last_node = get_last_node(mat)

            if last_node:
                if debug:
                    print("  found last node", last_node.name)

                normal_input = last_node.inputs.get('Normal')

                if normal_input and not normal_input.links:
                    if debug:
                        print("   has a normal input without links, creating bevel node and connecting it")

                    bevel = tree.nodes.new('ShaderNodeBevel')
                    bevel.location.x = last_node.location.x - 300

                    # for a newly created bevel mat, blender will return dimensions of 0 for the principled shader for some reason, so correct for that
                    y_dim = last_node.dimensions.y
                    if y_dim == 0:
                        y_dim = 660

                    bevel.location.y = last_node.location.y - y_dim + bevel.height

                    # link it to the normal output
                    tree.links.new(bevel.outputs[0], normal_input)

                # couldn't find a normal input, moving on to the next material
                else:
                    continue

            # couldn't find last node, moving on to the next material
            else:
                continue

        # set bevel node props
        if m3.use_bevel_shader:

            if bevel.samples != m3.bevel_shader_samples:
                if debug:
                    print(" setting bevel samples to:", m3.bevel_shader_samples)

                bevel.samples = m3.bevel_shader_samples

            if bevel.inputs[0].default_value != m3.bevel_shader_radius:
                if debug:
                    print(" setting bevel radius to:", m3.bevel_shader_radius)

                bevel.inputs[0].default_value = m3.bevel_shader_radius
        
        # remove bevel nodes and white bevel mat
        else:
            if mat == white_bevel:
                if debug:
                    print(" removing white bevel material")

                bpy.data.materials.remove(mat, do_unlink=True)

            elif bevel:
                if debug:
                    print(" removing bevel node")

                tree.nodes.remove(bevel)
