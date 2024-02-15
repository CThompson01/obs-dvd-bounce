-- Init globals here
obs = obslua
velocity = 5
interval = 25
source_name = ""
x_dir = 1
y_dir = 1

-------------------------------------------
-------- Code to Update the Source --------
-------------------------------------------

function update_source()
	local source = obs.obs_get_source_by_name(source_name)
	local scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
	local scene_item = obs.obs_scene_find_source(scene, source_name)

	-- If a target source is found, update it on screen
	if scene_item ~= nil then
		-- Get the current location of the source
		local location = obs.vec2()
		obs.obs_sceneitem_get_pos(scene_item, location)

		-- Get the scale of the source
		local scale = obs.vec2()
		obs.obs_sceneitem_get_scale(scene_item, scale)

		-- Get the height and width of the source
		local height = obs.obs_source_get_height(source)
		local width = obs.obs_source_get_width(source)

		-- Move the source and multiply by modifier
		location.x = location.x + (velocity * x_dir)
		location.y = location.y + (velocity * y_dir)
		
		-- Reverse X if needed and makes sure no overlap occurs
		if location.x + (width * scale.x) >= 1920 then
			x_dir = -1
			location.x = 1920 - (width * scale.x)
		elseif location.x <= 0 then
			x_dir = 1
			location.x = 0
		end

		-- Reverse Y if needed and makes sure no overlap occurs
		if location.y + (height * scale.y) >= 1080 then
			y_dir = -1
			location.y = 1080 - (height * scale.y)
		elseif location.y <= 0 then
			y_dir = 1
			location.y = 0
		end
			
		-- Update the position on screen
		obs.obs_sceneitem_set_pos(scene_item, location)
	end

	-- Release the scene and source from memory
	obs.obs_scene_release(scene)
	obs.obs_source_release(source)
	-- obs.obs_sceneitem_release(scene_item) -- This causes a crash and I don't know why
end

-------------------------------------------
------ Code to Initialize the Script ------
-------------------------------------------

function script_description()
	return "Moves a source around the screen in the style of the old DVD logos when left idle for too long. The update interval can be increased to help improve performance while making it look a little more choppy. The velocity can be changed to either slow the animation or speed it up.\n\nBy Chase Thompson"
end

function script_update(settings)
	-- Update information required to run the script
	interval = obs.obs_data_get_int(settings, "interval")
	velocity = obs.obs_data_get_int(settings, "velocity")
	source_name = obs.obs_data_get_string(settings, "source")
	enabled = obs.obs_data_get_bool(settings, "enabled")

	-- Set up the update callback if a source is provided
	obs.timer_remove(update_source)
	if source_name ~= ""  and enabled then
		obs.timer_add(update_source, interval)
	end
end

function script_defaults(settings)
	-- Set up non-property defaults
	x_dir = 1
	y_dir = 1

	-- Set up property defaults
	obs.obs_data_set_default_int(settings, "interval", 25)
	obs.obs_data_set_default_int(settings, "velocity", 5)
	obs.obs_data_set_default_bool(settings, "enabled", false)
end

function script_properties()
	-- Create Properties (this comment is just here for symmetry)
	local props = obs.obs_properties_create()

	-- Update Interval and Velocity input
	obs.obs_properties_add_int(props, "interval", "Update Interval (ms)", 25, 10000, 5)
	obs.obs_properties_add_int(props, "velocity", "Velocity", 1, 100, 1)

	-- Get list of all sources and add them to the list
	local p = obs.obs_properties_add_list(props, "source", "Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	local sources = obs.obs_enum_sources()
	if sources ~= nil then
		for _, source in ipairs(sources) do
			-- Filter out audio sources
			source_id = obs.obs_source_get_unversioned_id(source)
			if source_id ~= "wasapi_input_capture" and source_id ~= "wasapi_output_capture" then
				local name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)
			end
		end
		obs.source_list_release(sources)
	end

	-- Enable/Disable Toggle
	obs.obs_properties_add_bool(props, "enabled", "Enable")
	return props
end