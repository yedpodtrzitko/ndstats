IGNORE_WORLD = (
    'timelimit',
)


def log(timestamp, line, re_match, server):
    action = re_match.group(1)
    if action == 'round_start':
        server.finish_all(timestamp)
        return server.create_match(timestamp)

    if action == 'round_end':
        server.finish_all(timestamp)
        return

    if action == 'map_changed':
        map_name = re_match.group(2).strip()[1:-1]
        server.set_map_name(map_name)
        return

    if action in IGNORE_WORLD:
        return server.get_unfinished().first()
