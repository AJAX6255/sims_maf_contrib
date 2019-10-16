# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:11:20 2018

@author: rstreet
"""

import lsst.sims.maf.db as db
import lsst.sims.maf.metrics as metrics
import lsst.sims.maf.slicers as slicers
import lsst.sims.maf.metricBundles as metricBundles
from lsst.sims.maf.metrics import BaseMetric
import numpy as np
import calculate_lsst_field_visibility_astropy

class CalcExpectedVisitsMetric(BaseMetric):
    """Function to calculate the maximum possible number of visits to a
    given pointing, given the expected cadence of observation and within
    the date ranges given, taking target visibility into account.

    Input:
    :param array ra:            RAs, J2000.0, sexigesimal format
    :param array dec:           Decs, J2000.0, sexigesimal format
    :param float cadence:       Interval between successive visits in the
                                same single filter in hours
    :param string start_date:   Start of observing window YYYY-MM-DD
    :param string start_date:   End of observation window YYYY-MM-DD

    Output:
    :param list of arrays n_visits:       Number of visits possible per night
                                          for each pointing
    :param list of arrays hrs_visibility: Hours of visibility per night
                                          for each pointing
    """

    def __init__(self, metricName='CalcExpectedVisitsMetric',
                pointings,cadence,start_date,end_date,verbose=False):
        """Input:
            :param array ra:            RAs, J2000.0, sexigesimal format
            :param array dec:           Decs, J2000.0, sexigesimal format
            :param float cadence:       Interval between successive visits in the
                                        same single filter in hours
            :param string start_date:   Start of observing window YYYY-MM-DD
            :param string start_date:   End of observation window YYYY-MM-DD

            Output:
            :param list of arrays n_visits:       Number of visits possible per night
                                                  for each pointing
            :param list of arrays hrs_visibility: Hours of visibility per night
                                                  for each pointing
        """

        self.pointings = pointings
        self.cadence = cadence
        self.start_date = start_date
        self.end_date = end_date

        if len(self.filters) != len(self.cadence):
            raise ValueError('ERROR: The list of filters requested must correspond to the list of required cadences')
            exit()

        cols = [ ra_col, dec_col, visittime_col, filterCol ]

        super(CalcExpectedVisitsMetric,self).__init__(col=cols, metricName=metricName)

    def run(self, dataSlice, slicePoint=None, verbose=False):
        n_visits = []
        hrs_visibility = []

        if verbose:
            print('Calculating visbility for '+str(len(self.pointings))+' fields')

        for i in range(0,len(self.pointings),1):

            (ra, dec) = pointings[i]

            if verbose:
                print(' -> RA '+str(ra)+', Dec '+str(dec))

            (total_time_visible, hrs_visible_per_night) = calculate_lsst_field_visibility_astropy.calculate_lsst_field_visibility(ra,dec,self.start_date,self.end_date,verbose=False)

            n_visits.append( (np.array(hrs_visible_per_night) / self.cadence).astype(int) )
            hrs_visibility.append( np.array(hrs_visible_per_night) )

        return n_visits,hrs_visibility
