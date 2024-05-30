-- Pull in the wezterm API
local wezterm = require 'wezterm'
local keymaps = {}

-- This will hold the configuration.
local config = wezterm.config_builder()

-- This is where you actually apply your config choices

-- Visual
config.color_scheme = 'Snazzy (base16)'
config.line_height = 1.1
config.initial_rows = 36
config.initial_cols = 120

-- Open new wezterm window at (30%, 30%) of the active screen
wezterm.on('gui-startup', function(cmd)
  local active = wezterm.gui.screens()["active"]
  local tab, pane, window = wezterm.mux.spawn_window(cmd or {
    position = { x = active["width"] * 0.3, y = active["height"] * 0.3, },
  })
end)

-- and finally, return the configuration to wezterm
return config
