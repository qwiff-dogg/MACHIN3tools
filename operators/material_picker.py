import bpy
from bpy.props import BoolProperty
from bl_ui.space_statusbar import STATUSBAR_HT_header as statusbar
from mathutils import Vector
import os
from .. utils.raycast import cast_obj_ray_from_mouse, cast_bvh_ray_from_mouse
from .. utils.draw import draw_label, update_HUD_location, draw_init
from .. utils.registration import get_prefs
from .. utils.system import printd
from .. utils.ui import init_cursor, init_status, finish_status
from .. items import alt, ctrl
from .. colors import white, yellow, green, red


def draw_material_pick_status(op):
    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.label(text=f"Material Picker")

        if op.assign_from_assetbrowser:
            row.label(text="Assign Material from Asset Browsr to Object under Mouse")

        else:
            row.label(text="", icon='MOUSE_LMB')
            
            if op.assign:
                row.label(text="Pick Material and Assign it to Selected Objects")

            else:
                row.label(text="Pick Material and Finish")

        row.label(text="", icon='MOUSE_MMB')
        row.label(text="Viewport")

        row.label(text="", icon='MOUSE_RMB')
        row.label(text="Cancel")

        row.label(text="", icon='EVENT_SPACEKEY')
        row.label(text="Finish")

        row.separator(factor=10)

        row.label(text="", icon='EVENT_ALT')
        row.label(text=f"Assign Material: {op.assign}")

        if op.asset_browser:
            row.label(text="", icon='EVENT_CTRL')
            row.label(text=f"Assign Material from Asset Browser: {op.assign_from_assetbrowser}")

    return draw


class MaterialPicker(bpy.types.Operator):
    bl_idname = "machin3.material_picker"
    bl_label = "MACHIN3: Material Picker"
    bl_description = "Pick a Material from the 3D View\nALT: Assign it to the Selection too"
    bl_options = {'REGISTER', 'UNDO'}

    # hidden
    passthrough = None

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def draw_HUD(self, context):
        draw_init(self, None)

        title, color = ("Assign from Asset Browser ", green) if self.assign_from_assetbrowser else ("Assign", yellow) if self.assign else ("Pick", white)
        dims = draw_label(context, title=title, coords=Vector((self.HUD_x, self.HUD_y)), color=color, center=False, return_dimensions=True)

        if self.assign_from_assetbrowser:
            draw_label(context, title=self.asset['import_type'], coords=Vector((self.HUD_x + dims[0], self.HUD_y)), center=False, color=white, alpha=0.5, return_dimensions=True)

            self.offset += 18

            if self.asset:
                asset_type = self.asset['asset_type']

                if asset_type == 'Material':
                    title = f"{self.asset['library']} • {self.asset['blend_name']} • "
                    dims = draw_label(context, title=title, coords=Vector((self.HUD_x, self.HUD_y)), offset=self.offset, center=False, color=white, alpha=0.5, return_dimensions=True)

                    title = f"{self.asset['asset_name']}"
                    draw_label(context, title=title, coords=Vector((self.HUD_x + dims[0], self.HUD_y)), offset=self.offset, center=False, color=white)

                else:
                    draw_label(context, title=f"Can't assign {asset_type} asset as a Material", coords=Vector((self.HUD_x, self.HUD_y)), offset=self.offset, color=red, center=False)
            else:
                draw_label(context, title="No Asset Selected in Asset Browser", coords=Vector((self.HUD_x, self.HUD_y)), offset=self.offset, color=red, center=False)

        else:
            self.offset += 18

            color = red if self.pick_material_name == 'None' else white

            dims = draw_label(context, title='Material ', coords=Vector((self.HUD_x, self.HUD_y)), offset=self.offset, center=False, color=white, alpha=0.5, return_dimensions=True)
            draw_label(context, title=self.pick_material_name, coords=Vector((self.HUD_x + dims[0], self.HUD_y)), offset=self.offset, center=False, color=color, alpha=1)


    def modal(self, context, event):
        context.area.tag_redraw()

        self.mousepos = Vector((event.mouse_region_x, event.mouse_region_y))
        self.mousepos_screen = Vector((event.mouse_x, event.mouse_y))


        area_under_mouse = self.get_area_under_mouse(self.mousepos_screen)
        # print("area under mouse:", area_under_mouse)

        # restore mouse eyedropper mouse cursor, and fetch the selected asset from the asset browser
        if self.passthrough and area_under_mouse != 'ASSET_BROWSER':
            self.passthrough = False
            context.window.cursor_set("EYEDROPPER")

            # fetch selected asset from asset browser
            self.asset = self.get_selected_asset()

            if self.asset:
                printd(self.asset)


        # PASSTROUGH to ASSET BROWSER

        if area_under_mouse == 'ASSET_BROWSER':
            self.passthrough = True
            return {'PASS_THROUGH'}


        # VIEW3D

        elif area_under_mouse == 'VIEW_3D':

            # MOD KEYS

            self.assign = event.alt

            if 'ASSET_BROWSER' in self.areas:
                self.assign_from_assetbrowser = event.ctrl

                if self.assign_from_assetbrowser:
                    self.assign = False

            if event.type in [*alt, *ctrl]:
                if event.value == 'PRESS':
                    context.window.cursor_set("PAINT_CROSS")


                elif event.value == 'RELEASE':
                    context.window.cursor_set("EYEDROPPER")
                
                # force statusbar update
                if context.visible_objects:
                    context.visible_objects[0].select_set(context.visible_objects[0].select_get())


            # MOUSEMOVE

            if event.type == 'MOUSEMOVE':
                update_HUD_location(self, event)

                # fetch material via raycast in pick and assign modes, but not when assigning from the asset browser
                if not self.assign_from_assetbrowser:
                    hitobj, matindex = self.get_material_hit(context, self.mousepos, debug=False)

                    # try to fetch the material from the hit and stroe its name on the op
                    mat, self.pick_material_name = self.get_material_from_hit(hitobj, matindex)


            # FINISH

            elif event.type == 'LEFTMOUSE':

                hitobj, matindex = self.get_material_hit(context, self.mousepos, debug=False)

                if hitobj:

                    # PICK - make the hitobject and its material (slot) active

                    context.view_layer.objects.active = hitobj
                    hitobj.active_material_index = matindex

                    if self.assign_from_assetbrowser:

                        # Import Material from ASSETBROWSER and assign it to the picked object at matindex

                        if self.assign_from_assetbrowser:
                            if self.asset['asset_type'] == 'Material':
                                import_type = self.asset['import_type']
                                directory = os.path.join(self.asset['blendpath'], 'Material')
                                filename = self.asset['asset_name']

                                # print("\nassset browser material import")
                                mat = bpy.data.materials.get(filename)

                                if mat:
                                    # print(" a material of this name exists already:", mat)
                                    pass

                                else:
                                    # print(" import type:", import_type)
                                    # print(" directory:", directory)
                                    # print(" filename:", filename)

                                    if 'Append' in import_type:
                                        reuse_local_id= 'Reuse' in import_type
                                        bpy.ops.wm.append(directory=directory, filename=filename, do_reuse_local_id=reuse_local_id)

                                    else:
                                        bpy.ops.wm.link(directory=directory, filename=filename)

                                    mat = bpy.data.materials.get(filename)
                                    # print(" imported material:", mat)

                                    # disable fake user
                                    if mat.use_fake_user:
                                        mat.use_fake_user = False

                                # apply the material at the matindex
                                print(" applying to obj", hitobj.name, "at index", matindex)
                                hitobj.material_slots[matindex].material = mat

                        # don't finish the modal in this case, finish using space instead
                        return {'RUNNING_MODAL'}


                    # ASSIGN - assign the picked material to the selection of objects

                    elif self.assign:
                        mat, matname = self.get_material_from_hit(hitobj, matindex)

                        if mat:
                            sel = [obj for obj in context.selected_objects if obj != hitobj and obj.data]

                            for obj in sel:
                                if not obj.material_slots:
                                    obj.data.materials.append(mat)

                                else:
                                    obj.material_slots[obj.active_material_index].material = mat

                self.finish(context)

                return {'FINISHED'}


            # FINISH with SPACE

            elif event.type == 'SPACE':
                self.finish(context)
                return {'FINISHED'}


            # NAV PASSTHROUGH

            elif event.type == 'MIDDLEMOUSE':
                return {'PASS_THROUGH'}


            # CANCEL

            elif event.type in ['RIGHTMOUSE', 'ESC']:
                self.finish(context)
                return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def finish(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self.HUD, 'WINDOW')

        context.window.cursor_set("DEFAULT")

        # reset statusbar
        finish_status(self)

        if context.visible_objects:
            context.visible_objects[0].select_set(context.visible_objects[0].select_get())

    def invoke(self, context, event):

        # init
        self.assign = False 
        self.assign_from_assetbrowser = False 
        self.pick_material_name = "None"

        # get the depsgraph
        self.dg = context.evaluated_depsgraph_get()

        # init mouse cursor
        init_cursor(self, event)
        context.window.cursor_set("EYEDROPPER")

        # check the active screen and fetch all areas and their position/dimenension
        self.areas, self.asset_browser = self.get_areas(context)

        # then fetch the selected asset
        self.asset = self.get_selected_asset()

        # int statusbar
        init_status(self, context, func=draw_material_pick_status(self))

        if context.visible_objects:
            context.visible_objects[0].select_set(context.visible_objects[0].select_get())

        # handlers
        self.HUD = bpy.types.SpaceView3D.draw_handler_add(self.draw_HUD, (context, ), 'WINDOW', 'POST_PIXEL')

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def get_areas(self, context):
        '''
        check the active screen and fetch all areas and their position/dimenension
        '''

        areas = {}
        asset_browser = None

        for area in context.screen.areas:
            if area.type == 'FILE_BROWSER' and area.ui_type == 'ASSETS':
                area_type = 'ASSET_BROWSER'
                asset_browser = area.spaces.active.params

            else:
                area_type = area.type

            # print("     x:", area.x)
            # print("     y:", area.y)
            # print(" width:", area.width)
            # print("height:", area.height)

            areas[area_type] = {'x': (area.x, area.x + area.width),
                                'y': (area.y, area.y + area.height)}

        return areas, asset_browser

    def get_area_under_mouse(self, mousepos):
        '''
        return name of area, under ther mouse
        '''

        for areaname, coords in self.areas.items():
            if coords['x'][0] <= self.mousepos_screen.x <= coords['x'][1]:
                # print(" in x of", areaname)

                if coords['y'][0] <= self.mousepos_screen.y <= coords['y'][1]:
                    # print(" in y of", areaname, "too")
                    return areaname

    def get_selected_asset(self):
        '''
        from the asset browser, fetch the selected asset
        '''

        asset = None

        if self.asset_browser:
            ab = self.asset_browser

            directory = ab.directory.decode().replace('\\', '/')
            filename = ab.filename.replace('\\', '/')

            split = filename.split('/')

            blendpath = os.path.join(directory, split[0])
            blend_name = split[0].replace('.blend', '')
            asset_type, asset_name = split[1:3]

            asset = {'import_type': ab.import_type.title().replace('_', ' '),
                     'library': ab.asset_library_ref,
                     'catalog_id': ab.catalog_id,
                     'blendpath': blendpath,
                     'blend_name': blend_name,
                     'asset_type': asset_type,
                     'asset_name': asset_name}

            printd(asset)

        else:
            print("there is no asset browser")

        return asset

    def get_material_hit(self, context, mousepos, debug=False):
        '''
        cat ray in object or edit mode and return the hit object and material index
        '''

        if debug:
            print("\nmaterial hitting at", mousepos)
        
        if context.mode == 'OBJECT':
            hitobj, hitobj_eval, _, _, hitindex, _ = cast_obj_ray_from_mouse(self.mousepos, depsgraph=self.dg, debug=False)

        elif context.mode == 'EDIT_MESH':
            hitobj, _, _, hitindex, _, _ = cast_bvh_ray_from_mouse(self.mousepos, candidates=[obj for obj in context.visible_objects if obj.mode == 'EDIT'], debug=False)

        if hitobj:

            if context.mode == 'OBJECT':
                matindex = hitobj_eval.data.polygons[hitindex].material_index
            elif context.mode == 'EDIT_MESH':
                matindex = hitobj.data.polygons[hitindex].material_index

            # if debug:
            if True:
                print(" hit object:", hitobj.name, "material index:", matindex)

            # NOTE: safe-guard against crazy big material indices, which can happen as a result of (live?) booleans
            matindex = min(matindex, len(hitobj.material_slots) - 1)

            return hitobj, matindex

        if debug:
            print(" nothing hit")
        return None, None

    def get_material_from_hit(self, obj, index):
        '''
        from the passed in object and material index, return the material, if there is ona at the stack index
        return None, if either argument is None or there is no material are the passed in index
        '''

        if obj and index is not None:
            if obj.material_slots and obj.material_slots[index].material:
                mat = obj.material_slots[index].material
                return mat, mat.name
        return None, 'None'
