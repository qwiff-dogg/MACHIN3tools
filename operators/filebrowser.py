import bpy
from bpy.props import StringProperty, BoolProperty
import os
from .. utils.system import abspath, open_folder
from .. utils.property import step_list


class Open(bpy.types.Operator):
    bl_idname = "machin3.filebrowser_open"
    bl_label = "MACHIN3: Open in System's filebrowser"
    bl_description = "Open the current location in the System's own filebrowser\nALT: Open .blend file"

    path: StringProperty(name="Path")
    blend_file: BoolProperty(name="Open .blend file")

    @classmethod
    def poll(cls, context):
        return context.area.type == 'FILE_BROWSER'

    def execute(self, context):
        params = context.space_data.params
        directory = abspath(params.directory.decode())

        if self.blend_file:
            active_file = context.active_file

            if active_file.asset_data:
                bpy.ops.asset.open_containing_blend_file()

            else:
                path = os.path.join(directory, active_file.relative_path)
                bpy.ops.machin3.open_library_blend(blendpath=path)

        else:
            open_folder(directory)

        return {'FINISHED'}


class Toggle(bpy.types.Operator):
    bl_idname = "machin3.filebrowser_toggle"
    bl_label = "MACHIN3: Toggle Filebrowser"
    bl_description = ""

    type: StringProperty()

    @classmethod
    def poll(cls, context):
        return context.area.type == 'FILE_BROWSER'

    def execute(self, context):

        # 1
        if self.type == 'SORT':

            # FILEBROWSER - toggle sorting by name or time
            if context.area.ui_type == 'FILES':
                if context.space_data.params.sort_method == 'FILE_SORT_ALPHA':
                    context.space_data.params.sort_method = 'FILE_SORT_TIME'

                else:
                    context.space_data.params.sort_method = 'FILE_SORT_ALPHA'

            # ASSETBROWSER - cycle asset liraries
            elif context.area.ui_type == 'ASSETS':
                base_libs = ['LOCAL']

                # TODO: make ALL and ESSENTIALS optional via addon prefs
                if bpy.app.version >= (3, 5, 0):
                    base_libs.insert(0, 'ALL')
                    base_libs.append('ESSENTIALS')

                asset_libraries = base_libs + [lib.name for lib in context.preferences.filepaths.asset_libraries]
                current = context.space_data.params.asset_library_ref

                context.space_data.params.asset_library_ref = step_list(current, asset_libraries, 1)

        # 2
        elif self.type == 'DISPLAY_TYPE':

            # FILEBROWSER - toggle display type
            if context.area.ui_type == 'FILES':
                if context.space_data.params.display_type == 'LIST_VERTICAL':
                    context.space_data.params.display_type = 'THUMBNAIL'

                else:
                    context.space_data.params.display_type = 'LIST_VERTICAL'

            # ASSETBROWSER - cycle import types
            elif context.area.ui_type == 'ASSETS':

                # only cycle importy types when you aren't in the LOCAL lib, in that case the prop is not used and is hidden in the UI, so you may end up changing it accidentally
                if context.space_data.params.asset_library_ref != 'LOCAL':
                    import_types = ['LINK', 'APPEND', 'APPEND_REUSE']

                    if bpy.app.version >= (3, 5, 0):
                        import_types.insert(0, 'FOLLOW_PREFS')

                    current = context.space_data.params.import_type
                    bpy.context.space_data.params.import_type = step_list(current, import_types, 1)

        # 4 toggle hidden files in asset browser
        elif self.type == 'HIDDEN':
            if context.area.ui_type == 'FILES':
                context.space_data.params.show_hidden = not context.space_data.params.show_hidden

        return {'FINISHED'}


class CycleThumbs(bpy.types.Operator):
    bl_idname = "machin3.filebrowser_cycle_thumbnail_size"
    bl_label = "MACHIN3: Cycle Thumbnail Size"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    reverse: BoolProperty(name="Reverse Cycle Diretion")

    @classmethod
    def poll(cls, context):
        return context.area.type == 'FILE_BROWSER' and context.space_data.params.display_type == 'THUMBNAIL'

    # 3  
    def execute(self, context):
        sizes = ['TINY', 'SMALL', 'NORMAL', 'LARGE']
        size = bpy.context.space_data.params.display_size
        bpy.context.space_data.params.display_size = step_list(size, sizes, -1 if self.reverse else 1, loop=True)

        return {'FINISHED'}
