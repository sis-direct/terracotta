# Copyright 2012 Anton Beloglazov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" The functions from this module are shared by other components.
"""

from contracts import contract
from neat.contracts_extra import *

import time

from neat.config import *
from neat.db_utils import *


@contract
def start(init_state, execute, iterations, time_interval):
    """ Start the processing loop.

    :param init_state: A function accepting a config and returning a state dictionary.
     :type init_state: function

     :param execute: A function performing the processing at each iteration.
     :type execute: function

    :param iterations: The number of iterations to perform, -1 for infinite.
     :type iterations: int

    :param iterations: The time interval to wait between iterations.
     :type iterations: int

    :return: The final state.
     :rtype: dict(str: *)
    """
    config = read_config([DEFAILT_CONFIG_PATH, CONFIG_PATH])
    if not validate_config(config, REQUIRED_FIELDS):
        raise KeyError("The config dictionary does not contain all the required fields")
    state = init_state(config)

    if iterations == -1:
        while True:
            state = execute(config, state)
            time.sleep(time_interval)
    else:
        for _ in xrange(iterations):
            state = execute(config, state)
            time.sleep(time_interval)

    return state
