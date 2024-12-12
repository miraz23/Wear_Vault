import pytest

from apimatic_core.utilities.comparison_helper import ComparisonHelper


class TestComparisonHelper:

    @pytest.mark.parametrize('input_expected_headers, input_received_headers, '
                             'input_should_allow_extra, expected_output',
                             [
                                 ({}, {}, False,
                                  True),
                                 ({'content-type': 'application/json'}, {'content-type': 'application/json'}, False,
                                  True),
                                 ({'content-type': 'APPLICATION/JSON'}, {'content-type': 'application/json'}, False,
                                  False),
                                 ({'content-type': 'application/json'}, {'CONTENT-TYPE': 'application/json'}, False,
                                  True),
                                 ({'content-type': 'application/json'}, {'content-type': 'APPLICATION/JSON'}, False,
                                  False),
                                 ({'content-type': 'application/json', 'accept': 'application/json'},
                                  {'content-type': 'application/json'}, False, False),
                                 ({'content-type': 'application/json', 'accept': 'application/json'},
                                  {'content-type': 'application/json'}, True, False),
                                 ({'content-type': 'application/json'}, {'Connection': 'close'}, True, False),
                                 ({'content-type': 'application/json'},
                                  {'content-type': 'application/json', 'accept': 'application/json'}, True, True)
                             ])
    def test_match_headers(self, input_expected_headers, input_received_headers,
                           input_should_allow_extra, expected_output):
        actual_output = ComparisonHelper.match_headers(input_expected_headers, input_received_headers
                                                       , input_should_allow_extra)
        assert actual_output is expected_output

    @pytest.mark.parametrize('input_expected_body, input_received_body, input_check_values, '
                             'input_check_order, input_check_count, expected_output',
                             [
                                 ([100, 500, 300, 200, 400], '[100, 500, 300, 200, 400]', True, True, True, False),  # 0
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200, 400], True, True, True, True),  # 1
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200, 400], True, True, False, True),  # 2
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200, 400], True, False, True, True),  # 3
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200, 400], True, False, False, True),  # 4
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200, 400], False, True, True, True),  # 5
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200, 400], False, True, False, True),  # 6
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200, 400], False, False, True, True),  # 7
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200, 400], False, False, False, True),  # 8

                                 ([101, 500, 300, 200, 400], [100, 500, 300, 200, 400], True, True, True, False),  # 9
                                 ([101, 500, 300, 200, 400], [100, 500, 300, 200, 400], True, True, False, False),  # 10
                                 ([101, 500, 300, 200, 400], [100, 500, 300, 200, 400], True, False, True, False),  # 11
                                 ([101, 500, 300, 200, 400], [100, 500, 300, 200, 400], True, False, False, False),  # 12
                                 ([101, 500, 300, 200, 400], [100, 500, 300, 200, 400], False, True, True, False),  # 13
                                 ([101, 500, 300, 200, 400], [100, 500, 300, 200, 400], False, True, False, False),  # 14
                                 ([101, 500, 300, 200, 400], [100, 500, 300, 200, 400], False, False, True, False),  # 15
                                 ([101, 500, 300, 200, 400], [100, 500, 300, 200, 400], False, False, False, False),  # 16

                                 ([100, 500, 300, 200, 400], [101, 500, 300, 200, 400], True, True, True, False),  # 17
                                 ([100, 500, 300, 200, 400], [101, 500, 300, 200, 400], True, True, False, False),  # 18
                                 ([100, 500, 300, 200, 400], [101, 500, 300, 200, 400], True, False, True, False),  # 19
                                 ([100, 500, 300, 200, 400], [101, 500, 300, 200, 400], True, False, False, False),  # 20
                                 ([100, 500, 300, 200, 400], [101, 500, 300, 200, 400], False, True, True, False),  # 21
                                 ([100, 500, 300, 200, 400], [101, 500, 300, 200, 400], False, True, False, False),  # 22
                                 ([100, 500, 300, 200, 400], [101, 500, 300, 200, 400], False, False, True, False),  # 23
                                 ([100, 500, 300, 200, 400], [101, 500, 300, 200, 400], False, False, False, False),  # 24

                                 ([100, 500, 300, 200, 400], [500, 100, 300, 200, 400], True, True, True, False),  # 25
                                 ([100, 500, 300, 200, 400], [500, 100, 300, 200, 400], True, True, False, False),  # 26
                                 ([100, 500, 300, 200, 400], [500, 100, 300, 200, 400], True, False, True, True),  # 27
                                 ([100, 500, 300, 200, 400], [500, 100, 300, 200, 400], True, False, False, True),  # 28
                                 ([100, 500, 300, 200, 400], [500, 100, 300, 200, 400], False, True, True, False),  # 29
                                 ([100, 500, 300, 200, 400], [500, 100, 300, 200, 400], False, True, False, False),  # 30
                                 ([100, 500, 300, 200, 400], [500, 100, 300, 200, 400], False, False, True, True),  # 31
                                 ([100, 500, 300, 200, 400], [500, 100, 300, 200, 400], False, False, False, True),  # 32

                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200], True, True, True, False),  # 33
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200], True, True, False, False),  # 34
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200], True, False, True, False),  # 35
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200], True, False, False, False),  # 36
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200], False, True, True, False),  # 37
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200], False, True, False, False),  # 38
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200], False, False, True, False),  # 39
                                 ([100, 500, 300, 200, 400], [100, 500, 300, 200], False, False, False, False),  # 40

                                 ([100, 500, 300, 200], [100, 500, 300, 200, 400], True, True, True, False),  # 41
                                 ([100, 500, 300, 200], [100, 500, 300, 200, 400], True, True, False, True),  # 42
                                 ([100, 500, 300, 200], [100, 500, 300, 200, 400], True, False, True, False),  # 43
                                 ([100, 500, 300, 200], [100, 500, 300, 200, 400], True, False, False, True),  # 44
                                 ([100, 500, 300, 200], [100, 500, 300, 200, 400], False, True, True, False),  # 45
                                 ([100, 500, 300, 200], [100, 500, 300, 200, 400], False, True, False, True),  # 46
                                 ([100, 500, 300, 200], [100, 500, 300, 200, 400], False, False, True, False),  # 47
                                 ([100, 500, 300, 200], [100, 500, 300, 200, 400], False, False, False, True),  # 48

                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, 'Not a dictionary', True, True, True, False),  # 49
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, True, True),  # 50
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, False, True),  # 51
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, True, True),  # 52
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, False, True),  # 53
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, True, True),  # 54
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, False, True),  # 55
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, True, True),  # 56
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, False, True),  # 57

                                 ({
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, True, False),  # 58
                                 ({
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, False, False),  # 59
                                 ({
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, True, False),  # 60
                                 ({
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, False, False),  # 61
                                 ({
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, True, False),  # 62
                                 ({
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, False, False),  # 63
                                 ({
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, True, False),  # 64
                                 ({
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, False, False),  # 65

                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, True, False),  # 66
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, False, False),  # 67
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, True, False),  # 68
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, False, False),  # 69
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, True, False),  # 70
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, False, False),  # 71
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, True, False),  # 72
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "changed-id": "file",
                                          "changed-value": "File",
                                          "changed-popup": {
                                              "changed-menuitem": [
                                                  {
                                                      "changed-value": "New",
                                                      "changed-onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Open",
                                                      "changed-onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "changed-value": "Save",
                                                      "changed-onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, False, False),  # 73

                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, True, True),  # 74 [suspicious]
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, False, True),  # 75 [suspicious]
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, True, True),  # 76
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, False, True),  # 77
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, True, True),  # 78 [suspicious]
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, False, True),  # 79 [suspicious]
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, True, True),  # 80
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, False, True),  # 81

                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, True, False),  # 82
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, False, False),  # 83
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, True, False),  # 84
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, False, False),  # 85
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, True, True),  # 86 [suspicious]
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, False, True),  # 87 [suspicious]
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, True, True),  # 88 [suspicious]
                                 ({
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, False, True),  # 89 [suspicious]

                                 ({
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, True, False),  # 90
                                 ({
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, True, False, True),  # 91
                                 ({
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, True, False),  # 92
                                 ({
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, True, False, False, True),  # 93
                                 ({
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, True, True),  # 94 [suspicious]
                                 ({
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, True, False, True),  # 95
                                 ({
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, True, True),  # 96 [suspicious]
                                 ({
                                      "menu": {
                                          "value": "File",
                                          "id": "file",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, {
                                      "menu": {
                                          "id": "file",
                                          "value": "File",
                                          "popup": {
                                              "menuitem": [
                                                  {
                                                      "value": "New",
                                                      "onclick": "CreateDoc()"
                                                  },
                                                  {
                                                      "value": "Open",
                                                      "onclick": "OpenDoc()"
                                                  },
                                                  {
                                                      "value": "Save",
                                                      "onclick": "SaveDoc()"
                                                  }
                                              ]
                                          }
                                      }
                                  }, False, False, False, True)  # 97
                             ])
    def test_match_body(self, input_expected_body, input_received_body, input_check_values, input_check_order,
                        input_check_count, expected_output):
        actual_output = ComparisonHelper.match_body(input_expected_body, input_received_body, input_check_values,
                                                    input_check_order, input_check_count)
        assert actual_output is expected_output
