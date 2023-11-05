import bpy
from .. utils.ui import get_mouse_pos
from .. utils.system import printd
from .. utils.registration import get_prefs
from .. colors import red


class ToggleRegion(bpy.types.Operator):
    bl_idname = "machin3.toggle_region"
    bl_label = "MACHIN3: Toggle Reagion"
    bl_description = "Toggle 3D View Region based on Mouse Position"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.area.type in ['VIEW_3D']

    def invoke(self, context, event):

        # get regions
        regions = self.get_regions(context.area, debug=False)

        # get mouse pos
        get_mouse_pos(self, context, event, hud=False)

        # get the region type to toggle
        type = self.get_region_type_from_mouse(context, debug=False)

        # then toggle it
        self.toggle_region(context, regions, type=type, debug=True)

        context.area.tag_redraw()
        return {'FINISHED'}


    # UTILS

    def get_regions(self, area, debug=False):
        '''
        collect toolbar, sidebar, redo panel and asset shelf regions in a dict
        ignore others like WINDOW, HEADR, ASSET_SHELF_HEADER
        '''
        
        regions = {}

        for region in area.regions:
            if region.type in ['TOOLS', 'UI', 'HUD', 'ASSET_SHELF']:
                regions[region.type] = region


        if debug:
            printd(regions)

        return regions

    def get_region_type_from_mouse(self, context, debug=False):
        '''
        from the mouse position, get the type of the region you want to toggle
        unless it's over a non-WINDOW region already, then just toggle this one
        '''

        close_range = 25
        prefer_left_right = True  # TODO: addon prefs

        if context.region.type == 'WINDOW':
            area = context.area

            # get mouse position expresed in percentages
            x_pct = (self.mouse_pos.x / area.width) * 100
            y_pct = (self.mouse_pos.y / area.height) * 100

            is_left = x_pct < 50
            is_bottom = y_pct < 50


            # check left/right sides first, and only choose bottom/top if within close range
            if prefer_left_right:
                side = 'LEFT' if is_left else 'RIGHT'

                if y_pct <= close_range:
                    side = 'BOTTOM'

                elif y_pct >= 100 - close_range:
                    side = 'TOP'

            # check bottom/top sides first, and only choose left/right if within close range
            else:
                side = 'BOTTOM' if is_bottom else 'TOP'

                if x_pct <= close_range:
                    side = 'LEFT'

                elif x_pct >= 100 - close_range:
                    side = 'RIGHT'


            if debug:
                # print()
                # print("area")
                # print(f" width x height: {area.width} x {area.height}")
                #
                # print()
                # print("mouse")
                # # print(f" x x y: {self.mouse_pos.x} x {self.mouse_pos.y}")
                # print(f" x x y: {x_pct}% x {y_pct}%")
                #
                # print()
                # print("sides")
                # print(" is left:", is_left)
                # print(" is bottom:", is_bottom)

                print()
                print(f"side: {side}")


            if side == 'LEFT':
                return 'TOOLS'

            elif side == 'RIGHT':
                return 'UI'

            elif side == 'BOTTOM':
                return 'ASSET_BOTTOM'

            elif side == 'TOP':
                return 'ASSET_TOP'

        else:
            return context.region.type

    def toggle_region(self, context, regions, type='TOOLS', debug=False):
        '''
        toggle region based on type arg
        '''

        if debug:
            print()
            print("toggling:", type)

        space = context.space_data

        # fetch the region that is being toggled
        region = regions[type] if type in regions else None

        # the asset shelf is pretty limited right now, so don't use it yet
        asset_shelf = False


        # Toolbar

        if type == 'TOOLS':
            space.show_region_toolbar = not space.show_region_toolbar


        # Sidebar

        elif type == 'UI':
            space.show_region_ui = not space.show_region_ui

            if region:

                # it's possible the region can't be toggled because there is not enough space, in which case the width will be 1
                if region.width == 1:
                    scale = context.preferences.system.ui_scale * get_prefs().modal_hud_scale
                    coords = (context.region.width / 2, 100 * scale)
                    bpy.ops.machin3.draw_label(text="Can't Toggle the Sidebar", coords=coords, color=red, alpha=1, time=1.2)

                    coords = (context.region.width / 2, (100 - 20) * scale)
                    bpy.ops.machin3.draw_label(text="Insufficient view space", coords=coords, color=red, alpha=1, time=1.5)


        # Redo Panel / Adjust Last Operation

        elif type == 'HUD':
            space.show_region_hud = not space.show_region_hud

            if region:
                if debug:
                    print("redo region:", region)


        # Asset Shelf or Browser

        elif type == 'ASSET_BOTTOM':

            if asset_shelf:
                space.show_region_asset_shelf = not space.show_region_asset_shelf

                if region:
                    if debug:
                        print("asset shelf region:", region)

            else:
                # TODO: split bottom area

                if debug:
                    print("splitting the area to create assetbrowser at BOTTOM")


        elif type == 'ASSET_TOP':

                # TODO: split top area

                if debug:
                    print("splitting the area to create assetbrowser at TOP")

        
        # TODO?
        # show_region_header True
        # show_region_tool_header True
