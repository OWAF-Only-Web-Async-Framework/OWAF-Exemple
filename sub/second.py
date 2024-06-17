from OWAF import Shard

class Index(Shard):
    async def index(self) -> str:
        '''explanation
        Say hello to the world
        :test: g=1
        :route: GET: /
        :end test:'''
        return 'wow'
