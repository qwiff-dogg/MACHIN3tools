
classes = {'CORE': [('properties', [('HistoryObjectsCollection', ''),
                                    ('HistoryUnmirroredCollection', ''),
                                    ('HistoryEpochCollection', ''),
                                    ('M3SceneProperties', ''),
                                    ('M3ObjectProperties', '')]),
                    ('preferences', [('MACHIN3toolsPreferences', '')]),
                    ('ui.operators.call_pie', [('CallMACHIN3toolsPie', 'call_machin3tools_pie')]),
                    ('ui.operators.draw', [('DrawLabel', 'draw_label'),
                                           ('DrawLabels', 'draw_labels')]),
                    ('ui.panels', [('PanelMACHIN3tools', 'machin3_tools')]),
                    ('ui.menus', [('MenuMACHIN3toolsObjectContextMenu', 'machin3tools_object_context_menu'),
                                  ('MenuMACHIN3toolsMeshContextMenu', 'machin3tools_mesh_context_menu'),
                                  ('MenuGroupObjectContextMenu', 'group_object_context_menu')]),
                    ('operators.quadsphere', [('QuadSphere', 'quadsphere')])],

           'SMART_VERT': [('operators.smart_vert', [('SmartVert', 'smart_vert')])],
           'SMART_EDGE': [('operators.smart_edge', [('SmartEdge', 'smart_edge')])],
           'SMART_FACE': [('operators.smart_face', [('SmartFace', 'smart_face')])],
           'CLEAN_UP': [('operators.clean_up', [('CleanUp', 'clean_up')])],
           'CLIPPING_TOGGLE': [('operators.clipping_toggle', [('ClippingToggle', 'clipping_toggle')])],
           'FOCUS': [('operators.focus', [('Focus', 'focus')])],
           'MIRROR': [('operators.mirror', [('Mirror', 'mirror'),
                                            ('Unmirror', 'unmirror')])],
           'ALIGN': [('operators.align', [('Align', 'align'),
                                          ('AlignRelative', 'align_relative')])],
           'APPLY': [('operators.apply', [('Apply', 'apply_transformations')])],
           'SELECT': [('operators.select', [('SelectCenterObjects', 'select_center_objects'),
                                            ('SelectWireObjects', 'select_wire_objects'),
                                            ('SelectHierarchy', 'select_hierarchy')])],
           'MESH_CUT': [('operators.mesh_cut', [('MeshCut', 'mesh_cut')])],
           'SURFACE_SLIDE': [('operators.surface_slide', [('SurfaceSlide', 'surface_slide'),
                                                          ('FinishSurfaceSlide', 'finish_surface_slide')])],
           'ASSETBROWSER': [('operators.assetbrowser', [('AssembleInstanceCollection', 'assemble_instance_collection'),
                                                        ('CreateAssemblyAsset', 'create_assembly_asset')])],
                                                        # ('CollectAssets', 'collect_assets')])],
           'FILEBROWSER': [('operators.filebrowser', [('Open', 'filebrowser_open'),
                                                      ('Toggle', 'filebrowser_toggle'),
                                                      ('CycleThumbs', 'filebrowser_cycle_thumbnail_size')])],
           'SMART_DRIVE': [('operators.smart_drive', [('SmartDrive', 'smart_drive'),
                                                      ('SwitchValues', 'switch_driver_values'),
                                                      ('SetValue', 'set_driver_value')])],
           'UNITY': [('operators.unity', [('PrepareExport', 'prepare_unity_export'),
                                          ('RestoreExport', 'restore_unity_export')])],
           'MATERIAL_PICKER': [('operators.material_picker', [('MaterialPicker', 'material_picker')])],
           'GROUP': [('operators.group', [('Group', 'group'),
                                          ('UnGroup', 'ungroup'),
                                          ('Groupify', 'groupify'),
                                          ('Add', 'add_to_group'),
                                          ('Remove', 'remove_from_group'),
                                          ('Select', 'select_group'),
                                          ('Duplicate', 'duplicate_group'),
                                          ('ToggleGroupMode', 'toggle_outliner_group_mode'),
                                          ('ToggleChildren', 'toggle_outliner_children'),
                                          ('ExpandOutliner', 'expand_outliner'),
                                          ('CollapseOutliner', 'collapse_outliner')])],

           'REGION': [('operators.region', [('ToggleRegion', 'toggle_region')])],
                                            # ('AreaDumper', 'area_dumper')])],
           'SMOOTH': [('operators.smooth', [('ToggleSmooth', 'toggle_smooth')])],
           'THREAD': [('operators.thread', [('Thread', 'add_thread')])],
           'EXTRUDE': [('operators.extrude', [('CursorSpin', 'cursor_spin'),
                                              ('PunchItALittle', 'punch_it_a_little')])],
           'RENDER': [('operators.render', [('Render', 'render'),
                                            ('DuplicateNodes', 'duplicate_nodes')])],

           'CUSTOMIZE': [('operators.customize', [('Customize', 'customize'),
                                                  ('RestoreKeymaps', 'restore_keymaps')])],

           'MODES_PIE': [('ui.pies', [('PieModes', 'modes_pie')]),
                         ('ui.operators.mode', [('EditMode', 'edit_mode'),
                                                ('MeshMode', 'mesh_mode'),
                                                ('ImageMode', 'image_mode'),
                                                ('UVMode', 'uv_mode'),
                                                ('SurfaceDrawMode', 'surface_draw_mode')]),
                         ('ui.operators.grease_pencil', [('ShrinkwrapGreasePencil', 'shrinkwrap_grease_pencil')]),

                         ('ui.operators.open_blend', [('OpenLibraryBlend', 'open_library_blend')])],
           'SAVE_PIE': [('ui.pies', [('PieSave', 'save_pie')]),
                        ('ui.operators.save', [('New', 'new'),
                                               ('Save', 'save'),
                                               ('SaveAs', 'save_as'),
                                               ('SaveIncremental', 'save_incremental'),
                                               ('SaveVersionedStartupFile', 'save_versioned_startup_file'),
                                               ('LoadMostRecent', 'load_most_recent'),
                                               ('LoadPrevious', 'load_previous'),
                                               ('LoadNext', 'load_next')]),
                        ('ui.operators.save', [('OpenTemp', 'open_temp_dir'),
                                               ('Purge', 'purge_orphans'),
                                               ('Clean', 'clean_out_blend_file'),
                                               ('ReloadLinkedLibraries', 'reload_linked_libraries'),
                                               ('ScreenCast', 'screen_cast')])],
           'SHADING_PIE': [('ui.pies', [('PieShading', 'shading_pie')]),
                           ('ui.operators.shading', [('SwitchShading', 'switch_shading'),
                                                     ('ToggleOutline', 'toggle_outline'),
                                                     ('ToggleCavity', 'toggle_cavity'),
                                                     ('ToggleCurvature', 'toggle_curvature'),
                                                     ('MatcapSwitch', 'matcap_switch'),
                                                     ('RotateStudioLight', 'rotate_studiolight')]),
                           ('ui.operators.overlay', [('ToggleGrid', 'toggle_grid'),
                                                     ('ToggleWireframe', 'toggle_wireframe')]),
                           ('ui.operators.mesh', [('Shade', 'shade'),
                                                  ('ToggleAutoSmooth', 'toggle_auto_smooth')]),
                           ('ui.operators.colorize', [('ColorizeMaterials', 'colorize_materials'),
                                                      ('ColorizeObjectsFromActive', 'colorize_objects_from_active'),
                                                      ('ColorizeObjectsFromCollections', 'colorize_objects_from_collections'),
                                                      ('ColorizeObjectsFromGroups', 'colorize_objects_from_groups'),
                                                      ('ColorizeObjectsFromMaterials', 'colorize_objects_from_materials')])],
           'VIEWS_PIE': [('ui.pies', [('PieViewport', 'viewport_pie')]),
                         ('ui.operators.viewport', [('ViewAxis', 'view_axis'),
                                                    ('MakeCamActive', 'make_cam_active'),
                                                    ('SmartViewCam', 'smart_view_cam'),
                                                    ('NextCam', 'next_cam'),
                                                    ('ToggleCamPerspOrtho', 'toggle_cam_persportho'),
                                                    ('ToggleViewPerspOrtho', 'toggle_view_persportho'),
                                                    ('ToggleOrbitMethod', 'toggle_orbit_method'),
                                                    ('ToggleOrbitSelection', 'toggle_orbit_selection'),
                                                    ('ResetViewport', 'reset_viewport')])],
           'ALIGN_PIE': [('ui.pies', [('PieAlign', 'align_pie'),
                                      ('PieUVAlign', 'uv_align_pie')]),
                         ('ui.operators.align', [('AlignEditMesh', 'align_editmesh'),
                                                 ('CenterEditMesh', 'center_editmesh'),
                                                 ('AlignObjectToEdge', 'align_object_to_edge'),
                                                 ('AlignObjectToVert', 'align_object_to_vert'),
                                                 ('Straighten', 'straighten')]),
                         ('ui.operators.uv', [('AlignUV', 'align_uv')])],
           'CURSOR_PIE': [('ui.pies', [('PieCursor', 'cursor_pie')]),
                          ('ui.operators.cursor', [('CursorToOrigin', 'cursor_to_origin'),
                                                   ('CursorToSelected', 'cursor_to_selected'),
                                                   ('SelectedToCursor', 'selected_to_cursor')]),
                          ('ui.operators.origin', [('OriginToActive', 'origin_to_active'),
                                                   ('OriginToCursor', 'origin_to_cursor'),
                                                   ('OriginToBottomBounds', 'origin_to_bottom_bounds')])],
           'TRANSFORM_PIE': [('ui.pies', [('PieTransform', 'transform_pie')]),
                             ('ui.operators.transform_preset', [('SetTransformPreset', 'set_transform_preset')])],
           'SNAPPING_PIE': [('ui.pies', [('PieSnapping', 'snapping_pie')]),
                            ('ui.operators.snapping_preset', [('SetSnappingPreset', 'set_snapping_preset')])],
           'COLLECTIONS_PIE': [('ui.pies', [('PieCollections', 'collections_pie')]),
                               ('ui.operators.collection', [('CreateCollection', 'create_collection'),
                                                            ('RemoveFromCollection', 'remove_from_collection'),
                                                            ('Purge', 'purge_collections'),
                                                            ('Select', 'select_collection')])],
           'WORKSPACE_PIE': [('ui.pies', [('PieWorkspace', 'workspace_pie')]),
                             ('ui.operators.workspace', [('SwitchWorkspace', 'switch_workspace'),
                                                         ('GetIconNameHelp', 'get_icon_name_help')])],
           'TOOLS_PIE': [('ui.pies', [('PieTools', 'tools_pie')]),
                         ('ui.operators.tool', [('SetToolByName', 'set_tool_by_name'),
                                                ('SetBCPreset', 'set_boxcutter_preset')])],
           }


keys = {'SMART_VERT': [{'label': 'Merge Last', 'keymap': 'Mesh', 'idname': 'machin3.smart_vert', 'type': 'ONE', 'value': 'PRESS', 'properties': [('mode', 'MERGE'), ('mergetype', 'LAST'), ('slideoverride', False)]},
                       {'label': 'Merge Center', 'keymap': 'Mesh', 'idname': 'machin3.smart_vert', 'type': 'ONE', 'value': 'PRESS', 'shift': True, 'properties': [('mode', 'MERGE'), ('mergetype', 'CENTER'), ('slideoverride', False)]},
                       {'label': 'Merge Paths', 'keymap': 'Mesh', 'idname': 'machin3.smart_vert', 'type': 'ONE', 'value': 'PRESS', 'alt': True, 'properties': [('mode', 'MERGE'), ('mergetype', 'PATHS'), ('slideoverride', False)]},
                       {'label': 'Connect Paths', 'keymap': 'Mesh', 'idname': 'machin3.smart_vert', 'type': 'ONE', 'value': 'PRESS', 'alt': True, 'ctrl': True, 'properties': [('mode', 'CONNECT'), ('slideoverride', False)]},
                       {'label': 'Slide Extend', 'keymap': 'Mesh', 'idname': 'machin3.smart_vert', 'type': 'ONE', 'value': 'PRESS', 'shift': True, 'alt': True, 'properties': [('slideoverride', True)]}],
        'SMART_EDGE': [{'label': 'Smart Edge', 'keymap': 'Mesh', 'idname': 'machin3.smart_edge', 'type': 'TWO', 'value': 'PRESS', 'properties': [('sharp', False), ('offset', False)]},
                       {'label': 'Toggle Sharp/Weight', 'keymap': 'Mesh', 'idname': 'machin3.smart_edge', 'type': 'TWO', 'shift': True, 'value': 'PRESS', 'properties': [('sharp', True), ('offset', False)]},
                       {'label': 'Offset Edges', 'keymap': 'Mesh', 'idname': 'machin3.smart_edge', 'type': 'TWO', 'ctrl': True, 'value': 'PRESS', 'properties': [('sharp', False), ('offset', True)]}],
        'SMART_FACE': [{'keymap': 'Mesh', 'idname': 'machin3.smart_face', 'type': 'FOUR', 'value': 'PRESS'}],
        'CLEAN_UP': [{'keymap': 'Mesh', 'idname': 'machin3.clean_up', 'type': 'THREE', 'value': 'PRESS'}],
        'CLIPPING_TOGGLE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'machin3.clipping_toggle', 'type': 'BUTTON5MOUSE', 'value': 'PRESS'}],
        'FOCUS': [{'label': 'View Selected', 'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'machin3.focus', 'type': 'F', 'value': 'PRESS', 'properties': [('method', 'VIEW_SELECTED')]},
                  {'label': 'Local View', 'keymap': 'Object Mode', 'idname': 'machin3.focus', 'type': 'F', 'value': 'PRESS', 'ctrl': True, 'properties': [('method', 'LOCAL_VIEW'), ('invert', False)]},
                  {'label': 'Local View (Inverted)', 'keymap': 'Object Mode', 'idname': 'machin3.focus', 'type': 'F', 'value': 'PRESS', 'ctrl': True, 'alt': True, 'properties': [('method', 'LOCAL_VIEW'), ('invert', True)]}],

        'MIRROR': [{'label': 'Flick Mirror', 'keymap': 'Object Mode', 'idname': 'machin3.mirror', 'type': 'X', 'value': 'PRESS', 'alt': True, 'shift': True, 'properties': [('flick', True), ('remove', False)]}],

        # 'MIRROR': [{'label': 'X Axis', 'keymap': 'Object Mode', 'idname': 'machin3.mirror', 'type': 'X', 'value': 'PRESS', 'alt': True, 'shift': True, 'properties': [('use_x', True), ('use_y', False), ('use_z', False)]},
                   # {'label': 'Y Axis', 'keymap': 'Object Mode', 'idname': 'machin3.mirror', 'type': 'Y', 'value': 'PRESS', 'alt': True, 'shift': True, 'properties': [('use_x', False), ('use_y', True), ('use_z', False)]},
                   # {'label': 'Z Axis', 'keymap': 'Object Mode', 'idname': 'machin3.mirror', 'type': 'Z', 'value': 'PRESS', 'alt': True, 'shift': True, 'properties': [('use_x', False), ('use_y', False), ('use_z', True)]}],

        'ALIGN': [{'label': 'Object Mode', 'keymap': 'Object Mode', 'idname': 'machin3.align', 'type': 'A', 'value': 'PRESS', 'alt': True},
                  {'label': 'Pose Mode', 'keymap': 'Pose', 'idname': 'machin3.align', 'type': 'A', 'value': 'PRESS', 'alt': True}],
        'FILEBROWSER': [{'label': 'Open Filebrowser', 'keymap': 'File Browser', 'space_type': 'FILE_BROWSER', 'idname': 'machin3.filebrowser_open', 'type': 'O', 'value': 'PRESS', 'properties': [('blend_file', False)]},
                        {'label': 'Open .blend File', 'keymap': 'File Browser', 'space_type': 'FILE_BROWSER', 'idname': 'machin3.filebrowser_open', 'type': 'O', 'value': 'PRESS', 'alt': True, 'properties': [('blend_file', True)]},
                        {'label': 'Toggle Sorting', 'keymap': 'File Browser', 'space_type': 'FILE_BROWSER', 'idname': 'machin3.filebrowser_toggle', 'type': 'ONE', 'value': 'PRESS', 'properties': [('type', 'SORT')]},
                        {'label': 'Toggle Display', 'keymap': 'File Browser', 'space_type': 'FILE_BROWSER', 'idname': 'machin3.filebrowser_toggle', 'type': 'TWO', 'value': 'PRESS', 'properties': [('type', 'DISPLAY_TYPE')]},
                        {'label': 'Cycle Thumbs Forwards', 'keymap': 'File Browser', 'space_type': 'FILE_BROWSER', 'idname': 'machin3.filebrowser_cycle_thumbnail_size', 'type': 'THREE', 'value': 'PRESS', 'properties': [('reverse', False)]},
                        {'label': 'Cycle Thumbs Backwards', 'keymap': 'File Browser', 'space_type': 'FILE_BROWSER', 'idname': 'machin3.filebrowser_cycle_thumbnail_size', 'type': 'THREE', 'value': 'PRESS', 'shift': True, 'properties': [('reverse', True)]},
                        {'label': 'Toggle Hidden', 'keymap': 'File Browser', 'space_type': 'FILE_BROWSER', 'idname': 'machin3.filebrowser_toggle', 'type': 'FOUR', 'value': 'PRESS', 'properties': [('type', 'HIDDEN')]}],
        'GROUP': [{'label': 'Create Group', 'keymap': 'Object Mode', 'idname': 'machin3.group', 'type': 'G', 'value': 'PRESS', 'ctrl': True},
                  {"label": "Select Group", "keymap": "Object Mode", "idname": "machin3.select_group", "type": "LEFTMOUSE", "value": "DOUBLE_CLICK", 'shift': True},
                  {'label': 'Toggle Group Mode', 'keymap': 'Outliner', 'space_type': 'OUTLINER', 'idname': 'machin3.toggle_outliner_group_mode', 'type': 'ONE', 'value': 'PRESS'},
                  {'label': 'Expand Outliner', 'keymap': 'Outliner', 'space_type': 'OUTLINER', 'idname': 'machin3.expand_outliner', 'type': 'TWO', 'value': 'PRESS'},
                  {'label': 'Collapse Outliner', 'keymap': 'Outliner', 'space_type': 'OUTLINER', 'idname': 'machin3.collapse_outliner', 'type': 'THREE', 'value': 'PRESS'},
                  {'label': 'Toggle Children', 'keymap': 'Outliner', 'space_type': 'OUTLINER', 'idname': 'machin3.toggle_outliner_children', 'type': 'FOUR', 'value': 'PRESS'}],
        'SELECT': [{'label': 'Select Children', 'keymap': 'Object Mode', 'idname': 'machin3.select_hierarchy', 'type': 'DOWN_ARROW', 'value': 'PRESS', 'properties': [('include_parent', False), ('unhide', False)]},
                   {'label': 'Select Parent + Children', 'keymap': 'Object Mode', 'idname': 'machin3.select_hierarchy', 'type': 'DOWN_ARROW', 'value': 'PRESS', 'shift': True, 'properties': [('include_parent', True), ('unhide', False)]},
                   {'label': 'Select Children + Unhide', 'keymap': 'Object Mode', 'idname': 'machin3.select_hierarchy', 'type': 'DOWN_ARROW', 'value': 'PRESS', 'ctrl': True, 'properties': [('include_parent', False), ('unhide', True)]},
                   {'label': 'Select Parent + Children + Unhide', 'keymap': 'Object Mode', 'idname': 'machin3.select_hierarchy', 'type': 'DOWN_ARROW', 'value': 'PRESS', 'shift': True, 'ctrl': True, 'properties': [('include_parent', True), ('unhide', True)]}],
        'REGION': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'machin3.toggle_region', 'type': 'T', 'value': 'PRESS'}],
        'SMOOTH': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'machin3.toggle_smooth', 'type': 'TAB', 'value': 'PRESS', 'alt': True, 'info': ['Remap this is if Alt + Tab switches Windows for you']}],
        'RENDER': [{'keymap': 'Node Editor', 'space_type': 'NODE_EDITOR', 'idname': 'machin3.duplicate_nodes', 'type': 'D', 'value': 'PRESS', 'shift': True}],

        'MODES_PIE': [{'label': '3D View', 'keymap': 'Object Non-modal', 'idname': 'wm.call_menu_pie', 'type': 'TAB', 'value': 'PRESS', 'properties': [('name', 'MACHIN3_MT_modes_pie')]},
                      {'label': 'Image Editor', 'keymap': 'Image', 'space_type': 'IMAGE_EDITOR', 'idname': 'wm.call_menu_pie', 'type': 'TAB', 'value': 'PRESS', 'properties': [('name', 'MACHIN3_MT_modes_pie')]}],
        'SAVE_PIE': [{'keymap': 'Window', 'idname': 'wm.call_menu_pie', 'type': 'S', 'value': 'PRESS', 'ctrl': True, 'properties': [('name', 'MACHIN3_MT_save_pie')]},
                     {'keymap': 'Window', 'idname': 'machin3.save_versioned_startup_file', 'type': 'U', 'value': 'PRESS', 'ctrl': True, 'active': False}],
        # 'SHADING_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'wm.call_menu_pie', 'type': 'PAGE_UP', 'value': 'PRESS', 'properties': [('name', 'MACHIN3_MT_shading_pie')]}],
        'SHADING_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'machin3.call_machin3tools_pie', 'type': 'PAGE_UP', 'value': 'PRESS', 'properties': [('idname', 'shading_pie')]}],
        'VIEWS_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'wm.call_menu_pie', 'type': 'PAGE_DOWN', 'value': 'PRESS', 'properties': [('name', 'MACHIN3_MT_viewport_pie')]}],
        'ALIGN_PIE': [{'label': 'Edit Mode', 'keymap': 'Mesh', 'idname': 'wm.call_menu_pie', 'type': 'A', 'value': 'PRESS', 'alt': True, 'properties': [('name', 'MACHIN3_MT_align_pie')]},
                      {'label': 'UV Editor', 'keymap': 'UV Editor', 'idname': 'wm.call_menu_pie', 'type': 'A', 'value': 'PRESS', 'alt': True, 'properties': [('name', 'MACHIN3_MT_uv_align_pie')]}],
        'CURSOR_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'wm.call_menu_pie', 'type': 'S', 'value': 'PRESS', 'shift': True, 'properties': [('name', 'MACHIN3_MT_cursor_pie')]}],
        'TRANSFORM_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'wm.call_menu_pie', 'type': 'BUTTON4MOUSE', 'value': 'PRESS', 'shift': True, 'properties': [('name', 'MACHIN3_MT_transform_pie')]}],
        'SNAPPING_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'wm.call_menu_pie', 'type': 'BUTTON5MOUSE', 'value': 'PRESS', 'shift': True, 'properties': [('name', 'MACHIN3_MT_snapping_pie')]}],
        'COLLECTIONS_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'wm.call_menu_pie', 'type': 'C', 'value': 'PRESS', 'shift': True, 'properties': [('name', 'MACHIN3_MT_collections_pie')]}],
        'WORKSPACE_PIE': [{'keymap': 'Window', 'idname': 'wm.call_menu_pie', 'type': 'PAUSE', 'value': 'PRESS', 'properties': [('name', 'MACHIN3_MT_workspace_pie')]}],
        # 'TOOLS_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'wm.call_menu_pie', 'type': 'Q', 'value': 'PRESS', 'properties': [('name', 'MACHIN3_MT_tools_pie')]}],
        'TOOLS_PIE': [{'keymap': '3D View Generic', 'space_type': 'VIEW_3D', 'idname': 'machin3.call_machin3tools_pie', 'type': 'Q', 'value': 'PRESS', 'properties': [('idname', 'tools_pie')]}],
        }
