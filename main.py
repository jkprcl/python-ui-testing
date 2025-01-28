import dearpygui.dearpygui as dpg

dpg.create_context()

# set up the default font
default_font_path = "assets/fonts/JetBrainsMono-Bold.ttf"
default_font_size = 20
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font(default_font_path, default_font_size)
dpg.bind_font(default_font)

with dpg.window(tag="Test Window"):
    dpg.add_text("Hello, world!")
    dpg.add_loading_indicator(style=1)

dpg.create_viewport(
    title="Test Notification",
    width=600,
    height=200,
    always_on_top=True,
    resizable=False,
    disable_close=True,
    decorated=False,
    vsync=True,
)
dpg.set_primary_window(window="Test Window", value=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
