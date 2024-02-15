import obspython as obs

# ------------------------------------------------------------
# --------------- Code to Update the Source ------------------
# ------------------------------------------------------------

def update_source():
	global velocity
	global source_name
	global x_dir
	global y_dir

	source = obs.obs_get_source_by_name(source_name)
	scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
	scene_item = obs.obs_scene_find_source(scene, source_name)

	# If a target source is found, update it on screen
	if scene_item:
		# Get the current location of the source
		location = obs.vec2()
		obs.obs_sceneitem_get_pos(scene_item, location)
		
		# Get the scale of the source
		scale = obs.vec2()
		obs.obs_sceneitem_get_scale(scene_item, scale)

		# Get the height and width of the source
		height = obs.obs_source_get_height(source)
		width = obs.obs_source_get_width(source)
		
		# Move the source and multiply by modifier
		location.x += velocity * x_dir
		location.y += velocity * y_dir
		
		# Reverse X if needed and makes sure no overlap occurs
		if location.x + (width * scale.x) >= 1920:
			x_dir = -1
			location.x = 1920 - (width * scale.x)
		elif location.x <= 0:
			x_dir = 1
			location.x = 0

		# Reverse Y if needed and makes sure no overlap occurs
		if location.y + (height * scale.y) >= 1080:
			y_dir = -1
			location.y = 1080 - (height * scale.y)
		elif location.y <= 0:
			y_dir = 1
			location.y = 0
			
		# Update the position on screen
		obs.obs_sceneitem_set_pos(scene_item, location)

	# Release the scene and source from memory
	obs.obs_scene_release(scene)
	obs.obs_source_release(source)
	# obs.obs_sceneitem_release(scene_item) # This causes a crash and I don't know why

# ------------------------------------------------------------
# ------------- Code to Initialize the Script ----------------
# ------------------------------------------------------------

# Creates the description for the script
def script_description():
	return "Moves a source around the screen in the style of the old DVD logos when left idle for too long. The update interval can be increased to help improve performance while making it look a little more choppy. The velocity can be changed to either slow the animation or speed it up.\n\nBy Chase Thompson"

# Function is called when a property is changed
def script_update(settings):
	global interval
	global velocity
	global source_name

	# Update information required to run the script
	interval = obs.obs_data_get_int(settings, "interval")
	velocity = obs.obs_data_get_int(settings, "velocity")
	source_name = obs.obs_data_get_string(settings, "source")
	enabled = obs.obs_data_get_bool(settings, "enabled")

	# Set up the update callback if a source is provided
	obs.timer_remove(update_source)
	if source_name != "" and enabled:
		obs.timer_add(update_source, interval)

# Sets up the default values of different properties
def script_defaults(settings):
	global x_dir
	global y_dir
	
	# Set up non-property defaults
	x_dir = 1
	y_dir = 1
	
	# Set up property defaults
	obs.obs_data_set_default_int(settings, "interval", 25)
	obs.obs_data_set_default_int(settings, "velocity", 5)
	obs.obs_data_set_default_bool(settings, "enabled", False)

# Initializes script properties and creates the menu
def script_properties():
	# Create Properties (this comment is just here for symmetry)
	props = obs.obs_properties_create()

	# Update Interval and Velocity input
	obs.obs_properties_add_int(props, "interval", "Update Interval (ms)", 25, 10000, 5)
	obs.obs_properties_add_int(props, "velocity", "Velocity", 1, 100, 1)

	# Get list of all sources and add them to the list
	p = obs.obs_properties_add_list(props, "source", "Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
			# Filter out audio sources
			source_id = obs.obs_source_get_unversioned_id(source)
			if source_id == "wasapi_input_capture" or source_id == "wasapi_output_capture":
				continue

			# Add non-audio sources to the list
			name = obs.obs_source_get_name(source)
			obs.obs_property_list_add_string(p, name, name)

		obs.source_list_release(sources)

	# Enable/Disable Toggle
	obs.obs_properties_add_bool(props, "enabled", "Enable")
	return props
