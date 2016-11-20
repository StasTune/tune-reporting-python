#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_advertiser_report_cohort_retention.py
#
#  Copyright (c) 2016 TUNE, Inc.
#  All rights reserved.
#
#  Python 2.7 and 3.0
#
#  @category  Tune_Reporting
#  @package   Tune_Reporting_Python
#  @author    Jeff Tanner <jefft@tune.com>
#  @copyright 2016 TUNE, Inc. (http://www.tune.com)
#  @license   http://opensource.org/licenses/MIT The MIT License (MIT)
#  @link      https://developers.tune.com @endlink
#

import datetime
import os.path
import sys
import unittest

try:
    from tune_reporting import (
        AdvertiserReportCohortRetention,
        SdkConfig,
        TUNE_FIELDS_RECOMMENDED
        )
except ImportError as exc:
    sys.stderr.write("Error: failed to import module ({})".format(exc))
    raise


class TestAdvertiserReportCohortRetention(unittest.TestCase):

    def __init__(self, api_key):
        # Setup TUNE Reporting SDK configuration.
        dirname = os.path.split(__file__)[0]
        dirname = os.path.dirname(dirname)
        filepath = os.path.join(dirname, "config", SdkConfig.SDK_CONFIG_FILENAME)

        abspath = os.path.abspath(filepath)

        sdk_config = SdkConfig(filepath=abspath)
        sdk_config.set_api_key(api_key)
        unittest.TestCase.__init__(self)

    def setUp(self):
        week_ago = datetime.date.fromordinal(datetime.date.today().toordinal() - 8)
        yesterday = datetime.date.fromordinal(datetime.date.today().toordinal() - 1)
        self.__start_date = "{} 00:00:00".format(week_ago)
        self.__end_date = "{} 23:59:59".format(yesterday)

    def test_ApiKey(self):
        sdk_config = SdkConfig()
        api_key = sdk_config.auth_key

        self.assertIsNotNone(api_key)
        self.assertGreater(len(api_key), 0)
        self.assertNotEqual("API_KEY", api_key)
        self.assertEqual("api_key", sdk_config.auth_type)

    def test_Fields(self):
        response = None
        advertiser_report = AdvertiserReportCohortRetention()
        response = advertiser_report.fields(TUNE_FIELDS_RECOMMENDED)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)

    def test_Count(self):
        response = None

        try:
            advertiser_report = AdvertiserReportCohortRetention()

            map_params = {
                "start_date": self.__start_date,
                "end_date": self.__end_date,
                "cohort_type": "install",
                "cohort_interval": "year_day",
                "retention_measure": "rolling_opens",
                "filter": "(install_publisher_id > 0)",
                "group": "site_id,install_publisher_id",
                "response_timezone": "America/Los_Angeles"
            }

            response = advertiser_report.count(
                map_params
            )
        except Exception as exc:
            self.fail("Exception: {0}".format(exc))

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.http_code, 200)
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, int)
        self.assertGreaterEqual(response.data, 0)

    def test_Find(self):
        response = None

        try:
            advertiser_report = AdvertiserReportCohortRetention()

            map_params = {
                "start_date": self.__start_date,
                "end_date": self.__end_date,
                "cohort_type": "install",
                "cohort_interval": "year_day",
                "retention_measure": "rolling_opens",
                "filter": "(install_publisher_id > 0)",
                "group": "site_id,install_publisher_id",
                "fields": advertiser_report.fields(TUNE_FIELDS_RECOMMENDED),
                "limit": 5,
                "page": None,
                "sort": {"year_day": "ASC", "install_publisher_id": "ASC"},
                "response_timezone": "America/Los_Angeles"
            }

            response = advertiser_report.find(
                map_params
            )
        except Exception as exc:
            self.fail("Exception: {0}".format(exc))

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.http_code, 200)
        self.assertIsNone(response.errors)
        self.assertIsInstance(response.data, list)
        self.assertLessEqual(len(response.data), 10)

    def test_Export(self):
        response = None

        try:
            advertiser_report = AdvertiserReportCohortRetention()

            map_params = {
                "start_date": self.__start_date,
                "end_date": self.__end_date,
                "cohort_type": "install",
                "cohort_interval": "year_day",
                "retention_measure": "rolling_opens",
                "filter": "(install_publisher_id > 0)",
                "group": "site_id,install_publisher_id",
                "fields": advertiser_report.fields(TUNE_FIELDS_RECOMMENDED),
                "response_timezone": "America/Los_Angeles"
            }

            response = advertiser_report.export(
                map_params
            )
        except Exception as exc:
            self.fail("Exception: {0}".format(exc))

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.http_code, 200)
        self.assertIsNone(response.errors)

    def runTest(self):
        self.test_ApiKey()
        self.test_Fields()
        self.test_Count()
        self.test_Find()
        self.test_Export()