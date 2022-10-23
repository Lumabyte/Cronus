from aiohttp import web


routes = web.RouteTableDef()


@routes.get('/')
async def get_pug_list(request):
    return web.json_response({'status': 'ok!'})


@routes.get('/pug')
async def get_pug_list(request):
    return web.json_response({'status': 'ok!'})


@routes.get('/pug/{id}')
async def get_pug(request):
    return web.json_response({'status': 'ok!'})


@routes.get('/pug/{id}/events')
async def get_pug_events(request):
    return web.json_response({'status': 'ok!'})


@routes.get('/player/{id}')
async def get_player(request):
    return web.json_response({'status': 'ok!'})


@routes.get('/player/{id}/stats')
async def get_player_statistics(request):
    return web.json_response({'status': 'ok!'})
