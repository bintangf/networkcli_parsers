#!/usr/bin/python

# pylint: disable=wrong-import-position, missing-docstring, global-statement

DOCUMENTATION = '''
---
module: textfsm_parse_command
author:  NIS-E
short_description: Module for using textFSM to parse network CLI output.
description:
    - Module for using textFSM to parse network CLI output.
    - Disclaimer: this custom build parsers is a working progress.
options:
    device_name:
        description:
            - Device name or hostname
        required: true
    device_os:
        description:
            - Device OS (IOS, IOSXE, ASA, NXOS, etc)
        required: true
    cli_command:
        description:
            - CLI command used to get the output (show interfaces, show version, etc)
        required: true
    cli_result:
        description:
            - output from the previously executed CLI command
        required: true
'''

EXAMPLES = '''
- name: get show interfaces output from IOS device
  asa_command:
    commands:
    - term pager 0
    - show failover
  register: config

- name: parse with textfsm parsers
  textfsm_parse_command:
    device_name: firewall01
    device_os: asa
    cli_command: show failover
    cli_result: "{{ config.stdout[1] }}"
  register: parsed

- debug: msg="{{ parsed }}"
'''

RETURN = '''
message:
    description: success/error message
    type: str
parsed_cli:
    description: parsed cli output in JSON/dictionary format
    type: dict
'''



from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.textfsm_parse import parse


def main():
    """ Process the module """
    # Manage the parameters
    module = AnsibleModule(
        argument_spec=dict(
            device_name=dict(type="str", required=True),
            device_os=dict(type="str", required=True),
            cli_command=dict(type="str", required=True),
            cli_result=dict(type="str", required=True)
        ),
        supports_check_mode=False,
    )

    # Manage the result, assume no changes
    result = dict(
        failed=False,
        message='',
        parsed_cli={}
    )

    # assign parameters to local variables
    device_name = module.params["device_name"]
    device_os = module.params["device_os"]
    cli_command = module.params["cli_command"]
    cli_result = module.params["cli_result"]
    
    try:
        result["failed"] = False
        result["parsed_cli"] = parse(device_name, device_os, cli_command, cli_result)
        result["message"] = "parsing success"
    except Exception as e:
        result["failed"] = True
        result["message"] = e
        result["parsed_cli"] = {}


    # exit with change state indicated
    module.exit_json(**result)

    

if __name__ == "__main__":
    main()