"""
Run this benchmark with pytest (requires the package pytest-benchmark):
pytest tests/integration/benchmark.py
"""

import bz2

from betfair_parser.spec.streaming import MCM, STREAM_RESPONSE, stream_decode
from tests.resources import RESOURCES_DIR


def test_performance(benchmark):
    path = RESOURCES_DIR / "data/27312315.bz2"
    lines = bz2.open(path).readlines()

    def decode_all(lst: list[bytes]) -> list[STREAM_RESPONSE]:
        return [stream_decode(line) for line in lst]

    result = benchmark.pedantic(decode_all, args=(lines,))
    assert len(result) == 50854
    for msg in result:
        assert isinstance(msg, STREAM_RESPONSE)  # type: ignore


def test_market_update_performance(benchmark):
    line = b'{"op":"mcm","clk":"640811137","pt":1430339874907,"mc":[{"id":"1.116499285","rc":[{"atb":[[450,3.99]],"id":7610786}],"con":true,"img":false,"tv":398222.04}]}'  # noqa
    result: MCM = benchmark.pedantic(stream_decode, args=(line,), rounds=10, iterations=10)
    assert isinstance(result, MCM)


def test_market_definition_performance(benchmark):
    line = b'{"op":"mcm","clk":"645222418","pt":1430417651653,"mc":[{"id":"1.117817971","marketDefinition":{"bspMarket":false,"turnInPlayEnabled":false,"persistenceEnabled":true,"marketBaseRate":5.0,"eventId":"27312315","eventTypeId":"8","numberOfWinners":3,"bettingType":"ODDS","marketType":"UNDIFFERENTIATED","marketTime":"2015-03-14T06:00:00.000Z","suspendTime":"2015-03-14T06:00:00.000Z","bspReconciled":false,"complete":false,"inPlay":false,"crossMatching":false,"runnersVoidable":false,"numberOfActiveRunners":18,"betDelay":0,"status":"OPEN","runners":[{"status":"ACTIVE","sortPriority":1,"id":7812754,"name":"Lewis Hamilton"},{"status":"ACTIVE","sortPriority":2,"id":7812755,"name":"Nico Rosberg"},{"status":"ACTIVE","sortPriority":3,"id":7812761,"name":"Daniel Ricciardo"},{"status":"ACTIVE","sortPriority":4,"id":7812752,"name":"Sebastian Vettel"},{"status":"ACTIVE","sortPriority":5,"id":6533198,"name":"Valtteri Bottas"},{"status":"ACTIVE","sortPriority":6,"id":7610784,"name":"Fernando Alonso"},{"status":"ACTIVE","sortPriority":7,"id":7812753,"name":"Kimi Raikkonen"},{"status":"ACTIVE","sortPriority":8,"id":7812756,"name":"Felipe Massa"},{"status":"ACTIVE","sortPriority":9,"id":7610786,"name":"Jenson Button"},{"status":"ACTIVE","sortPriority":10,"id":8064931,"name":"Daniil Kvyat"},{"status":"ACTIVE","sortPriority":11,"id":7812757,"name":"Romain Grosjean"},{"status":"ACTIVE","sortPriority":12,"id":7812763,"name":"Pastor Maldonado"},{"status":"ACTIVE","sortPriority":13,"id":9023044,"name":"Max Verstappen"},{"status":"ACTIVE","sortPriority":14,"id":7812758,"name":"Nico Hulkenberg"},{"status":"ACTIVE","sortPriority":15,"id":7812760,"name":"Sergio Perez"},{"status":"ACTIVE","sortPriority":16,"id":6203941,"name":"Marcus Ericsson"},{"status":"ACTIVE","sortPriority":17,"id":6203939,"name":"Felipe Nasr"},{"status":"ACTIVE","sortPriority":18,"id":9039059,"name":"Carlos Sainz Jr"}],"regulators":["MR_INT"],"discountAllowed":true,"timezone":"Europe/London","openDate":"2015-03-14T06:00:00.000Z","version":938098268,"name":"Drivers Championship 2015 - Top 3","eventName":"Formula 1 2015"},"rc":[{"atb":[[1.5,100],[15,2],[6,36.52],[3.05,36.52],[2,53.76],[4.5,10],[2.5,25],[6.2,51.13]],"id":6533198},{"atl":[[29,18.26]],"id":6533198},{"trd":[[10.5,78.57],[6.2,18.99]],"ltp":10.5,"tv":97.55,"id":6533198},{"atb":[[3,29.22],[2.6,45],[3.05,2.57],[2,73.76],[2.5,25]],"id":7812753},{"atl":[[32,5],[12.5,10],[9.8,14.61],[12,2],[21,10],[8,10]],"id":7812753},{"trd":[[3,50.29],[6,41.63],[4.2,5.2],[4.1,37.44]],"ltp":3.0,"tv":134.56,"id":7812753},{"atb":[[6,15],[10,18.26],[4,25]],"id":7610786},{"atl":[[900,3]],"id":7610786},{"atb":[[1.12,1.03],[1.1,109.58],[1.11,26.72],[1.01,7.73],[1.15,5],[1.03,2.57],[1.02,2.57]],"id":7812752},{"atl":[[1.7,50],[1.4,5],[1.99,29.22],[10.5,10],[1.54,46.75],[1.55,300],[4.1,10],[6.2,10]],"id":7812752},{"trd":[[1.11,1.72],[1.3,150.95],[1.5,199.86],[1.31,13.46],[1.33,10],[1.62,5.18],[2,161.49],[1.34,3.1],[2.02,10.36],[1.61,73.13]],"ltp":1.11,"tv":629.25,"id":7812752},{"atb":[[15,5],[30,8.84]],"id":6203941},{"atb":[[2,65],[10,25.56],[4,10]],"id":7610784},{"atl":[[750,3]],"id":7610784},{"atb":[[1.01,502.57],[1.03,2.57],[1.02,185.22]],"id":7812754},{"atl":[[1.1,89.28],[1.09,5]],"id":7812754},{"atb":[[15,5],[30,8.84]],"id":6203939},{"atb":[[15,5],[30,8.84]],"id":7812758},{"atb":[[15,5],[30,8.84]],"id":9023044},{"atb":[[3,25],[13,2],[3.5,25],[7,36.52],[12,2],[8.2,10.95],[2,67.57]],"id":7812756},{"atl":[[32,16.2]],"id":7812756},{"trd":[[12.5,26.05]],"ltp":12.5,"tv":26.05,"id":7812756},{"atb":[[15,5],[30,8.84]],"id":7812760},{"atb":[[1.04,25],[1.06,97.56],[1.07,1.54],[1.01,502.57],[1.03,2.57],[1.02,185.22]],"id":7812755},{"atl":[[1.24,61.36],[1.19,5],[1.25,83.44]],"id":7812755},{"trd":[[1.06,4.88],[1.1,328.34],[1.07,3.1]],"ltp":1.06,"tv":336.32,"id":7812755},{"atb":[[6,15],[10,18.26],[4,25]],"id":8064931},{"atl":[[300,5],[900,3]],"id":8064931},{"atb":[[7,36.52],[2,67.57],[20,3],[4,25]],"id":7812761},{"atl":[[32,5],[55,5]],"id":7812761},{"trd":[[7,10]],"ltp":7.0,"tv":10.0,"id":7812761},{"atb":[[6,10],[12.5,5],[20,10.95]],"id":7812757},{"atb":[[6,10],[12.5,5],[20,10.95]],"id":7812763},{"atb":[[15,5],[30,8.84]],"id":9039059}],"con":true,"img":true,"tv":1233.83}]}'  # noqa
    result: MCM = benchmark.pedantic(stream_decode, args=(line,), rounds=10, iterations=10)
    assert isinstance(result, MCM)
    assert result.mc[0].market_definition
