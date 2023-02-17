window.BENCHMARK_DATA = {
  "lastUpdate": 1676615215901,
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
      },
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
          "id": "a6bef859b1473bec2a5490220e79df441a032aab",
          "message": "WIP",
          "timestamp": "2023-02-17T17:20:39+11:00",
          "tree_id": "a56ea891e826b9c353520ce473f62250c2e67c3b",
          "url": "https://github.com/limx0/betfair_parser/commit/a6bef859b1473bec2a5490220e79df441a032aab"
        },
        "date": 1676614898385,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.12443914463989912,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 8.036056522999985 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 575043.4258376253,
            "unit": "iter/sec",
            "range": "stddev: 3.0522191408501754e-8",
            "extra": "mean: 1.7389991000129612 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20671.544050161887,
            "unit": "iter/sec",
            "range": "stddev: 0.000005309317924902622",
            "extra": "mean: 48.37567999629755 usec\nrounds: 5"
          }
        ]
      },
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
          "id": "9a7055ac62a17a99119e5eb1b5f1fa056a3d364f",
          "message": "WIP",
          "timestamp": "2023-02-17T17:21:40+11:00",
          "tree_id": "f94d022328c80c53e99c87dfe742c3e2b70ca831",
          "url": "https://github.com/limx0/betfair_parser/commit/9a7055ac62a17a99119e5eb1b5f1fa056a3d364f"
        },
        "date": 1676614965074,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.09370145617151776,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 10.672192737000046 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 621943.5362128537,
            "unit": "iter/sec",
            "range": "stddev: 2.835721951374621e-8",
            "extra": "mean: 1.6078630000549765 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18361.83089579696,
            "unit": "iter/sec",
            "range": "stddev: 0.0000054622563099380416",
            "extra": "mean: 54.46079999728682 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "name": "limx0",
            "username": "limx0"
          },
          "id": "9a7055ac62a17a99119e5eb1b5f1fa056a3d364f",
          "message": "Add benchmarking to CI",
          "timestamp": "2022-12-06T07:23:44Z",
          "url": "https://github.com/limx0/betfair_parser/pull/3/commits/9a7055ac62a17a99119e5eb1b5f1fa056a3d364f"
        },
        "date": 1676614973155,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1269791877275275,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 7.87530632299999 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 606210.7258786607,
            "unit": "iter/sec",
            "range": "stddev: 5.454067829290689e-8",
            "extra": "mean: 1.6495914000046241 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20119.21844078265,
            "unit": "iter/sec",
            "range": "stddev: 0.000005369603040682954",
            "extra": "mean: 49.70372000002499 usec\nrounds: 5"
          }
        ]
      },
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
          "id": "7bc43ab8f355c01a1449b917ed8f3593c7af35d5",
          "message": "Cleanup",
          "timestamp": "2023-02-17T17:23:06+11:00",
          "tree_id": "6ad309781a51ca309acc3f7f020e09fe6fef5a74",
          "url": "https://github.com/limx0/betfair_parser/commit/7bc43ab8f355c01a1449b917ed8f3593c7af35d5"
        },
        "date": 1676615056857,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.12380659696615345,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 8.077114018999993 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 605988.4016277854,
            "unit": "iter/sec",
            "range": "stddev: 2.973768113184444e-8",
            "extra": "mean: 1.6501965999907497 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20364.97289711815,
            "unit": "iter/sec",
            "range": "stddev: 0.000005304520790191034",
            "extra": "mean: 49.103920002835366 usec\nrounds: 5"
          }
        ]
      },
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
          "id": "743d9e79813820edc1e399f80de4676a2741910f",
          "message": "Bump msgspec version",
          "timestamp": "2023-02-17T17:25:53+11:00",
          "tree_id": "15cee28f53d9e548f051636efdca5bfeda8ee096",
          "url": "https://github.com/limx0/betfair_parser/commit/743d9e79813820edc1e399f80de4676a2741910f"
        },
        "date": 1676615214898,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1101768513082793,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 9.076316740999971 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 642857.207152165,
            "unit": "iter/sec",
            "range": "stddev: 3.126368471131825e-8",
            "extra": "mean: 1.555555399977493 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19172.925988244366,
            "unit": "iter/sec",
            "range": "stddev: 0.0000048965096584516055",
            "extra": "mean: 52.15687999907459 usec\nrounds: 5"
          }
        ]
      }
    ]
  }
}