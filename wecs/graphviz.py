from graphviz import Graph


# Examples of use from Bob the Wizard:
#
# from wecs.graphviz import system_component_dependency
# system_component_dependency(
#     world,
#     omit_systems=[
#         systems.PrintOutput,
#         systems.ReadInput,
#     ],
# )
#
# system_component_dependency(
#     world,
#     systems_groups={
#         'magic': [
#             systems.BecomeLich,
#             systems.RegenerateMana,
#             systems.ReadySpells,
#             systems.CastRejuvenationSpell,
#             systems.CastRestoreHealthSpell,
#             systems.CastLichdomSpell,
#         ],
#         'io': [
#             systems.PrintOutput,
#             systems.ReadInput,
#         ],
#         'lifecycle': [
#             systems.Aging,
#             systems.DieFromHealthLoss,
#             systems.Die,
#         ],
#     }
# )


def system_component_dependency(world, filename=None,
                                omit_systems=None, systems_groups=None):
    assert omit_systems is None or systems_groups is None
    if systems_groups is not None:
        assert filename is None
    if filename is None and systems_groups is None:
        filename = "system_component_dependencies"

    if omit_systems is None:
        omit_systems = []

    dependency_graph = world.get_system_component_dependencies()
    if systems_groups is not None:
        for filename, system_types in systems_groups.items():
            systems = [s for s in dependency_graph.keys()
                       if type(s) in system_types]
            draw_graph(filename, world, systems)
    else:
        systems = [s for s in dependency_graph.keys()
                   if type(s) not in omit_systems]
        if filename is None:
            filename = "system_component_dependencies"
        draw_graph(filename, world, systems)


def draw_graph(filename, world, systems):
    dependency_graph = world.get_system_component_dependencies()
    components = set()
    for s in dependency_graph.values():
        components.update(s)

    dot = Graph(
        comment="System Component Dependencies",
        filename=filename,
        graph_attr=dict(
            rankdir='LR',
            ranksep='5',
        ),
        node_attr=dict(
            group='A',
        ),
    )

    for system in systems:
        dot.node(repr(system))
    for component in components:
        dot.node(repr(component))
    for system in systems:
        for dependency in dependency_graph[system]:
            dot.edge(repr(system), repr(dependency))

    dot.render(format='png')
