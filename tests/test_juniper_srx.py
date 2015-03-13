#!/usr/bin/env python2.7

"""This module runs tests against Juniper devices.

setup_module: setup variables for later use.
test_disable_paging: disable paging
test_verify_ssh: verify ssh connectivity
test_verify_send_command: send a command
test_base_prompt: test the base prompt
test_strip_prompt: test removing the prompt
test_strip_command: test stripping extraneous info after sending a command
test_normalize_linefeeds: ensure \n is the only line termination character in output
def test_clear_buffer: clear text buffer
"""

import netmiko
import time
from testutils import Utils
from os import path

def setup_module(module):
    """Setup variables for the tests."""
    pwd = path.dirname(path.realpath(__file__))
    responses = Utils.parse_yaml(pwd + "/etc/responses.yml")
    module.EXPECTED_RESPONSES = responses["juniper"]
    module.commands = Utils.parse_yaml(pwd + "/etc/commands.yml")
    module.commands = module.commands["juniper"]
    dispatcher = Utils.parse_yaml(pwd + "/etc/dispatchers.yml")
    dispatcher = dispatcher["juniper"]

    SSHClass = netmiko.ssh_dispatcher(dispatcher["device_type"])
    net_connect = SSHClass(**dispatcher)

    module.show_version = net_connect.send_command(module.commands["version"])
    module.multiple_line_output = net_connect.send_command(module.commands["multiline"],
                                                           delay_factor=2)
    module.show_ip = net_connect.send_command(module.commands["basic"])
    module.base_prompt = net_connect.base_prompt

    # Test buffer clearing
    net_connect.remote_conn.send(module.commands["version"])
    time.sleep(2)
    net_connect.clear_buffer()
    # Should not be anything there on the second pass
    module.clear_buffer_check = net_connect.clear_buffer()

def test_disable_paging():
    """Verify paging is disabled by looking for string after when paging would normally occur."""
    assert 'security-zone untrust' in multiple_line_output

def test_verify_ssh_connect():
    """Verify the connection was established successfully."""
    assert 'JUNOS Software Release' in show_version

def test_verify_send_command():
    """Verify a command can be sent down the channel successfully."""
    assert EXPECTED_RESPONSES['interface_ip'] in show_ip

def test_base_prompt():
    """Verify the router base_prompt is detected correctly."""
    assert base_prompt == EXPECTED_RESPONSES['base_prompt']

def test_strip_prompt():
    """Ensure the router prompt is not in the command output."""
    assert EXPECTED_RESPONSES['base_prompt'] not in show_version

def test_strip_command():
    """Ensure that the command that was executed does not show up in the command output."""
    assert commands["basic"] not in show_ip

def test_normalize_linefeeds():
    """Ensure no '\r' sequences."""
    assert not '\r' in show_ip

def test_clear_buffer():
    """Test that clearing the buffer works."""
    assert clear_buffer_check is None

