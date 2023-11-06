import bpy
from bpy.utils import time_from_frame
from .. utils.ui import get_mouse_pos
from .. utils.system import printd
from .. utils.registration import get_prefs
from .. utils.workspace import is_fullscreen, get_assetbrowser_space
from .. utils.asset import get_asset_import_method, get_asset_library_reference, set_asset_import_method, set_asset_library_reference
from .. colors import red, yellow


class ToggleRegion(bpy.types.Operator):
    bl_idname = "machin3.toggle_region"
    bl_label = "MACHIN3: Toggle Reagion"
    bl_description = "Toggle 3D View Region based on Mouse Position"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.area.type in ['VIEW_3D']

    def invoke(self, context, event):

        # init asset_browser_prefs dict
        self.initiate_asset_browser_prefs(context, debug=False)

        # find_areas directly above or below the active area
        areas = self.get_areas(context, debug=False)

        # get regions
        regions = self.get_regions(context.area, debug=False)

        # get mouse pos
        get_mouse_pos(self, context, event, hud=False)

        # get the region type to toggle
        region_type = self.get_region_type_from_mouse(context, debug=False)

        # then toggle it
        self.toggle_region(context, areas, regions, region_type=region_type, debug=True)

        # context.area.tag_redraw()
        return {'FINISHED'}


    # UTILS

    def initiate_asset_browser_prefs(self, context, debug=False):
        '''
        1. ensure the asset browser prefs are stored on the scene level in a dict
        2. and reference it on the op via self.prefs
        3. then add the current screen to it, if it's not stored already
        '''

        if not context.scene.M3.get('asset_browser_prefs', False):
            context.scene.M3['asset_browser_prefs'] = {}

        self.prefs = context.scene.M3.get('asset_browser_prefs')

        # ensure the curretn screen is in the asset browser presf
        if context.screen.name not in self.prefs:
            # print("initiating asset browser prefs for screen", screen_name)

            empty = {'libref': 'ALL',
                     'catalog_id': '',
                     'import_method': 'FOLLOW_PREFS',
                     'header_align': 'TOP',
                     'show_region_toolbar': True,
                     'show_region_ui': False}

            self.prefs[context.screen.name] = {'ASSET_TOP': empty,
                                               'ASSET_BOTTOM': empty.copy()}

        if debug:
            printd(self.prefs.to_dict())

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

    def toggle_region(self, context, areas, regions, region_type='TOOLS', debug=False):
        '''
        toggle region based on type arg
        '''

        # if debug:
        #     print()
        #     print("toggling:", type)


        # get context
        area = context.area
        space = context.space_data
        region = regions[region_type] if region_type in regions else None
        screen_name = context.screen.name

        # get settingsbpy.ops.screen.back_to_previous()
        asset_shelf = False
        below_area_split = 'ASSET_BROWSER'
        top_area_split = 'IMAGE_EDITOR'
        asset_split_factor = 0.2
        scale = context.preferences.system.ui_scale * get_prefs().modal_hud_scale


        # Toolbar

        if region_type == 'TOOLS':
            space.show_region_toolbar = not space.show_region_toolbar


        # Sidebar

        elif region_type == 'UI':
            space.show_region_ui = not space.show_region_ui

            if region:

                # it's possible the region can't be toggled because there is not enough space, in which case the width will be 1
                if region.width == 1:
                    coords = (context.region.width / 2, 100 * scale)
                    bpy.ops.machin3.draw_label(text="Can't Toggle the Sidebar", coords=coords, color=red, alpha=1, time=1.2)

                    coords = (context.region.width / 2, (100 - 20) * scale)
                    bpy.ops.machin3.draw_label(text="Insufficient view space", coords=coords, color=red, alpha=1, time=1.5)


        # Redo Panel / Adjust Last Operation

        elif region_type == 'HUD':
            space.show_region_hud = not space.show_region_hud


        # Asset Shelf or Browser

        elif region_type in ['ASSET_BOTTOM', 'ASSET_TOP']:


            # TOGGLE ASSET SHELF

            if asset_shelf:
                space.show_region_asset_shelf = not space.show_region_asset_shelf


            # SPLIT AREA 

            else:

                if is_fullscreen(context.screen):

                    coords = (context.region.width / 2, 100 * scale if region_type == 'ASSET_BOTTOM' else context.region.height - 100 * scale)
                    bpy.ops.machin3.draw_label(text="You can't Split this area in Fullscreen", coords=coords, color=red, alpha=1, time=2)


                else:
                    is_bottom = region_type == 'ASSET_BOTTOM'
                    # print(f"splitting the area to create assetbrowser at {'BOTTOM' if is_bottom else 'TOP'}")


                    # TODO: only close the type of area you would open
                    # ####: for instance, don't close a fucking time line if you would open an asset browser

                    
                    # CLOSE EXISTING AREA at the BOTTOM or TOP, if present, and before you do, fetch it's properties and store them, for later restoration

                    if (is_bottom and areas['BOTTOM']) or (not is_bottom and areas['TOP']):
                        close_area = areas['BOTTOM' if is_bottom else 'TOP']

                        for space in close_area.spaces:
                            if space.type == 'FILE_BROWSER':
                                if space.params:
                                    libref = get_asset_library_reference(space.params)
                                    import_method = get_asset_import_method(space.params)

                                    self.prefs[screen_name][region_type]['libref'] = libref
                                    self.prefs[screen_name][region_type]['import_method'] = import_method
                                    self.prefs[screen_name][region_type]['catalog_id'] = space.params.catalog_id

                        for region in close_area.regions:
                            if region.type == 'HEADER':
                                self.prefs[screen_name][region_type]['header_align'] = region.alignment


                        with context.temp_override(area=close_area):
                            bpy.ops.screen.area_close()

 
                    # OPEN NEW AREA at BOTTOM or TOP

                    else:

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

                            # NOTE: some very odd behavior here, show_region_toolbar needs to be negated to maintain whatever 
                            for new_space in new_area.spaces:
                                if new_space.type == 'FILE_BROWSER':
                                    new_space.show_region_toolbar = not new_space.show_region_toolbar

                                    if new_space.params:
                                        if screen_name in self.prefs:
                                            libref = self.prefs[screen_name][region_type]['libref']
                                            import_method = self.prefs[screen_name][region_type]['import_method']
                                            catalog_id = self.prefs[screen_name][region_type]['catalog_id']

                                            set_asset_library_reference(new_space.params, libref)
                                            set_asset_import_method(new_space.params, import_method)

                                            new_space.params.catalog_id = catalog_id

                                        # flip HEADER region if necessary
                                        for region in new_area.regions:
                                            if region.type == 'HEADER':
                                                if region.alignment != self.prefs[screen_name][region_type]['header_align']:
                                                    with context.temp_override(area=new_area, region=region):
                                                        bpy.ops.screen.region_flip()

                                    # NOTE: space.params can be None, so we can't set Library, or any other of the spaces settings
                                    # ####: however, if you manually turn the 3d view into an asset browser and back into a 3d view again, then params will be available
                                    else:
                                        coords = (context.region.width / 2, 100 * scale if region_type == 'ASSET_BOTTOM' else context.region.height - (80 * scale + context.region.height * asset_split_factor))

                                        bpy.ops.machin3.draw_label(text="WARNING: Assetbrowser couldn't be set up yet", coords=coords, color=red, alpha=1, time=3)

                                        coords = (context.region.width / 2, 80 * scale if region_type == 'ASSET_BOTTOM' else context.region.height - (100 * scale + context.region.height * asset_split_factor))
                                        bpy.ops.machin3.draw_label(text="TO FIX IT, DO THIS: Change the 3D View into an Asset browser, and back again", coords=coords, color=yellow, alpha=1, time=4)

                                        coords = (context.region.width / 2, 60 * scale if region_type == 'ASSET_BOTTOM' else context.region.height - (120 * scale + context.region.height * asset_split_factor))
                                        bpy.ops.machin3.draw_label(text="Then save the blend file", coords=coords, color=yellow, alpha=1, time=5)


        # TODO?
        # show_region_header True
        # show_region_tool_header True


class AreaDumper(bpy.types.Operator):
    bl_idname = "machin3.area_dumper"
    bl_label = "MACHIN3: Area Dumper"
    bl_description = "description"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # return False
        return True

    def execute(self, context):

 

        # del context.scene.M3['asset_browser_prefs']

        for region in context.area.regions:
            if region.type == 'HEADER':
                with context.temp_override(region=region):
                    print("flipping", region, "of type", region.type)

                    bpy.ops.screen.region_flip()



        return {'FINISHED'}


        space = get_assetbrowser_space(context.area)

        # if space and space.params:
        #     for d in dir(space.params):
        #         print("", d, getattr(space.params, d))

        area = context.area

        print()
        print("area")

        for d in dir(area):
            print("", d, getattr(area, d))

        # print()
        # print("spaces")
        # for space in area.spaces:
        #     if space.type == 'FILE_BROWSER':
        #         for d in dir(space):
        #             print("", d, getattr(space, d))
        #
        #         if space.params:
        #             print()
        #             print("params")
        #
        #             for d in dir(space.params):
        #                 print("", d, getattr(space.params, d))
        #
        print()
        print("regions")
        for region in area.regions:
            print()
            print(region.type)

            for d in dir(region):
                print("", d, getattr(region, d))


        return {'FINISHED'}
