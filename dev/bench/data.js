window.BENCHMARK_DATA = {
  "lastUpdate": 1685240966743,
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
          "id": "9c5f6b2fdef4186ba2431366a78e66599bc2ec63",
          "message": "Use structs instead of namedtuple",
          "timestamp": "2023-02-17T17:54:10+11:00",
          "tree_id": "be2162265ed6ebd6f38df3c387f53dcdf368dc87",
          "url": "https://github.com/limx0/betfair_parser/commit/9c5f6b2fdef4186ba2431366a78e66599bc2ec63"
        },
        "date": 1676616910140,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.14346426125082615,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.970377091000017 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 487938.00182082324,
            "unit": "iter/sec",
            "range": "stddev: 4.234068711578531e-8",
            "extra": "mean: 2.0494406999830517 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 16411.414467014714,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031957659481663646",
            "extra": "mean: 60.93319999990854 usec\nrounds: 5"
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
          "id": "e05501f22640caf385eddb3328fc5e56d6880d11",
          "message": "Version bump",
          "timestamp": "2023-02-17T21:40:38+11:00",
          "tree_id": "e1476ec33d454a46eadb7a5f782efe7c60dba807",
          "url": "https://github.com/limx0/betfair_parser/commit/e05501f22640caf385eddb3328fc5e56d6880d11"
        },
        "date": 1676630565878,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.20031646965407696,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 4.992100757999992 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 654268.5395538729,
            "unit": "iter/sec",
            "range": "stddev: 2.8548709766281034e-8",
            "extra": "mean: 1.5284243999900582 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 23208.404041360278,
            "unit": "iter/sec",
            "range": "stddev: 0.0000046394291895320145",
            "extra": "mean: 43.08784000045307 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "distinct": true,
          "id": "654538dc50702da14efc666bb4ba5f81bef980d7",
          "message": "Tighten msgspec parsing with forbid_unknown_fields",
          "timestamp": "2023-02-24T15:44:45+11:00",
          "tree_id": "d72b18c49da63468f9275924475e79badb402ba4",
          "url": "https://github.com/limx0/betfair_parser/commit/654538dc50702da14efc666bb4ba5f81bef980d7"
        },
        "date": 1677213959662,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.14530200949732427,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.882217275999992 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 578750.5597241012,
            "unit": "iter/sec",
            "range": "stddev: 1.7650719427349717e-7",
            "extra": "mean: 1.7278601000001004 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15744.956890270925,
            "unit": "iter/sec",
            "range": "stddev: 0.000005219813600394276",
            "extra": "mean: 63.51240000014969 usec\nrounds: 5"
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
          "id": "a5694fa94a2d9566a667d31d5a177fd7224d5db4",
          "message": "Version bump",
          "timestamp": "2023-02-24T15:46:10+11:00",
          "tree_id": "632d2e5eb635e936a9204f0cd35ef0a199ca69b8",
          "url": "https://github.com/limx0/betfair_parser/commit/a5694fa94a2d9566a667d31d5a177fd7224d5db4"
        },
        "date": 1677214031752,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.19152281872145593,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.2213099550000095 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 637882.4344437938,
            "unit": "iter/sec",
            "range": "stddev: 3.949341154152148e-8",
            "extra": "mean: 1.5676869999907694 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 22014.832713321914,
            "unit": "iter/sec",
            "range": "stddev: 0.000005531197593525202",
            "extra": "mean: 45.42392000075779 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "distinct": true,
          "id": "c91fdcb5d3bf13a32e4e11f8809058c9bea0e93f",
          "message": "Implement FlattenedMarket in navigation",
          "timestamp": "2023-02-24T16:53:38+11:00",
          "tree_id": "6a9fa6272d4d5bad0e237e022b2dcbf2dbf43686",
          "url": "https://github.com/limx0/betfair_parser/commit/c91fdcb5d3bf13a32e4e11f8809058c9bea0e93f"
        },
        "date": 1677218083467,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.15127171006674103,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.610621374999994 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 637798.0557862286,
            "unit": "iter/sec",
            "range": "stddev: 2.4041694764446414e-8",
            "extra": "mean: 1.567894400002956 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20416.06303194917,
            "unit": "iter/sec",
            "range": "stddev: 0.000004767310563530555",
            "extra": "mean: 48.98103999948943 usec\nrounds: 5"
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
          "id": "9e0e8ae6dd3fa411db82f59e53788dcd4ff9ca95",
          "message": "Version bump",
          "timestamp": "2023-02-24T16:54:01+11:00",
          "tree_id": "9a1aa9f66c0eb48a6f7b1bb83e5f51bfc0feb71c",
          "url": "https://github.com/limx0/betfair_parser/commit/9e0e8ae6dd3fa411db82f59e53788dcd4ff9ca95"
        },
        "date": 1677218102833,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1475363908857796,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.777988766000007 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 624655.9707226364,
            "unit": "iter/sec",
            "range": "stddev: 4.3652662831065965e-8",
            "extra": "mean: 1.600881200003812 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15749.906603250127,
            "unit": "iter/sec",
            "range": "stddev: 0.000003733244273714109",
            "extra": "mean: 63.492439999208734 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "distinct": true,
          "id": "e16a99055edd1851867b71c28d70247e95bdedd5",
          "message": "Revert piped union syntax, keep python39 compat",
          "timestamp": "2023-02-24T17:14:43+11:00",
          "tree_id": "e41e0f966af0ba40701fb84a008bab3a6f3a4b55",
          "url": "https://github.com/limx0/betfair_parser/commit/e16a99055edd1851867b71c28d70247e95bdedd5"
        },
        "date": 1677219343191,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.16534114623511204,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.048101290999995 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 633982.7831870364,
            "unit": "iter/sec",
            "range": "stddev: 3.667869033975051e-8",
            "extra": "mean: 1.5773298999903318 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19826.730239424498,
            "unit": "iter/sec",
            "range": "stddev: 0.000005059920911524464",
            "extra": "mean: 50.436959999160536 usec\nrounds: 5"
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
          "id": "e279daa2385c653bd1e6e145ec597ee38fa09c60",
          "message": "Version bump",
          "timestamp": "2023-02-24T17:16:12+11:00",
          "tree_id": "830011be293de1b218e10ed0025bfb1efc2c1915",
          "url": "https://github.com/limx0/betfair_parser/commit/e279daa2385c653bd1e6e145ec597ee38fa09c60"
        },
        "date": 1677219428092,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1930168405599067,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.180895082000006 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 637340.221197491,
            "unit": "iter/sec",
            "range": "stddev: 3.161031680388027e-8",
            "extra": "mean: 1.5690206999977363 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 22115.75207664942,
            "unit": "iter/sec",
            "range": "stddev: 0.000004831182505661737",
            "extra": "mean: 45.21664000094461 usec\nrounds: 5"
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
          "id": "41b97feec7fcca57c011f99abd5b72b8613f7384",
          "message": "fix bug in market catalog, add test",
          "timestamp": "2023-02-24T20:47:45+11:00",
          "tree_id": "e24c8ea96a5502b91c898edc52854a1f67b0f00d",
          "url": "https://github.com/limx0/betfair_parser/commit/41b97feec7fcca57c011f99abd5b72b8613f7384"
        },
        "date": 1677232461232,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.16774331235560921,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.9614895280000155 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 630599.9641586175,
            "unit": "iter/sec",
            "range": "stddev: 2.705787340895318e-8",
            "extra": "mean: 1.5857913999951734 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19604.614141722053,
            "unit": "iter/sec",
            "range": "stddev: 0.000004384281013937942",
            "extra": "mean: 51.00840000068274 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "distinct": true,
          "id": "0f18e03625038c9516a1a2ded67f923d00a26f55",
          "message": "Implement Navigation and MarketCatalogue parsing",
          "timestamp": "2023-02-25T11:42:18+11:00",
          "tree_id": "638a3665cd4731a16ad1bbdffd1ff70432e22df8",
          "url": "https://github.com/limx0/betfair_parser/commit/0f18e03625038c9516a1a2ded67f923d00a26f55"
        },
        "date": 1677285797522,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.16540805094820943,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.045654938000013 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 466959.85831183573,
            "unit": "iter/sec",
            "range": "stddev: 4.232486572167813e-8",
            "extra": "mean: 2.141511699988996 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15938.480017829477,
            "unit": "iter/sec",
            "range": "stddev: 0.000002839801754687062",
            "extra": "mean: 62.74123999787662 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "distinct": true,
          "id": "a8458706defeb5b3e4662275ba2a8fcb6049382b",
          "message": "Version bump",
          "timestamp": "2023-02-25T11:43:42+11:00",
          "tree_id": "a6454dafba42cb6af2c0e271032189ef63737527",
          "url": "https://github.com/limx0/betfair_parser/commit/a8458706defeb5b3e4662275ba2a8fcb6049382b"
        },
        "date": 1677285887320,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.14178114426335756,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 7.053124061000005 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 542752.5947494472,
            "unit": "iter/sec",
            "range": "stddev: 1.2512561731965098e-7",
            "extra": "mean: 1.8424601000049279 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 16769.51972096502,
            "unit": "iter/sec",
            "range": "stddev: 0.000005843091645462928",
            "extra": "mean: 59.63199999996504 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "distinct": true,
          "id": "48c711dff855afb0d010d954e0e2a2439d3be3f1",
          "message": "Version bump",
          "timestamp": "2023-02-27T18:48:18+11:00",
          "tree_id": "e44941c34ba2f3d8969d71d07a11005622a21260",
          "url": "https://github.com/limx0/betfair_parser/commit/48c711dff855afb0d010d954e0e2a2439d3be3f1"
        },
        "date": 1677484151205,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1942155976162314,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.148917040000015 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 617634.5535342661,
            "unit": "iter/sec",
            "range": "stddev: 3.330295026236177e-8",
            "extra": "mean: 1.6190804000160597 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 22075.19163473726,
            "unit": "iter/sec",
            "range": "stddev: 0.000004877505718077496",
            "extra": "mean: 45.29972000000271 usec\nrounds: 5"
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
          "id": "71730f77c34da56c74c8d0387aec8b9fae3923dc",
          "message": "Version bump",
          "timestamp": "2023-02-28T07:47:18+11:00",
          "tree_id": "53415a465cc2a568680e2831a8a2cf300e522592",
          "url": "https://github.com/limx0/betfair_parser/commit/71730f77c34da56c74c8d0387aec8b9fae3923dc"
        },
        "date": 1677530898776,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.18939201914538809,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.28005353399999 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 629965.2681221217,
            "unit": "iter/sec",
            "range": "stddev: 3.04641329964729e-8",
            "extra": "mean: 1.5873891000069307 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 22244.407310805756,
            "unit": "iter/sec",
            "range": "stddev: 0.000005394402025722678",
            "extra": "mean: 44.95512000062263 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "distinct": true,
          "id": "a8c79ae60b1e820524fe75cf1b870443b1af744c",
          "message": "Relax raceType field in MarketDefinition",
          "timestamp": "2023-03-01T07:45:09+11:00",
          "tree_id": "9b85a7e06beb081988459395cccb9169d11622b8",
          "url": "https://github.com/limx0/betfair_parser/commit/a8c79ae60b1e820524fe75cf1b870443b1af744c"
        },
        "date": 1677617166589,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.13979787521606474,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 7.153184542000005 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 639021.611902599,
            "unit": "iter/sec",
            "range": "stddev: 2.9069714317184328e-8",
            "extra": "mean: 1.5648923000000536 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19575.064499911783,
            "unit": "iter/sec",
            "range": "stddev: 0.000006239678202489054",
            "extra": "mean: 51.085399999806214 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "committer": {
            "email": "bradley.mcelroy@live.com",
            "name": "limx0",
            "username": "limx0"
          },
          "distinct": true,
          "id": "1fa2c952c9ace32458646358eb3d2fc99d5f7835",
          "message": "Version bump",
          "timestamp": "2023-03-01T07:50:33+11:00",
          "tree_id": "cceb3563c31d8fef8be6393964078d3a7461893a",
          "url": "https://github.com/limx0/betfair_parser/commit/1fa2c952c9ace32458646358eb3d2fc99d5f7835"
        },
        "date": 1677617488344,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.18695789582195174,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.348797896999997 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 640362.2093659198,
            "unit": "iter/sec",
            "range": "stddev: 3.2103905769756544e-8",
            "extra": "mean: 1.5616161999787437 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 21983.742583184194,
            "unit": "iter/sec",
            "range": "stddev: 0.000006056731693895909",
            "extra": "mean: 45.4881599989676 usec\nrounds: 5"
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
          "id": "5bd3db8ad02594db54a64b740cd94eae4d05fd79",
          "message": "Version bump",
          "timestamp": "2023-03-09T10:13:06+11:00",
          "tree_id": "e01623cc5e3e4fad74cf5c0ec9389bf1586173ea",
          "url": "https://github.com/limx0/betfair_parser/commit/5bd3db8ad02594db54a64b740cd94eae4d05fd79"
        },
        "date": 1678317231655,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1498718998486636,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.672364873000021 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 639577.7354274233,
            "unit": "iter/sec",
            "range": "stddev: 3.140595518809703e-8",
            "extra": "mean: 1.563531600004353 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19258.649830495022,
            "unit": "iter/sec",
            "range": "stddev: 0.000005658112829590868",
            "extra": "mean: 51.924719998623914 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "Brad",
            "username": "limx0"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "44e340e48789f5410d16d8e2d17829be981f178c",
          "message": "Merge pull request #4 from ml31415/main\n\nProper parametrized testcase ids",
          "timestamp": "2023-05-09T10:06:12+10:00",
          "tree_id": "6a488047ccc77f7a5e34f754e2e2b19368905679",
          "url": "https://github.com/limx0/betfair_parser/commit/44e340e48789f5410d16d8e2d17829be981f178c"
        },
        "date": 1683590818939,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.13738523515794515,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 7.278802549999995 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 624724.2623187348,
            "unit": "iter/sec",
            "range": "stddev: 3.14105972858174e-8",
            "extra": "mean: 1.60070620002557 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19453.542218202452,
            "unit": "iter/sec",
            "range": "stddev: 0.000006734251169401874",
            "extra": "mean: 51.40451999864126 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "committer": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "distinct": true,
          "id": "fdf0051ccb7ca27c06a4b31d63d51538533f08ce",
          "message": "Bump precommit, fixing mypy complaints",
          "timestamp": "2023-05-09T10:46:06+10:00",
          "tree_id": "57c7855c1c711084599b4b726d7cff6fd81e3659",
          "url": "https://github.com/limx0/betfair_parser/commit/fdf0051ccb7ca27c06a4b31d63d51538533f08ce"
        },
        "date": 1683593219944,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.14715486995492108,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.795561711999994 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 579352.4577590111,
            "unit": "iter/sec",
            "range": "stddev: 1.2254385344239203e-7",
            "extra": "mean: 1.7260649999968791 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 16855.652239724743,
            "unit": "iter/sec",
            "range": "stddev: 0.000006678267089579199",
            "extra": "mean: 59.32727999947929 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "Brad",
            "username": "limx0"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "06711027d46d469655c488753e1fd7152e61dbdd",
          "message": "Merge pull request #5 from ml31415/main\n\nEnum refactoring",
          "timestamp": "2023-05-15T06:17:38+10:00",
          "tree_id": "fa58a3a048338e4bf8409c988df0cc498309e975",
          "url": "https://github.com/limx0/betfair_parser/commit/06711027d46d469655c488753e1fd7152e61dbdd"
        },
        "date": 1684095508706,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.16503037283425992,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.059490643000004 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 621100.5753090712,
            "unit": "iter/sec",
            "range": "stddev: 2.7870223954605988e-8",
            "extra": "mean: 1.6100452000102905 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19582.439721637355,
            "unit": "iter/sec",
            "range": "stddev: 0.000005313155029433614",
            "extra": "mean: 51.06615999920905 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "michael@loeffler.io",
            "name": "Michael",
            "username": "ml31415"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "5ee0ef0abeabd696033e6ae76dea8b713453495c",
          "message": "WIP: API completion and refactoring (#8)\n\n* Refactoring spec more to how betfair structures the API\r\n\r\nAdded most type definitions and enums from the API\r\n\r\nUsing msgspec 0.15 generic structs for API responses\r\n\r\nAdded FloatStr and IntStr and according hooks for dealing with betfairs inconsistent quotation usage\r\n\r\n* Updated poetry.lock\r\n\r\n* Completed all API calls; tests missing so far\r\n\r\n* Tests extended and restructured",
          "timestamp": "2023-05-20T11:52:08+10:00",
          "tree_id": "2d89073334c3b4d02090bb5fb57e851aed8e4bbc",
          "url": "https://github.com/limx0/betfair_parser/commit/5ee0ef0abeabd696033e6ae76dea8b713453495c"
        },
        "date": 1684547572249,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1847525841696364,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.412644182999998 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 604272.2166576693,
            "unit": "iter/sec",
            "range": "stddev: 2.092611138423934e-8",
            "extra": "mean: 1.654883299998744 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20559.548676584625,
            "unit": "iter/sec",
            "range": "stddev: 0.000006346413791295265",
            "extra": "mean: 48.63920000047983 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "committer": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "distinct": true,
          "id": "39a2a925b5d7eeba61afd4ab580a8e4c39e6806d",
          "message": "Bump msgspec patch",
          "timestamp": "2023-05-20T11:53:40+10:00",
          "tree_id": "2616bb90d63404f7707455542afd2e1f13878e32",
          "url": "https://github.com/limx0/betfair_parser/commit/39a2a925b5d7eeba61afd4ab580a8e4c39e6806d"
        },
        "date": 1684547668747,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.19215421529932875,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.204153332999994 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 623288.9161030039,
            "unit": "iter/sec",
            "range": "stddev: 2.5783943060142843e-8",
            "extra": "mean: 1.6043924000001653 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20697.437408775462,
            "unit": "iter/sec",
            "range": "stddev: 0.000005858745565230619",
            "extra": "mean: 48.31516000024294 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "committer": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "distinct": true,
          "id": "45efc615ee0e32f9463c35f995048769f358f0cd",
          "message": "Bump version",
          "timestamp": "2023-05-20T11:54:52+10:00",
          "tree_id": "e3b1f574e65c9873840bd908cc693a56f11d1bc3",
          "url": "https://github.com/limx0/betfair_parser/commit/45efc615ee0e32f9463c35f995048769f358f0cd"
        },
        "date": 1684547739130,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.19426509379420598,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.147605164000005 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 623054.0852668165,
            "unit": "iter/sec",
            "range": "stddev: 3.046288124059984e-8",
            "extra": "mean: 1.6049971000057894 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 21175.583705186837,
            "unit": "iter/sec",
            "range": "stddev: 0.000005921813910747701",
            "extra": "mean: 47.22419999950489 usec\nrounds: 5"
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
          "id": "b8dd717e3b0ad67f896a5aed1f1d8bb74ef9bfac",
          "message": "Support python3.9",
          "timestamp": "2023-04-11T15:47:15Z",
          "url": "https://github.com/limx0/betfair_parser/pull/9/commits/b8dd717e3b0ad67f896a5aed1f1d8bb74ef9bfac"
        },
        "date": 1684572488817,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.17207224447264816,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.811512502000028 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 459976.12080301944,
            "unit": "iter/sec",
            "range": "stddev: 3.7206246063314794e-8",
            "extra": "mean: 2.1740258999841444 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15193.430603393339,
            "unit": "iter/sec",
            "range": "stddev: 0.00000532029390772313",
            "extra": "mean: 65.81792000133646 usec\nrounds: 5"
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
          "id": "9ccb7ba84e9d14811e326db3a31e474930af4fb7",
          "message": "Support python3.9",
          "timestamp": "2023-04-11T15:47:15Z",
          "url": "https://github.com/limx0/betfair_parser/pull/9/commits/9ccb7ba84e9d14811e326db3a31e474930af4fb7"
        },
        "date": 1684573091512,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.16836495793623102,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.939478215999998 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 616042.8903829884,
            "unit": "iter/sec",
            "range": "stddev: 4.219309914231872e-8",
            "extra": "mean: 1.6232636000040657 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18856.04166406575,
            "unit": "iter/sec",
            "range": "stddev: 0.000005757016242197058",
            "extra": "mean: 53.033400000686015 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "Brad",
            "username": "limx0"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "8c483c1e9db3bbe7fda2d6251d7781fc1a474929",
          "message": "Support python3.9 (#9)\n\n* Support python3.9\r\n\r\n* Fixing py39\r\n\r\n---------\r\n\r\nCo-authored-by: brad <brad@edgestackers.com>",
          "timestamp": "2023-05-20T18:59:14+10:00",
          "tree_id": "e657b552cd8708b4f81e40fd5fac4627164238e5",
          "url": "https://github.com/limx0/betfair_parser/commit/8c483c1e9db3bbe7fda2d6251d7781fc1a474929"
        },
        "date": 1684573194831,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1474124200973056,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.783688913999981 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 611717.9216961919,
            "unit": "iter/sec",
            "range": "stddev: 2.870947519849411e-8",
            "extra": "mean: 1.634740399998691 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18282.64530848251,
            "unit": "iter/sec",
            "range": "stddev: 0.000006545940484516502",
            "extra": "mean: 54.69668000046113 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "committer": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "distinct": true,
          "id": "4a8da45801c64c7e2d5143a785d5e7fa58d95392",
          "message": "Bump version",
          "timestamp": "2023-05-20T19:00:15+10:00",
          "tree_id": "d534fe0716028f893cd10d948335a2b1c04ba1de",
          "url": "https://github.com/limx0/betfair_parser/commit/4a8da45801c64c7e2d5143a785d5e7fa58d95392"
        },
        "date": 1684573260655,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.17655674042615366,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.663901573999993 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 620563.4753605799,
            "unit": "iter/sec",
            "range": "stddev: 2.738900382202451e-8",
            "extra": "mean: 1.6114386999959152 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20681.684878889337,
            "unit": "iter/sec",
            "range": "stddev: 0.000006515247133207807",
            "extra": "mean: 48.3519600001614 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "michael@loeffler.io",
            "name": "Michael",
            "username": "ml31415"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f33f5afe9d36a12e52e55649f02ba6db52cf9ccd",
          "message": "Further improvements (#10)\n\n* Refactoring spec more to how betfair structures the API\r\n\r\nAdded most type definitions and enums from the API\r\n\r\nUsing msgspec 0.15 generic structs for API responses\r\n\r\nAdded FloatStr and IntStr and according hooks for dealing with betfairs inconsistent quotation usage\r\n\r\n* Updated poetry.lock\r\n\r\n* Completed all API calls; tests missing so far\r\n\r\n* Tests extended and restructured\r\n\r\n* Further test improvements",
          "timestamp": "2023-05-21T07:34:16+10:00",
          "tree_id": "edeb333f1ab03188c345363bb0c7ef1bfe3175f0",
          "url": "https://github.com/limx0/betfair_parser/commit/f33f5afe9d36a12e52e55649f02ba6db52cf9ccd"
        },
        "date": 1684618501651,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.19134148617031738,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.226258141999992 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 619316.7239634132,
            "unit": "iter/sec",
            "range": "stddev: 2.4928839078915356e-8",
            "extra": "mean: 1.6146826999928976 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 21008.368053390866,
            "unit": "iter/sec",
            "range": "stddev: 0.000006702299158743506",
            "extra": "mean: 47.60007999948356 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "michael@loeffler.io",
            "name": "Michael",
            "username": "ml31415"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1d981ba2dd9b7c157a0397368cf3cbd63ef82854",
          "message": "Api completion & parametrized XML tests (#11)\n\n* Added tests against the betfair XML API specification for completeness and correctness\r\n\r\n* Last minute docstring fix",
          "timestamp": "2023-05-22T09:44:27+10:00",
          "tree_id": "849af7e6cfbf17ea6b7567c5b5bbf7add5dd3494",
          "url": "https://github.com/limx0/betfair_parser/commit/1d981ba2dd9b7c157a0397368cf3cbd63ef82854"
        },
        "date": 1684712719647,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.16614833473138688,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.018718162999988 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 461447.0027404402,
            "unit": "iter/sec",
            "range": "stddev: 4.8488862760220673e-8",
            "extra": "mean: 2.1670961000097577 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18681.40654514575,
            "unit": "iter/sec",
            "range": "stddev: 0.000006107600579906318",
            "extra": "mean: 53.52916000106234 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "michael@loeffler.io",
            "name": "Michael",
            "username": "ml31415"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "48647e4fc809b28501c29fe1028b7560c5f31884",
          "message": "Api completion py3.9 (#12)\n\n* Added tests against the betfair XML API specification for completeness and correctness\r\n\r\n* Last minute docstring fix\r\n\r\n* Fix py3.9 issue with completeness tests\r\n\r\n* Fix py3.9 issue with completeness tests\r\n\r\n* Added XML tests for error type",
          "timestamp": "2023-05-23T17:22:34+10:00",
          "tree_id": "57362bb8a19476daad7f59769fec5303bfaa5fe8",
          "url": "https://github.com/limx0/betfair_parser/commit/48647e4fc809b28501c29fe1028b7560c5f31884"
        },
        "date": 1684826594651,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1688126325179064,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.923727300999985 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 604103.5667915955,
            "unit": "iter/sec",
            "range": "stddev: 2.884677788822911e-8",
            "extra": "mean: 1.6553452999971796 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18634.285743790355,
            "unit": "iter/sec",
            "range": "stddev: 0.000005732245005140447",
            "extra": "mean: 53.66452000089339 usec\nrounds: 5"
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
          "id": "074e040f5877ddf6a92e86c7fd7e68861da8f86d",
          "message": "Navigation update",
          "timestamp": "2023-04-11T15:47:15Z",
          "url": "https://github.com/limx0/betfair_parser/pull/13/commits/074e040f5877ddf6a92e86c7fd7e68861da8f86d"
        },
        "date": 1684826626087,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.15741589365888065,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.352598690999997 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 562078.8553906017,
            "unit": "iter/sec",
            "range": "stddev: 2.1115695213531952e-7",
            "extra": "mean: 1.779109800003198 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19402.074625739926,
            "unit": "iter/sec",
            "range": "stddev: 0.000004217624925544403",
            "extra": "mean: 51.54087999812873 usec\nrounds: 5"
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
          "id": "894d7d7e3cec720c6b5e135c5d29556ca9c84a1f",
          "message": "Navigation update",
          "timestamp": "2023-04-11T15:47:15Z",
          "url": "https://github.com/limx0/betfair_parser/pull/13/commits/894d7d7e3cec720c6b5e135c5d29556ca9c84a1f"
        },
        "date": 1684826655666,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.14909286934985935,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.707228885999996 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 537186.4066914617,
            "unit": "iter/sec",
            "range": "stddev: 6.664546056694957e-8",
            "extra": "mean: 1.861551199999667 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15896.047480104437,
            "unit": "iter/sec",
            "range": "stddev: 0.00000722055618575208",
            "extra": "mean: 62.90871999794945 usec\nrounds: 5"
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
          "id": "d61268c79adc86d74328a75eccad05e37066a410",
          "message": "Navigation update",
          "timestamp": "2023-04-11T15:47:15Z",
          "url": "https://github.com/limx0/betfair_parser/pull/13/commits/d61268c79adc86d74328a75eccad05e37066a410"
        },
        "date": 1684826886764,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.15850002456916873,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.309147286999973 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 634847.1538788547,
            "unit": "iter/sec",
            "range": "stddev: 2.034007762801354e-7",
            "extra": "mean: 1.5751823000073273 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 16510.499356888653,
            "unit": "iter/sec",
            "range": "stddev: 0.000008169713643612628",
            "extra": "mean: 60.567519999494834 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "Brad",
            "username": "limx0"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ee68e2439ab973de008ee9a3343fbcbc7ec6e733",
          "message": "Navigation update (#13)\n\n* WIP\r\n\r\n* Add simple navigation test\r\n\r\n* Api completion py3.9 (#12)\r\n\r\n* Added tests against the betfair XML API specification for completeness and correctness\r\n\r\n* Last minute docstring fix\r\n\r\n* Fix py3.9 issue with completeness tests\r\n\r\n* Fix py3.9 issue with completeness tests\r\n\r\n* Added XML tests for error type\r\n\r\n---------\r\n\r\nCo-authored-by: brad <brad@edgestackers.com>\r\nCo-authored-by: Michael <michael@loeffler.io>",
          "timestamp": "2023-05-23T17:29:33+10:00",
          "tree_id": "37075601f9ac818326d81afc650f654f22d90a73",
          "url": "https://github.com/limx0/betfair_parser/commit/ee68e2439ab973de008ee9a3343fbcbc7ec6e733"
        },
        "date": 1684827019606,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1553551414712299,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.436864531999987 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 458162.9215444872,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025270567155136036",
            "extra": "mean: 2.1826296999961414 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18583.215639283175,
            "unit": "iter/sec",
            "range": "stddev: 0.000009569750257035584",
            "extra": "mean: 53.81200000101671 usec\nrounds: 5"
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
          "id": "22c4e177e5d62beac909f7f7f93c6d4923c0086a",
          "message": "Bump version",
          "timestamp": "2023-05-24T16:41:29+10:00",
          "tree_id": "58c7c5bbb65798ace842b5858dcfd3f7ef0bef8a",
          "url": "https://github.com/limx0/betfair_parser/commit/22c4e177e5d62beac909f7f7f93c6d4923c0086a"
        },
        "date": 1684910537539,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1919348889418474,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.21010018299998 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 622420.8048842303,
            "unit": "iter/sec",
            "range": "stddev: 3.948461758785065e-8",
            "extra": "mean: 1.6066301000108751 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20515.210797620006,
            "unit": "iter/sec",
            "range": "stddev: 0.000007269897852294756",
            "extra": "mean: 48.74432000065099 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "michael@loeffler.io",
            "name": "Michael",
            "username": "ml31415"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bbff396b3e58b76d4a03ccfc77994b0158be649b",
          "message": "camel case (#15)\n\n* First draft camel case\r\n\r\n* Fix benchmark",
          "timestamp": "2023-05-27T08:08:30+10:00",
          "tree_id": "ee5cb7023eea93501e9432c95720d6b56ec4f792",
          "url": "https://github.com/limx0/betfair_parser/commit/bbff396b3e58b76d4a03ccfc77994b0158be649b"
        },
        "date": 1685138952566,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.18281629359891344,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.469971960999999 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 613571.9539214513,
            "unit": "iter/sec",
            "range": "stddev: 4.63704809285264e-8",
            "extra": "mean: 1.6298006999974746 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 19940.974714513457,
            "unit": "iter/sec",
            "range": "stddev: 0.000007303240377269899",
            "extra": "mean: 50.148000000831416 usec\nrounds: 5"
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
          "id": "8a57547abd667c107202222a867cccba253623e4",
          "message": "Add automated release",
          "timestamp": "2023-05-25T14:18:40Z",
          "url": "https://github.com/limx0/betfair_parser/pull/16/commits/8a57547abd667c107202222a867cccba253623e4"
        },
        "date": 1685170516719,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1466902558699929,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.817085388999999 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 537331.2786465597,
            "unit": "iter/sec",
            "range": "stddev: 7.487068681875904e-8",
            "extra": "mean: 1.8610493000124961 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15466.516538489617,
            "unit": "iter/sec",
            "range": "stddev: 0.00000632739189065986",
            "extra": "mean: 64.65579999940019 usec\nrounds: 5"
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
          "id": "c8af7ac9cf6ca22f31d01e073f0f45b4a8561463",
          "message": "Add automated release",
          "timestamp": "2023-05-25T14:18:40Z",
          "url": "https://github.com/limx0/betfair_parser/pull/16/commits/c8af7ac9cf6ca22f31d01e073f0f45b4a8561463"
        },
        "date": 1685170573294,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.18667843748388543,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.356805068000007 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 615231.2051154347,
            "unit": "iter/sec",
            "range": "stddev: 3.037584229270006e-8",
            "extra": "mean: 1.6254052000050478 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20079.86968968423,
            "unit": "iter/sec",
            "range": "stddev: 0.000008301670556122609",
            "extra": "mean: 49.80111999998371 usec\nrounds: 5"
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
          "id": "efb01f7318297c33751893ca63fb13a8bd675a7c",
          "message": "Add automated release",
          "timestamp": "2023-05-25T14:18:40Z",
          "url": "https://github.com/limx0/betfair_parser/pull/16/commits/efb01f7318297c33751893ca63fb13a8bd675a7c"
        },
        "date": 1685170994487,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1420911705832667,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 7.037734968999999 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 592596.4554491611,
            "unit": "iter/sec",
            "range": "stddev: 4.2015182067146937e-8",
            "extra": "mean: 1.6874889999840548 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18413.398472422145,
            "unit": "iter/sec",
            "range": "stddev: 0.000008202558407005139",
            "extra": "mean: 54.3082800004413 usec\nrounds: 5"
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
          "id": "aa6361f5493b50912e5e59319ec57ca92c8189ae",
          "message": "Add automated release",
          "timestamp": "2023-05-25T14:18:40Z",
          "url": "https://github.com/limx0/betfair_parser/pull/16/commits/aa6361f5493b50912e5e59319ec57ca92c8189ae"
        },
        "date": 1685171005663,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.17044156506073846,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.867113457000002 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 621530.3070584022,
            "unit": "iter/sec",
            "range": "stddev: 3.062727867426432e-8",
            "extra": "mean: 1.6089320000062912 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18053.8655130152,
            "unit": "iter/sec",
            "range": "stddev: 0.000008087046190798337",
            "extra": "mean: 55.38980000039828 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "Brad",
            "username": "limx0"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "69e60569cf15e959a61023cfac82cbdc28cac403",
          "message": "Add automated release (#16)\n\n* Add automated release\r\n\r\n* Use 3.10 for release\r\n\r\n* Add poetry build\r\n\r\n* Fix python version",
          "timestamp": "2023-05-27T17:05:54+10:00",
          "tree_id": "7a16a134d397767369cb115bd7c9cd8fa30c3ee7",
          "url": "https://github.com/limx0/betfair_parser/commit/69e60569cf15e959a61023cfac82cbdc28cac403"
        },
        "date": 1685171211971,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.13255685934851824,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 7.543932505000001 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 489113.19619901065,
            "unit": "iter/sec",
            "range": "stddev: 3.820692211371146e-7",
            "extra": "mean: 2.044516500006921 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 14646.529446343136,
            "unit": "iter/sec",
            "range": "stddev: 0.000016056687566343927",
            "extra": "mean: 68.27555999961987 usec\nrounds: 5"
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
          "id": "95e386f6afe9f7109e847d4ce58f4ac424a6b677",
          "message": "Use git tag for building",
          "timestamp": "2023-05-27T17:27:40+10:00",
          "tree_id": "7130b97c6605273885d90ee4fb44faae519f2e40",
          "url": "https://github.com/limx0/betfair_parser/commit/95e386f6afe9f7109e847d4ce58f4ac424a6b677"
        },
        "date": 1685172510271,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.13951551061659337,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 7.1676618289999965 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 566713.0332437307,
            "unit": "iter/sec",
            "range": "stddev: 5.984959082984113e-7",
            "extra": "mean: 1.7645614999821646 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20707.346386311558,
            "unit": "iter/sec",
            "range": "stddev: 0.000004080808843173831",
            "extra": "mean: 48.29204000088794 usec\nrounds: 5"
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
          "id": "c43ff4fb08196e1979a4762a0bc879af0029e3cf",
          "message": "Use tagged gh-action-pypi-publish",
          "timestamp": "2023-05-27T17:33:11+10:00",
          "tree_id": "c19eea16cbb3f06253307454066847957345e71e",
          "url": "https://github.com/limx0/betfair_parser/commit/c43ff4fb08196e1979a4762a0bc879af0029e3cf"
        },
        "date": 1685172841271,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.15137492148052242,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.606114079000008 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 549865.9701693594,
            "unit": "iter/sec",
            "range": "stddev: 9.689931162135926e-8",
            "extra": "mean: 1.8186250000013615 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15896.94708631668,
            "unit": "iter/sec",
            "range": "stddev: 0.000008980350460657953",
            "extra": "mean: 62.90516000149183 usec\nrounds: 5"
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
          "id": "3821dd09cf15f445fd03c816eb1df4ae5771700a",
          "message": "Add description",
          "timestamp": "2023-05-27T17:38:49+10:00",
          "tree_id": "6b6bc11efd2c1f4f4a9379ce2aee09f68d82621f",
          "url": "https://github.com/limx0/betfair_parser/commit/3821dd09cf15f445fd03c816eb1df4ae5771700a"
        },
        "date": 1685173174072,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.19034146370646024,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.2537160349999965 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 603586.8875141016,
            "unit": "iter/sec",
            "range": "stddev: 2.562240526947655e-8",
            "extra": "mean: 1.6567622999872356 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20545.79493298261,
            "unit": "iter/sec",
            "range": "stddev: 0.000006653805917086897",
            "extra": "mean: 48.67176000061591 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "committer": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "distinct": true,
          "id": "f2d4ae1a84c2f6895c38d7eb9dc0df5840485c71",
          "message": "Add test pypi workflow",
          "timestamp": "2023-05-28T11:42:13+10:00",
          "tree_id": "96f6954db8abb74ec291f7f30585294d7a91f3ef",
          "url": "https://github.com/limx0/betfair_parser/commit/f2d4ae1a84c2f6895c38d7eb9dc0df5840485c71"
        },
        "date": 1685238189969,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.1705399574174583,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.863728449000007 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 621505.4303425478,
            "unit": "iter/sec",
            "range": "stddev: 3.058498805657633e-8",
            "extra": "mean: 1.6089963999974088 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18290.71109827465,
            "unit": "iter/sec",
            "range": "stddev: 0.000007387152578027968",
            "extra": "mean: 54.672560002018145 usec\nrounds: 5"
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
          "id": "413eb46a978b066c9665a4c07ac294e2aadf8cef",
          "message": "Test ci",
          "timestamp": "2023-05-25T14:18:40Z",
          "url": "https://github.com/limx0/betfair_parser/pull/17/commits/413eb46a978b066c9665a4c07ac294e2aadf8cef"
        },
        "date": 1685239514309,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.17089308554244242,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.851611824000003 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 606307.3180217852,
            "unit": "iter/sec",
            "range": "stddev: 2.880433914569084e-8",
            "extra": "mean: 1.6493285999956697 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18433.533103986712,
            "unit": "iter/sec",
            "range": "stddev: 0.000005452710227507421",
            "extra": "mean: 54.248959999085855 usec\nrounds: 5"
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
          "id": "aef570299c91ef194e02a5a933fc329759a976f0",
          "message": "Test ci",
          "timestamp": "2023-05-25T14:18:40Z",
          "url": "https://github.com/limx0/betfair_parser/pull/17/commits/aef570299c91ef194e02a5a933fc329759a976f0"
        },
        "date": 1685239971608,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.15095084438031942,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.624673112000011 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 609306.1027125249,
            "unit": "iter/sec",
            "range": "stddev: 2.7871230866971728e-8",
            "extra": "mean: 1.6412111999997592 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18282.63193861891,
            "unit": "iter/sec",
            "range": "stddev: 0.000006421969574554501",
            "extra": "mean: 54.69671999946968 usec\nrounds: 5"
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
          "id": "2a6c776d14e30fcc61a1337a808ffd71ad1d899e",
          "message": "Test ci",
          "timestamp": "2023-05-25T14:18:40Z",
          "url": "https://github.com/limx0/betfair_parser/pull/17/commits/2a6c776d14e30fcc61a1337a808ffd71ad1d899e"
        },
        "date": 1685240004225,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.14646550546560352,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.827546163999983 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 532982.673375845,
            "unit": "iter/sec",
            "range": "stddev: 3.991046233726659e-8",
            "extra": "mean: 1.8762335999895183 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15187.062080951018,
            "unit": "iter/sec",
            "range": "stddev: 0.000007561490249284171",
            "extra": "mean: 65.8455200004937 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "bradley.mcelroy@live.com",
            "name": "Brad",
            "username": "limx0"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a3bc4d43ae3435ca3744f35486226e384eecd8a8",
          "message": "Test ci (#17)\n\n* Add twine\r\n\r\n* Only run on tags\r\n\r\n* Run builds and testpypi on all events\r\n\r\n* Don't upload to testpypi\r\n\r\n* Merge jobs\r\n\r\n* Only update testpypi on tags\r\n\r\n---------\r\n\r\nCo-authored-by: brad <brad@edgestackers.com>",
          "timestamp": "2023-05-28T12:22:58+10:00",
          "tree_id": "8041062c3aa08fe4ca978d15b1b1d11b7ed55173",
          "url": "https://github.com/limx0/betfair_parser/commit/a3bc4d43ae3435ca3744f35486226e384eecd8a8"
        },
        "date": 1685240621708,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.17179888741545918,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 5.8207594649999805 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 600657.6720987527,
            "unit": "iter/sec",
            "range": "stddev: 2.8862121965922653e-8",
            "extra": "mean: 1.6648417999988396 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18387.51767027902,
            "unit": "iter/sec",
            "range": "stddev: 0.0000055147747742640484",
            "extra": "mean: 54.38472000037109 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "committer": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "distinct": true,
          "id": "cfb4a62b4de23959a60b056c52f8a97d36cfedc2",
          "message": "Release 0.2.5",
          "timestamp": "2023-05-28T12:25:56+10:00",
          "tree_id": "8041062c3aa08fe4ca978d15b1b1d11b7ed55173",
          "url": "https://github.com/limx0/betfair_parser/commit/cfb4a62b4de23959a60b056c52f8a97d36cfedc2"
        },
        "date": 1685240855453,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.15820035165359528,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.3210984649999915 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 628019.2811973185,
            "unit": "iter/sec",
            "range": "stddev: 3.1919963817215384e-8",
            "extra": "mean: 1.5923077999985935 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 18433.53310360041,
            "unit": "iter/sec",
            "range": "stddev: 0.0000069080389996535735",
            "extra": "mean: 54.24896000022272 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "committer": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "distinct": true,
          "id": "b5ee7f51b80bdda16426c3adfd347559bc764603",
          "message": "Fix workflow",
          "timestamp": "2023-05-28T12:27:44+10:00",
          "tree_id": "8a482527a2ad9594ef62ba36296a380c0479c40f",
          "url": "https://github.com/limx0/betfair_parser/commit/b5ee7f51b80bdda16426c3adfd347559bc764603"
        },
        "date": 1685240918531,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.14622309993801208,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 6.838864724000018 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 524494.4411248023,
            "unit": "iter/sec",
            "range": "stddev: 4.547147441538345e-8",
            "extra": "mean: 1.906597899980511 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 15660.264959014137,
            "unit": "iter/sec",
            "range": "stddev: 0.000007265563417477799",
            "extra": "mean: 63.85588000057396 usec\nrounds: 5"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "committer": {
            "email": "brad@edgestackers.com",
            "name": "brad"
          },
          "distinct": true,
          "id": "563db8a282ec8f3682df0754b5ee51e757aa791d",
          "message": "Release 0.2.5",
          "timestamp": "2023-05-28T12:28:27+10:00",
          "tree_id": "8a482527a2ad9594ef62ba36296a380c0479c40f",
          "url": "https://github.com/limx0/betfair_parser/commit/563db8a282ec8f3682df0754b5ee51e757aa791d"
        },
        "date": 1685240965521,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/integration/benchmark.py::test_performance",
            "value": 0.13716980021372782,
            "unit": "iter/sec",
            "range": "stddev: 0",
            "extra": "mean: 7.290234427999998 sec\nrounds: 1"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_update_performance",
            "value": 624408.5290199879,
            "unit": "iter/sec",
            "range": "stddev: 3.851037656738836e-8",
            "extra": "mean: 1.6015156000023012 usec\nrounds: 100"
          },
          {
            "name": "tests/integration/benchmark.py::test_market_definition_performance",
            "value": 20156.348766232135,
            "unit": "iter/sec",
            "range": "stddev: 0.00000858317407581004",
            "extra": "mean: 49.612159999696814 usec\nrounds: 5"
          }
        ]
      }
    ]
  }
}