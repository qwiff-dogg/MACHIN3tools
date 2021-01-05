import bpy
from mathutils import Vector
from . object import parent, unparent
from . math import average_locations, get_loc_matrix
from . registration import get_prefs


def get_group_polls(context):
    active_group = bool(context.active_object if context.active_object and context.active_object.M3.is_group_empty and context.active_object.select_get() else None)
    active_child = bool(context.active_object if context.active_object and context.active_object.M3.is_group_object and context.active_object.select_get() else None)
    group_empties = bool([obj for obj in context.visible_objects if obj.M3.is_group_empty])
    groupable = bool(len([obj for obj in context.selected_objects if not obj.parent]) > 1)
    regroupable = bool(len([obj for obj in context.selected_objects if obj.M3.is_group_object]) > 1)
    ungroupable = bool([obj for obj in context.selected_objects if obj.M3.is_group_empty]) if group_empties else False
    addable = bool([obj for obj in context.selected_objects if not obj.M3.is_group_object and not obj.parent and not obj == active_group and not obj == active_child])
    removable = bool([obj for obj in context.selected_objects if obj.M3.is_group_object])
    selectable = bool([obj for obj in context.selected_objects if obj.M3.is_group_empty or obj.M3.is_group_object])
    duplicatable = bool([obj for obj in context.selected_objects if obj.M3.is_group_empty])
    groupifyable = bool([obj for obj in context.selected_objects if obj.type == 'EMPTY' and not obj.M3.is_group_empty and obj.children])

    return active_group, active_child, group_empties, groupable, regroupable, ungroupable, addable, removable, selectable, duplicatable, groupifyable


def get_group_collection(context, sel):
    '''
    if all the objects in sel are in the same collection, return it
    otherwise return the master collection
    '''

    collections = set(col for obj in sel for col in obj.users_collection)

    if len(collections) == 1:
        return collections.pop()

    else:
        return context.scene.collection


def group(context, sel, location):
    col = get_group_collection(context, sel)

    empty = bpy.data.objects.new(name=get_base_group_name(), object_data=None)
    empty.M3.is_group_empty = True
    empty.matrix_world = get_group_matrix(context, location, sel)
    col.objects.link(empty)

    context.view_layer.objects.active = empty
    empty.select_set(True)
    empty.show_in_front = True
    empty.empty_display_type = 'CUBE'

    if context.scene.M3.group_hide:
        empty.show_name = False

        # 0.0001 is the smalled you can go
        empty.empty_display_size = 0.0001

    else:
        empty.show_name = True
        empty.empty_display_size = get_prefs().group_size

    empty.M3.group_size = get_prefs().group_size

    for obj in sel:
        parent(obj, empty)
        obj.M3.is_group_object = True


def ungroup(empty):
    for obj in empty.children:
        unparent(obj)
        obj.M3.is_group_object = False

    bpy.data.objects.remove(empty, do_unlink=True)


def get_group_matrix(context, location_type, objects):
    if location_type == 'AVERAGE':
        location = average_locations([obj.matrix_world.to_translation() for obj in objects])

    elif location_type == 'ACTIVE':
        if context.active_object:
            return context.active_object.matrix_world

        # fallback to average if no active object is present
        else:
            location = average_locations([obj.matrix_world.to_translation() for obj in objects])

    elif location_type == 'CURSOR':
        location = context.scene.cursor.location

    elif location_type == 'WORLD':
        location = Vector()

    return get_loc_matrix(location)


def select_group_children(empty, recursive=False):
    children = [c for c in empty.children if c.M3.is_group_object]

    for obj in children:
        obj.select_set(True)

        if obj.M3.is_group_empty and recursive:
            select_group_children(obj, recursive=True)


def get_base_group_name():
    p = get_prefs()

    if get_prefs().group_auto_name:
        name = f"{p.group_prefix}{p.group_basename + '_001'}{p.group_suffix}"

        c = 0
        while name in bpy.data.objects:
            c += 1
            name = f"{p.group_prefix}{p.group_basename + '_' + str(c).zfill(3)}{p.group_suffix}"

        return name

    else:
        name = f"{p.group_basename}_001"

        c = 0
        while name in bpy.data.objects:
            c += 1
            name = f"{p.group_basename + '_' + str(c).zfill(3)}"

        return name


def update_group_name(group):
    p = get_prefs()
    prefix = p.group_prefix
    suffix = p.group_suffix

    name = group.name
    newname = name

    if not name.startswith(prefix):
        newname = prefix + newname

    if not name.endswith(suffix):
        newname = newname + suffix

    if name == newname:
        return

    c = 0
    while newname in bpy.data.objects:
        c += 1
        newname = f"{p.group_prefix}{name + '_' + str(c).zfill(3)}{p.group_suffix}"

    group.name = newname