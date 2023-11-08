import bpy
from bpy.types import CompositorNodeAntiAliasing
from bpy.utils import time_from_frame
from .. utils.ui import get_mouse_pos, warp_mouse, get_window_space_co2d
from .. utils.system import printd
from .. utils.registration import get_prefs
from .. utils.workspace import is_fullscreen, get_assetbrowser_space
from .. utils.asset import get_asset_import_method, get_asset_library_reference, set_asset_import_method, set_asset_library_reference
from .. colors import red, yellow


supress_assetbrowser_toggle = False

class ToggleVIEW3DRegion(bpy.types.Operator):
    bl_idname = "machin3.toggle_view3d_region"
    bl_label = "MACHIN3: Toggle 3D View Region"
    bl_description = "Toggle 3D View Region based on Mouse Position"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if context.area:
            return context.area.type == 'VIEW_3D'

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
        area = self.toggle_region(context, areas, regions, region_type, debug=False)

        # warp the mouse to the region border, so it can be adjusted right away if the user choses so
        if get_prefs().region_warp_mouse_to_asset_border:
            self.warp_mouse_to_border(context, area, region_type)

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
            print("initiating asset browser prefs on scene object")

        self.prefs = context.scene.M3.get('asset_browser_prefs')

        # ensure the curretn screen is in the asset browser presf
        if context.screen.name not in self.prefs:
            print("initiating asset browser prefs for screen", context.screen.name)

            empty = {'area_height': 250,

                     'libref': 'ALL',
                     'catalog_id': '',
                     'import_method': 'FOLLOW_PREFS',
                     'display_size': 96 if bpy.app.version >= (4, 0, 0) else 'SMALL',

                     'header_align': 'TOP',

                     'show_region_toolbar': True,
                     'show_region_tool_props': False,

                     'filter_search': '',
                     'filter_action': True,
                     'filter_group': True,
                     'filter_material': True,
                     'filter_node_tree': True,
                     'filter_object': True,
                     'filter_world': True,
                     }

            self.prefs[context.screen.name] = {'ASSET_TOP': empty,
                                               'ASSET_BOTTOM': empty.copy()}

        # if True:
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
                 'BOTTOM': None,
                 'ACTIVE': active_area}

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
        ignore others like WINDOW, HEADER, ASSET_SHELF_HEADER
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

        prefer_left_right = get_prefs().region_prefer_left_right
        close_range = get_prefs().region_close_range

        if context.region.type in ['WINDOW', 'HEADER', 'TOOL_HEADER']:
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
        #     print("toggling:", region_type)

        # get context
        space = context.space_data
        region = regions[region_type] if region_type in regions else None
        screen_name = context.screen.name

        # get settingsbpy.ops.screen.back_to_previous()
        asset_shelf = get_prefs().region_toggle_assetshelf
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


            # SPLIT or CLOSE AREA 

            else:

                if is_fullscreen(context.screen):
                    coords = (context.region.width / 2, 100 * scale if region_type == 'ASSET_BOTTOM' else context.region.height - 100 * scale)
                    bpy.ops.machin3.draw_label(text="You can't Split this area in Fullscreen", coords=coords, color=red, alpha=1, time=2)

                else:
                    return self.toggle_area(context, areas, region_type, screen_name, scale)

        # TODO?
        # show_region_header True
        # show_region_tool_header True

    def toggle_area(self, context, areas, region_type, screen_name, scale):
        '''
        "toggle" area, by splitting the current area or closing the one above or below the current one
        '''

        # print(f"splitting the area to create assetbrowser at {'BOTTOM' if is_bottom else 'TOP'}")

        # get settings
        below_area_split = 'ASSET_BROWSER'
        top_area_split = 'ASSET_BROWSER'
        is_bottom = region_type == 'ASSET_BOTTOM'


        # CLOSE EXISTING AREA at the BOTTOM or TOP, if present, and before you do, fetch it's properties and store them, for later restoration

        close_area = areas['BOTTOM' if is_bottom else 'TOP']

        if close_area and self.is_close_area_of_type(close_area, 'ASSET_BROWSER'):
            self.store_asset_browser_area_settings(context, close_area, region_type, screen_name)

            with context.temp_override(area=close_area):
                bpy.ops.screen.area_close()


        # OPEN NEW AREA at BOTTOM or TOP

        else:

            # NOTE: supress automatic invokation of ToggleASSETBROWSERRegion()
            # ####: for some reason this happens due to the split op I think, but not sure actually

            global supress_assetbrowser_toggle
            supress_assetbrowser_toggle = True

            # calculate the area split factor
            area_split_factor = self.get_area_split_factor(context, areas['ACTIVE'].height, self.prefs[screen_name][region_type]['area_height'], is_bottom)

            # fetch all currently existing areas
            all_areas = [area for area in context.screen.areas]

            # do the split
            bpy.ops.screen.area_split(direction='HORIZONTAL', factor=area_split_factor if is_bottom else 1 - area_split_factor)

            # find the new area by comparison
            new_areas = [area for area in context.screen.areas if area not in all_areas]

            # and turn it into an asset browser
            if new_areas:
                new_area = new_areas[0]
                new_area.type = 'FILE_BROWSER'
                new_area.ui_type = 'ASSETS'

                for new_space in new_area.spaces:
                    if new_space.type == 'FILE_BROWSER':

                        # restore settings 

                        if new_space.params:
                            if screen_name in self.prefs:


                                # fetch them
                                libref = self.prefs[screen_name][region_type]['libref']
                                import_method = self.prefs[screen_name][region_type]['import_method']
                                catalog_id = self.prefs[screen_name][region_type]['catalog_id']
                                display_size = self.prefs[screen_name][region_type]['display_size']

                                show_region_toolbar = self.prefs[screen_name][region_type]['show_region_toolbar']
                                show_region_tool_props = self.prefs[screen_name][region_type]['show_region_tool_props']

                                filter_search = self.prefs[screen_name][region_type]['filter_search']
                                filter_action = self.prefs[screen_name][region_type]['filter_action']
                                filter_group = self.prefs[screen_name][region_type]['filter_group']
                                filter_material = self.prefs[screen_name][region_type]['filter_material']
                                filter_node_tree = self.prefs[screen_name][region_type]['filter_node_tree']
                                filter_object = self.prefs[screen_name][region_type]['filter_object']
                                filter_world = self.prefs[screen_name][region_type]['filter_world']

                                # then set them
                                set_asset_library_reference(new_space.params, libref)
                                set_asset_import_method(new_space.params, import_method)
                                new_space.params.catalog_id = catalog_id
                                new_space.params.display_size = display_size

                                # NOTE: some very odd behavior here, show_region_toolbar needs to be negated to maintain whatever was set, but even that may not always work
                                # new_space.show_region_toolbar = not show_region_toolbar
                                # NOTE: I think it was due to the T key still being passed through, so the normal toggle took over!
                                # ####: it's no longer happening now, that the ToggleASSETBROWSERRegion() takes over in that region
                                new_space.show_region_toolbar = show_region_toolbar

                                # set the 'N panel' too, which in the FILE_BROWSER is called show_region_tool_props, not show_region_UI like in the 3d view!
                                new_space.show_region_tool_props = show_region_tool_props

                                new_space.params.filter_search = filter_search
                                new_space.params.filter_asset_id.filter_action = filter_action
                                new_space.params.filter_asset_id.filter_group = filter_group
                                new_space.params.filter_asset_id.filter_material = filter_material
                                new_space.params.filter_asset_id.filter_node_tree = filter_node_tree
                                new_space.params.filter_asset_id.filter_object = filter_object
                                new_space.params.filter_asset_id.filter_world = filter_world

                                # finalyl flip the HEADER region if necessary
                                for region in new_area.regions:
                                    if region.type == 'HEADER':
                                        if region.alignment != self.prefs[screen_name][region_type]['header_align']:
                                            with context.temp_override(area=new_area, region=region):
                                                bpy.ops.screen.region_flip()


                        # NOTE: space.params can be None, so we can't set Library, or any other of the spaces settings
                        # ####: however, if you manually turn the 3d view into an asset browser and back into a 3d view again, then params will be available
                        else:
                            coords = (context.region.width / 2, 100 * scale if region_type == 'ASSET_BOTTOM' else context.region.height - (80 * scale + context.region.height * area_split_factor))

                            bpy.ops.machin3.draw_label(text="WARNING: Assetbrowser couldn't be set up yet, due to Blender shenanigans", coords=coords, color=red, alpha=1, time=3)

                            coords = (context.region.width / 2, 80 * scale if region_type == 'ASSET_BOTTOM' else context.region.height - (100 * scale + context.region.height * area_split_factor))
                            bpy.ops.machin3.draw_label(text="TO FIX IT, DO THIS: Change THIS 3D View into an Asset browser, and back again", coords=coords, color=yellow, alpha=1, time=4)

                            coords = (context.region.width / 2, 60 * scale if region_type == 'ASSET_BOTTOM' else context.region.height - (120 * scale + context.region.height * area_split_factor))
                            bpy.ops.machin3.draw_label(text="Then save the blend file, for the change to stick", coords=coords, color=yellow, alpha=1, time=5)

                return new_area

    def is_close_area_of_type(self, area, area_type='ASSET_BROWSER'):  
        '''
        compare passed in area with area_type arg
        note, that for ASSET_BROWSER you hace to check the ui_type to, as it's still just a FILE_BROWSER as of Blender 4

        we do this check to eunsure we only close an area that would would open too, so we don't want to close a time line for instance, until we support opening timelines
        '''

        if area_type == 'ASSET_BROWSER':
            return area.type == 'FILE_BROWSER' and area.ui_type == 'ASSETS'

        else:
            return area.type == area_type

    def store_asset_browser_area_settings(self, context, area, region_type, screen_name):
        '''
        store the passed in area settings on the scene
        '''

        for space in area.spaces:
            if space.type == 'FILE_BROWSER':
                if space.params:
                    libref = get_asset_library_reference(space.params)
                    import_method = get_asset_import_method(space.params)

                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['area_height'] = area.height

                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['libref'] = libref
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['import_method'] = import_method
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['catalog_id'] = space.params.catalog_id
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['display_size'] = space.params.display_size

                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['show_region_toolbar'] = space.show_region_toolbar
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['show_region_tool_props'] = space.show_region_tool_props

                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['filter_search'] = space.params.filter_search
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['filter_action'] = space.params.filter_asset_id.filter_action
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['filter_group'] = space.params.filter_asset_id.filter_group
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['filter_material'] = space.params.filter_asset_id.filter_material
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['filter_node_tree'] = space.params.filter_asset_id.filter_node_tree
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['filter_object'] = space.params.filter_asset_id.filter_object
                    context.scene.M3['asset_browser_prefs'][screen_name][region_type]['filter_world'] = space.params.filter_asset_id.filter_world

        for region in area.regions:
            if region.type == 'HEADER':
                context.scene.M3['asset_browser_prefs'][screen_name][region_type]['header_align'] = region.alignment

    def get_area_split_factor(self, context, total_height, asset_browser_height, is_bottom, debug=False):
        '''
        calculate asset split factor, from stored height in pixels divided by the total height of the current pre-split area
        NOTE, depending of the percentage and depending on the general UI scale it needs to be compensated by a few pixels
        also it needs to be capped at less than 50%, I chose 45%, or the new region will be current one
        '''

        if debug:
            print()
            print("total height:", total_height)
            print("percentage:", asset_browser_height / total_height)

        if is_bottom:
            if debug:
                print("bottom split")

            if context.preferences.system.ui_scale >= 2:
                if debug:
                    print(" big ui scale")
                    print("  ", asset_browser_height / total_height)

                if asset_browser_height / total_height <= 0.12:
                    area_split_factor = (asset_browser_height + 3) / total_height

                    if debug:
                        print("  smaller than 37.5%, compensating with", 3, "pixels")

                elif asset_browser_height / total_height <= 0.375:
                    area_split_factor = (asset_browser_height + 2) / total_height

                    if debug:
                        print("  smaller than 37.5%, compensating with", 2, "pixels")

                else:
                    area_split_factor = min(0.45, (asset_browser_height + 1)/ total_height)

                    if debug:
                        print("  bigger than 37.5% compensating with", 1, "pixels, capped at 45%")

            else:
                if debug:
                    print(" normal ui scale")

                if asset_browser_height / total_height <= 0.25:
                    area_split_factor = (asset_browser_height + 1) / total_height

                    if debug:
                        print("  smaller than 25%, compensating with", 1, "pixels")

                else:
                    area_split_factor = min(0.45, asset_browser_height / total_height)

                    if debug:
                        print("  using original height, capped at 45%")

        else:
            if context.preferences.system.ui_scale >= 2:
                if debug:
                    print(" big ui scale")

                if asset_browser_height / total_height <= 0.12:
                    area_split_factor = (asset_browser_height + 4) / total_height

                    if debug:
                        print("  smaller than 12%, compensating with", 4, "pixels")

                elif asset_browser_height / total_height <= 0.375:
                    area_split_factor = (asset_browser_height + 3) / total_height

                    if debug:
                        print("  smaller than 37.5%, compensating with", 3, "pixels")

                else:
                    area_split_factor = min(0.45, (asset_browser_height + 2)/ total_height)

                    if debug:
                        print("  bigger than 37.5% compensating with", 2, "pixels, capped at 45%")

            else:
                if debug:
                    print(" normal ui scale")

                if asset_browser_height / total_height <= 0.25:
                    area_split_factor = (asset_browser_height + 2) / total_height

                    if debug:
                        print("  smaller than 25%, compensating with", 2, "pixels")

                else:
                    area_split_factor = min(0.45, (asset_browser_height + 1)/ total_height)

                    if debug:
                        print("  bigger than 25% compensating with", 1, "pixels, capped at 45%")

        return area_split_factor

    def warp_mouse_to_border(self, context, area, region_type):
        '''
        note, unfortunately my attempts to invoke screen.area_move() failed due to wrong context, even with various overrides
        so positioning the mouse on the area border is all I can do for now
        '''
        
        if area and region_type in ['ASSET_BOTTOM', 'ASSET_TOP']:
            mouse = get_window_space_co2d(context, self.mouse_pos)
            if region_type == 'ASSET_BOTTOM':
                mouse.y = area.y + area.height

            else:
                mouse.y = area.y

            warp_mouse(self, context, mouse, region=False)


class ToggleASSETBROWSERRegion(bpy.types.Operator):
    bl_idname = "machin3.toggle_asset_browser_region"
    bl_label = "MACHIN3: Toggle Asset Browser Region"
    bl_description = "Toggle Asset Browser Region based on Mouse Position"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        if context.area:
            return context.area.type == 'FILE_BROWSER' and context.area.ui_type == 'ASSETS'

    def invoke(self, context, event):
        global supress_assetbrowser_toggle

        if supress_assetbrowser_toggle:
            supress_assetbrowser_toggle = False
            # print("supressing")

            return {'CANCELLED'}

        # init asset_browser_prefs dict
        ToggleVIEW3DRegion.initiate_asset_browser_prefs(self, context, debug=False)

        # find_areas directly above or below the active area
        areas = ToggleVIEW3DRegion.get_areas(self, context, debug=False)

        # find out of there is a 3d view above or below the asset browser
        self.view3d_above =  areas['TOP'] if areas['TOP'] and areas['TOP'].type == 'VIEW_3D' else None
        self.view3d_below =  areas['BOTTOM'] if areas['BOTTOM'] and areas['BOTTOM'].type == 'VIEW_3D' else None

        # if there is a 3dview above or below, then you can in fact close the curretn asset browsr
        can_close = bool(self.view3d_above or self.view3d_below)
        # print("can close:", can_close)

        # get mouse pos
        get_mouse_pos(self, context, event, hud=False)

        # get the region type to toggle
        region_type = self.get_region_type_from_mouse(context, can_close, debug=False)

        # then toggle it
        self.toggle_region(context, areas, region_type, debug=False)

        # context.area.tag_redraw()
        return {'FINISHED'}

    def get_region_type_from_mouse(self, context, can_close, debug=False):
        '''
        from the mouse position, get the type of the region you want to toggle
        unless it's over a non-WINDOW region already, then just toggle this one
        '''

        close_range = get_prefs().region_close_range if can_close else 50

        if context.region.type in ['WINDOW', 'HEADER']:
            area = context.area
            region_width = 0

            # in the asset browser, the TOOOLS region will the mouse to the right, but the area.width stays unaffected
            for region in area.regions:
                if region.type == 'TOOLS':
                    break

            # get mouse position expresed in percentages, and consider the TOOLS header width too, which pushes the mouse to the right, while keeping the area width unaffected
            # x_pct = (self.mouse_pos.x / area.width) * 100
            x_pct = ((self.mouse_pos.x + region.width)/ area.width) * 100

            if x_pct <= close_range:
                side = 'LEFT'

            elif x_pct >= 100 - close_range:
                side = 'RIGHT'

            else:
                side = 'CENTER'

            if debug:
                print()
                print("area width:", area.width)
                print("tools region width:", region_width)
                # print("mouse pos:", self.mouse_pos.x)
                print("mouse pos, corrected:", self.mouse_pos.x + region_width)

                print()
                print("mouse.x in %", x_pct)

                print()
                print(f"side: {side}")

            if side == 'LEFT':
                return 'TOOLS'

            elif side == 'RIGHT':
                return 'TOOL_PROPS'

            elif side == 'CENTER':
                return 'CLOSE'

        else:
            return context.region.type

    def toggle_region(self, context, areas, region_type='TOOLS', debug=False):
        '''
        toggle region based on type arg
        '''

        # if debug:
        #     print()
        #     print("toggling:", region_type)


        # CLOSE ASSET BROWSER

        if region_type == 'CLOSE':

            # store the props before closing
            area = areas['ACTIVE']
            region_type = 'ASSET_BOTTOM' if self.view3d_above else 'ASSET_TOP'
            screen_name = context.screen.name

            ToggleVIEW3DRegion.store_asset_browser_area_settings(self, context, area, region_type, screen_name)

            # then close
            bpy.ops.screen.area_close()


        # TOGGLE TOOLS (library and catalog slection) or ACTIVE ASSET info panel
        else:
            space = context.space_data

            if region_type == 'TOOLS':
                space.show_region_toolbar = not space.show_region_toolbar

            elif region_type == 'TOOL_PROPS':
                space.show_region_tool_props = not space.show_region_tool_props


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
        # print(context.area.type)
        # print(context.space_data.type)
        # print(context.region.type)
        #
        # bpy.ops.screen.area_move('INVOKE_DEFAULT')

        # del context.scene.M3['asset_browser_prefs']



        area = context.area

        for space in area.spaces:
            if space.type == area.type:
                # for d in dir(space):
                #     print("", d, getattr(space, d))

                if space.params:
                    print(space.params)

                    # for d in dir(space.params):
                    #     print(d, getattr(space.params, d))


                    # space.params.display_size = 120

                    # space.params.filter_search = 'hello'

                    filter_id = space.params.filter_asset_id

                    print(filter_id.filter_action)
                    print(filter_id.filter_group)
                    print(filter_id.filter_material)
                    print(filter_id.filter_node_tree)
                    print(filter_id.filter_object)
                    print(filter_id.filter_world)

                    filter_id.filter_material = False

                    # filter_asset_id = space.params.filter_asset_id
                    #
                    # for d in dir(filter_asset_id):
                    #     print(d, getattr(filter_asset_id, d))











        return {'FINISHED'}



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

        print()
        print("regions")
        for region in area.regions:
            print()
            print(region.type)

            for d in dir(region):
                print("", d, getattr(region, d))


        return {'FINISHED'}
