# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.utils.translation import ugettext_lazy as _

from auth_backend.resources.base import Action
from auth_backend.resources.django import DjangoModelResource
from auth_backend.resources.inspect import FixedCreatorFieldInspect
from auth_backend.backends import get_backend_from_config

from gcloud.taskflow3.models import TaskFlowInstance
from gcloud.core.permissions import project_resource

taskflow_resource = DjangoModelResource(
    rtype='flow-instance',
    name=_(u"流程实例"),
    scope_type='system',
    scope_id='bk_sops',
    scope_name=_(u"标准运维"),
    actions=[
        Action(id='view', name=_(u"查看"), is_instance_related=True),
        Action(id='edit', name=_(u"编辑"), is_instance_related=True),
        Action(id='operate', name=_(u"控制"), is_instance_related=True),
        Action(id='claim', name=_(u"认领"), is_instance_related=True),
        Action(id='delete', name=_(u"删除"), is_instance_related=True),
        Action(id='clone', name=_(u"克隆"), is_instance_related=True)
    ],
    operations=[
        {
            'operate_id': 'view',
            'actions_id': ['view']
        },
        {
            'operate_id': 'edit',
            'actions_id': ['view', 'edit']
        },
        {
            'operate_id': 'operate',
            'actions_id': ['view', 'operate']
        },
        {
            'operate_id': 'claim',
            'actions_id': ['view', 'claim']
        },
        {
            'operate_id': 'delete',
            'actions_id': ['view', 'delete']
        },
        {
            'operate_id': 'clone',
            'actions_id': ['view', 'clone']
        }
    ],
    parent=project_resource,
    resource_cls=TaskFlowInstance,
    tomb_field='is_deleted',
    backend=get_backend_from_config(),
    inspect=FixedCreatorFieldInspect(creator_type='user',
                                     creator_id_f='creator',
                                     resource_id_f='id',
                                     resource_name_f='name',
                                     parent_f='project'))
