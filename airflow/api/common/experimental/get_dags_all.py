# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from flask import url_for

from airflow.exceptions import AirflowException
from airflow.models import DagBag, DagRun
from airflow.utils.log.logging_mixin import LoggingMixin

from datetime import timedelta

_log = LoggingMixin().log

def get_dags_all(run_url_route='Airflow.graph'):
    dags = DagBag().dags
    dags_list = list()

    for key in dags:
        dag = dags[key]
        _log.info(dag.dag_id)

        tasks = list()
        for task_id in dag.task_ids:
            downstreams = list()
            for downstream_id in dag.get_task(task_id).downstream_task_ids:
                downstreams.append(downstream_id)

            upstreams = list()
            for upstream_id in dag.get_task(task_id).upstream_task_ids:
                upstreams.append(upstream_id)
            tasks.append({
                'name': task_id,
                'downstream': downstreams,
                'upstreams': upstreams
                })
        dags_list.append({
            'dag_id': dag.dag_id,
            'schedule_interval': str(dag.schedule_interval),
            'description': dag.description,
            'paused': (dag.is_paused==1 if True else False),
            'tasks': tasks
            })
#        for tag_id in dag.task_ids:
#            #_log.info(dag.get_task(tag_id).upstream_task_ids)
    return dags_list 

