#!/usr/bin/env python

from distutils.version import LooseVersion
from ansible.module_utils.basic import *
import uuid

import logging

def main():

    module = AnsibleModule(
        argument_spec = dict(),
        supports_check_mode = True
    )

    args = module.params

    facts = []
    for y in range(0,100): 
        f = {}
        for i in range(0,5): 
            u = str(uuid.uuid4())
            f[u] = [ u ]

        facts.append(f)
    
    resp = {
        'changed': False,
        'ansible_facts': {
            'uuid': facts
        }
    }

    module.exit_json(**resp)

if __name__ == "__main__":
    main()