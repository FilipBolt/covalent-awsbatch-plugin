# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the GNU Affero General Public License 3.0 (the "License").
# A copy of the License may be obtained with this software package or at
#
#      https://www.gnu.org/licenses/agpl-3.0.en.html
#
# Use of this file is prohibited except in compliance with the License. Any
# modifications or derivative works of this file must retain this copyright
# notice, and modified files must contain a notice indicating that they have
# been altered from the originals.
#
# Covalent is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
#
# Relief from the License may be granted by purchasing a commercial license.

"""Docker and Python execution scripts."""

PYTHON_EXEC_SCRIPT = """
import os
import boto3
import cloudpickle as pickle

local_func_filename = os.path.join("{docker_working_dir}", "{func_filename}")
local_result_filename = os.path.join("{docker_working_dir}", "{result_filename}")

s3 = boto3.client("s3")
s3.download_file("{s3_bucket_name}", "{func_filename}", local_func_filename)

with open(local_func_filename, "rb") as f:
    function, args, kwargs = pickle.load(f)

result = function(*args, **kwargs)

with open(local_result_filename, "wb") as f:
    pickle.dump(result, f)

s3.upload_file(local_result_filename, "{s3_bucket_name}", "{result_filename}")
"""

DOCKER_SCRIPT = """
FROM amd64/python:3.8-slim-buster

RUN apt-get update && apt-get install -y \\
  gcc \\
  && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --use-feature=in-tree-build boto3 cloudpickle
RUN pip install covalent --pre

WORKDIR {docker_working_dir}

COPY {func_basename} {docker_working_dir}

ENTRYPOINT [ "python" ]
CMD ["{docker_working_dir}/{func_basename}"]
"""
