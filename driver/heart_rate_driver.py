import logging

from datetime import datetime

import cms50dplus


def read_simulated_cms50plus(q, port):
    logging.info("Simulating cms50plus. I was passed in port {}".format(port))
    while True:
        q.put(
            cms50dplus.LiveDataPoint(
                datetime.now(),
                [134, 40, 5, 86, 98]
            )
        )


def read_cms50dplus(q, port):
    logging.info("Connecting to cms50dplus")
    oximeter = cms50dplus.CMS50Dplus(port)
    for data in oximeter.getLiveData():
        q.put(data)
