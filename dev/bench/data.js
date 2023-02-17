window.BENCHMARK_DATA = {
  "lastUpdate": 1676614723396,
  "repoUrl": "https://github.com/limx0/betfair_parser",
  "entries": {
    "Python Benchmark with pytest-benchmark": [
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "Bradley McElroy",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "Bradley McElroy",
            "username": "limx0"
          },
          "distinct": true,
          "id": "5b63b53717112453eb6a596849997499ce5ed449",
          "message": "WIP",
          "timestamp": "2023-02-17T17:13:42+11:00",
          "tree_id": "906ee6a5ae82d06b3a228c92749adb59b8610219",
          "url": "https://github.com/limx0/betfair_parser/commit/5b63b53717112453eb6a596849997499ce5ed449"
        },
        "date": 1676614722849,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.12423699870539515,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 8.049131985000002 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 610980.2187862191,
            "unit": "iter/sec",
            "range": "stddev: 2.446924188293714e-8",
            "extra": "mean: 1.636714199989342 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20146.61903429364,
            "unit": "iter/sec",
            "range": "stddev: 0.000005638946108474067",
            "extra": "mean: 49.63612000096873 usec\nrounds: 5"
          }
        ]
      }
    ]
  }
}