import bpy
from .. utils.ui import get_mouse_pos
from .. utils.system import printd
from .. utils.registration import get_prefs
from .. utils.workspace import is_fullscreen
from .. utils.asset import set_asset_library_reference
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

        # find_areas directly above or below the active area
        areas = self.get_areas(context, debug=False)


        # get regions
        regions = self.get_regions(context.area, debug=False)

        # get mouse pos
        get_mouse_pos(self, context, event, hud=False)

        # get the region type to toggle
        type = self.get_region_type_from_mouse(context, debug=False)

        # then toggle it
        self.toggle_region(context, areas, regions, type=type, debug=True)

        # context.area.tag_redraw()
        return {'FINISHED'}


    # UTILS

    def get_areas(self, context, debug=False):
        '''
        check the screen for areas exactly above or below the active area
        so they have to have the same x coord and width!
        '''

        active_area = context.area

        if debug:
            print()
            print("active area:", active_area.x, active_area.y, active_area.width, active_area.height)

        areas = {'TOP': None,
                 'BOTTOM': None}

        for area in context.screen.areas:
            if area == active_area:
                # if debug:
                #     print(">", area.type)
                continue
            else:
                if debug:
                    print(" ", area.type)
                    print("  ", area.x, area.y, area.width, area.height)

                if area.x == active_area.x and area.width == active_area.width:
                    location = 'BOTTOM' if area.y < active_area.y else 'TOP'

                    if debug:
                        print(f"   area is in the same 'column' and located at the {location}")

                    # replace existing location, if it is closer to the active one, compared to the previously stored region above or below the active
                    if areas[location]:
                        if location == 'BOTTOM' and area.y > areas[location].y:
                            areas[location] = area

                        elif location == 'TOP' and area.y < areas[location].y:
                            areas[location] = area

                    else:
                        areas[location] = area

        if debug:
            for location, area in areas.items():
                print(location)

                if area:
                    print("", area.type)

        return areas

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

    def toggle_region(self, context, areas, regions, type='TOOLS', debug=False):
        '''
        toggle region based on type arg
        '''

        # fetch settingsbpy.ops.screen.back_to_previous()
        asset_shelf = False
        below_area_split = 'ASSET_BROWSER'
        top_area_split = 'IMAGE_EDITOR'
        asset_split_factor = 0.2

        scale = context.preferences.system.ui_scale * get_prefs().modal_hud_scale


        if debug:
            print()
            print("toggling:", type)

        space = context.space_data

        # fetch the region that is being toggled
        region = regions[type] if type in regions else None


        # Toolbar

        if type == 'TOOLS':
            space.show_region_toolbar = not space.show_region_toolbar


        # Sidebar

        elif type == 'UI':
            space.show_region_ui = not space.show_region_ui

            if region:

                # it's possible the region can't be toggled because there is not enough space, in which case the width will be 1
                if region.width == 1:
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

        elif type in ['ASSET_BOTTOM', 'ASSET_TOP']:


            # TOGGLE ASSET SHELF

            if asset_shelf:
                space.show_region_asset_shelf = not space.show_region_asset_shelf

                if region:
                    if debug:
                        print("asset shelf region:", region)


            # SPLIT AREA 

            else:

                if is_fullscreen(context.screen):

                    coords = (context.region.width / 2, 100 * scale if type == 'ASSET_BOTTOM' else context.region.height - 100 * scale)
                    bpy.ops.machin3.draw_label(text="You can't Split this area in Fullscreen", coords=coords, color=red, alpha=1, time=2)


                else:
                    is_bottom = type == 'ASSET_BOTTOM'

                    if debug:
                        print(f"splitting the area to create assetbrowser at {'BOTTOM' if is_bottom else 'TOP'}")
                    
                    # close the existing area at the bottom or top, if present
                    if (is_bottom and areas['BOTTOM']) or (not is_bottom and areas['TOP']):
                        with context.temp_override(area=areas['BOTTOM' if is_bottom else 'TOP']):
                            bpy.ops.screen.area_close()

                    else:
                        if debug:
                            print(" there is no existing area bellow yet")

                        # fetch all exsiting areas
                        all_areas = [area for area in context.screen.areas]

                        # do the split
                        bpy.ops.screen.area_split(direction='HORIZONTAL', factor=asset_split_factor if is_bottom else 1 - asset_split_factor)

                        # find the new area
                        new_areas = [area for area in context.screen.areas if area not in all_areas]

                        # and make it an asset browser
                        if new_areas:
                            new_area = new_areas[0]
                            new_area.type = 'FILE_BROWSER'
                            new_area.ui_type = 'ASSETS'

                            context.area.tag_redraw()
                            new_area.tag_redraw()

                            # NOTE: there is some unpredictable behavior happening, most of the time the new area/screen will not have the tool bar shown
                            # ####: and what is odd is, that it can' be enabled by setting show_region_toolbar to True
                            # ####: but it can be enabled by reversing it? 
                            # ####: what's also odd is that, it always reads out as True
                            for new_space in new_area.spaces:
                                if new_space.type == 'FILE_BROWSER':
                                    new_space.show_region_toolbar = not new_space.show_region_toolbar

                                    # print()
                                    #
                                    # for d in dir(new_space):
                                    #     print("", d, getattr(new_space, d))

                                    # set_asset_library_reference(new_space.params, 'Library')

                                    # NOTE: space.params will be None, so we can't set Library, or any other of the spaces settings
                                    # ####: however, if you manually turn the 3d view into an asset browsr and set it up how you like, and then switch it back to a 3d view
                                    # ####: THEN the new split open asset browser will take all of these settings!



        # TODO?
        # show_region_header True
        # show_region_tool_header True
