import logging
import random

from datetime import datetime

import cms50dplus


def read_simulated_cms50plus(q, port):
    logging.info("Simulating cms50plus. I was passed in port {}".format(port))
    while True:
        q.put(
            cms50dplus.LiveDataPoint(
                datetime.now(),
                random.choice(
                    [[135, 35, 4, 70, 98], [199, 64, 8, 76, 98], [144, 40, 53, 0, 0], [198, 68, 8, 84, 97],
                     [199, 59, 7, 85, 97], [199, 66, 8, 86, 97], [134, 85, 10, 106, 97], [198, 69, 8, 107, 97],
                     [198, 76, 9, 110, 97], [134, 75, 9, 109, 96]]
                )
            )
        )


def read_cms50dplus(q, port):
    logging.info("Connecting to cms50dplus")
    oximeter = cms50dplus.CMS50Dplus(port)
    for data in oximeter.getLiveData():
        q.put(data)
