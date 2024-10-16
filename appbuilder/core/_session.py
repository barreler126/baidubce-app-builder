# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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

import requests
import json
from appbuilder.utils.logger_util import logger
from appbuilder.utils.trace.tracer_wrapper import session_post


class InnerSession(requests.sessions.Session):

    def __init__(self, *args, **kwargs):
        """
        Initialize inner session.
        """
        super(InnerSession, self).__init__(*args, **kwargs)

    def build_curl(self, request: requests.PreparedRequest) -> str:
        """
        Generate cURL command from prepared request object.
        """
        curl = "curl -X {0} -L '{1}' \\\n".format(request.method, request.url)

        headers = [
            "-H '{0}: {1}' \\".format(k, v)
            for k, v in request.headers.items()
            if k != "Content-Length"
        ]

        if headers:
            headers[-1] = headers[-1].rstrip(" \\")
        curl += "\n".join(headers)
        if request.body:
            try:
                body = json.loads(request.body)
                body = "'{0}'".format(json.dumps(body, ensure_ascii=False))
                curl += " \\\n-d {0}".format(body)
            except:
                curl += " \\\n-d '{0}'".format(request.body)
        return curl

    def send(self, request, **kwargs):
        """
        Send request using inner session.
        """
        logger.debug("Curl Command:\n" + self.build_curl(request) + "\n")
        return super(InnerSession, self).send(request, **kwargs)

    @session_post
    def post(self, url, data=None, json=None, **kwargs):
        return super().post(url=url, data=data, json=json, allow_redirects=False, **kwargs)

    @session_post
    def delete(self, url, **kwargs):
        return super().delete(url=url, allow_redirects=False, **kwargs)

    @session_post
    def get(self, url, **kwargs):
        return super().get(url=url, allow_redirects=False, **kwargs)

    @session_post
    def put(self, url, data=None, **kwargs):
        return super().put(url=url, data=data, allow_redirects=False, **kwargs)
