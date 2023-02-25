window.BENCHMARK_DATA = {
  "lastUpdate": 1677285888426,
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
      }
    ]
  }
}