import sys
import inspect

from panda3d.core import loadPrcFileData

# We want the time of collision traversal to be added to systems that
# run them.
loadPrcFileData('', 'pstats-active-app-collisions-ctrav false')

from wecs.core import System
from wecs.panda3d import ECSShowBase


def run_game(module_name=None, simplepbr=False, simplepbr_kwargs=None, console=False, keybindings=False, debug_keys=False):
    # Application Basics
    ECSShowBase()
    base.win.setClearColor((0.5,0.7,0.9,1))
    base.disable_mouse()

    if keybindings:
        import os
        from keybindings.device_listener import add_device_listener
        from keybindings.device_listener import SinglePlayerAssigner
        add_device_listener(
            config_module=module_name,
            config_file="keybindings.toml",
            debug=True,
            assigner=SinglePlayerAssigner(),
        )
    if simplepbr is True:
        import simplepbr
        if simplepbr_kwargs is None:
            simplepbr_kwargs = {}  # i.e. dict(max_lights=1)
        simplepbr.init(**simplepbr_kwargs)

    # Handy Helpers:
    # esc: quit
    # f 9: console
    # f10: frame rate meter
    # f11: pdb, during event loop
    # f12: pstats; connects to a running server

    if console:
        from cefconsole import add_console
        from cefconsole import PythonSubconsole
        if debug_keys:
            add_console(subconsoles=[PythonSubconsole()], toggle="f9")
        else:
            add_console(subconsoles=[PythonSubconsole()])

    if debug_keys:
        base.accept('escape', sys.exit)
        base.frame_rame_meter_visible = False
        base.set_frame_rate_meter(base.frame_rame_meter_visible)
        def toggle_frame_rate_meter():
            base.frame_rame_meter_visible = not base.frame_rame_meter_visible
            base.set_frame_rate_meter(base.frame_rame_meter_visible)
        base.accept('f10', toggle_frame_rate_meter)

        def debug():
            import pdb; pdb.set_trace()
        base.accept('f11', debug)

        def pstats():
            base.pstats = True
            PStatClient.connect()
        base.accept('f12', pstats)

    # Set up the world:
    import game
    # system_types is deprecated, because badly named. Do not use.
    if hasattr(game, 'system_types'):
        add_systems(game.system_types)
    if console:
        base.console.render_console()

    # And here we go...
    base.run()


def add_systems(system_specs):
    sort, priority = 1, 1
    full_specs = {}  # (sort, priority): system_instance

    for spec in system_specs:
        # Figure out the full_specs
        if isinstance(spec, System):
            system = spec
            priority -= 1
        elif issubclass(spec, System):
            system = spec()
            priority -= 1
        else:
            sort, priority, system_spec = spec
            if isinstance(system_spec, System):
                system = system_spec
            elif issubclass(system_spec, System):
                system = system_spec()
            else:
                raise ValueError

        base.add_system(system, sort, priority=priority)
