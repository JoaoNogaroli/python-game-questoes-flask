import pusher
def connection_pusher(evento,dicio):
    
    pusher_client = pusher.Pusher(
        app_id='1468023',
        key='3eef3f7cf3be6643b599',
        secret='3abd13233fdb05a859ce',
        cluster='sa1',
        ssl=True
        )
    pusher_client.trigger('nixquestoes', evento, dicio)
