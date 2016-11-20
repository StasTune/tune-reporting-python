#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2016 TUNE, Inc. (http://www.tune.com)
#  @namespace tune_reporting
"""TUNE Advertisers.
"""

import logging

from pyhttpstatus_utils import (
    HttpStatusType,
    is_http_status_type
)
from requests_mv_integrations.errors import (
    get_exception_message,
    print_traceback
)
from tune_reporting.errors import (
    TuneReportingError
)
from requests_mv_integrations.support import (
    python_check_version
)
from tune_reporting import (
    __python_required_version__
)
from tune_reporting.tmc.tune_mobileapptracking_api_base import (
    TuneMobileAppTrackingApiBase
)
from logging_mv_integrations import (
    TuneLoggingFormat
)

python_check_version(__python_required_version__)


# @brief TUNE Advertisers.
#
# @namespace tune_reporting.TuneV2AdvertiserStatus
class TuneV2AdvertiserStatus(object):
    """Status states for Advertisers.
    """
    ACTIVE = 1
    NOT_ACTIVE = 2
    ALL = 3


#   TUNE MobileAppTracking: Advertisers
#
class TuneV2Advertisers(TuneMobileAppTrackingApiBase):
    """TUNE Advertisers.
    """

    #  Advertiser ID
    #  @var str
    __advertiser_id = None

    # Initialize Job
    #
    def __init__(
        self,
        logger_level=logging.NOTSET,
        logger_format=TuneLoggingFormat.JSON
    ):
        super(TuneV2Advertisers, self).__init__(
            logger_level=logger_level,
            logger_format=logger_format
        )

    @property
    def advertiser_id(self):
        """Get Property: advertiser_id
        """
        return self.__advertiser_id

    @advertiser_id.setter
    def advertiser_id(self, value):
        """Set Property: advertiser_id
        """
        self.__advertiser_id = value

    # Collect Advertisers
    #
    def get_advertiser_id(
        self,
        auth_type,
        auth_value,
        request_retry=None
    ):
        """Get Advertiser ID

        Args:
            auth_type:
            auth_value:
            request_retry:

        Returns:

        """
        if not auth_type:
            raise ValueError(
                "TMC v2 Advertisers: Get Advertiser ID: Value 'auth_type' not provided."
            )
        if not auth_value:
            raise ValueError(
                "TMC v2 Advertisers: Get Advertiser ID: Value 'auth_value' not provided."
            )

        request_url = \
            self.tune_mat_request_path(
                mat_api_version="v2",
                controller="advertiser",
                action="find"
            )

        request_params = \
            {
                auth_type: auth_value,
                "source": "multiverse",
            }

        self.logger.info(
            "TMC v2 Advertisers: Advertiser ID"
        )

        try:
            response = self.request_mv_integration.request(
                request_method="GET",
                request_url=request_url,
                request_params=request_params,
                request_retry=None,
                request_retry_http_status_codes=None,
                request_retry_func=self.tune_v2_request_retry_func,
                request_retry_excps_func=None,
                request_label="TMC v2 Advertisers"
            )

        except TuneReportingError as tmv_ex:
            self.logger.error(
                "TMC v2 Advertisers: Advertiser ID: Failed",
                extra={
                    'error': str(tmv_ex)
                }
            )
            raise

        except Exception as ex:
            print_traceback(ex)

            self.logger.error(
                "TMC v2 Advertisers: Advertiser ID: Failed",
                extra={
                    'error': get_exception_message(ex)
                }
            )

            raise TuneReportingError(
                error_message=(
                    "TMC v2 Advertisers: Failed: {}"
                ).format(
                    get_exception_message(ex)
                ),
                errors=ex
            )

        json_response = self.request_mv_integration.validate_json_response(
            response,
            request_label="TMC v2 Advertisers: Advertiser ID:"
        )

        self.logger.debug(
            "TMC v2 Advertisers: Advertiser ID",
            extra={
                'response': json_response
            }
        )

        json_response_status_code = json_response['status_code']

        http_status_successful = is_http_status_type(
            http_status_code=json_response_status_code,
            http_status_type=HttpStatusType.SUCCESSFUL
        )

        if not http_status_successful or not json_response['data']:
            raise TuneReportingError(
                error_message="TMC v2 Advertisers: Failed: {}".format(
                    json_response_status_code
                )
            )

        if 'data' not in json_response or \
                not json_response['data'] or \
                len(json_response['data']) == 0:
            raise TuneReportingError(
                error_message="TMC v2 Advertisers: Advertiser ID: Failed"
            )

        advertiser_data = json_response['data'][0]
        self.advertiser_id = advertiser_data['id']

        self.logger.info(
            "TMC v2 Advertisers: Advertiser ID: {}".format(
                self.advertiser_id
            )
        )

        self.logger.info(
            "TMC v2 Advertisers: Finished"
        )

        return True