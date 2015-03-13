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
    module.net_connect = SSHClass(**dispatcher)

def test_disable_paging():
    """Verify paging is disabled by looking for string after when paging would normally occur."""
    multiple_line_output = net_connect.send_command(commands["multiline"], delay_factor=2)
    assert 'security-zone untrust' in multiple_line_output

def test_verify_ssh_connect():
    """Verify the connection was established successfully."""
    show_version = net_connect.send_command(commands["version"])
    assert 'JUNOS Software Release' in show_version

def test_verify_send_command():
    """Verify a command can be sent down the channel successfully."""
    show_ip = net_connect.send_command(commands["basic"])
    assert EXPECTED_RESPONSES["interface_ip"] in show_ip

def test_base_prompt():
    """Verify the router base_prompt is detected correctly."""
    base_prompt = net_connect.base_prompt
    assert base_prompt == EXPECTED_RESPONSES["base_prompt"]

def test_strip_prompt():
    """Ensure the router prompt is not in the command output."""
    show_version = net_connect.send_command(commands["version"])
    assert EXPECTED_RESPONSES["base_prompt"] not in show_version

def test_strip_command():
    """Ensure that the command that was executed does not show up in the command output."""
    show_ip = net_connect.send_command(commands["basic"])
    assert commands["basic"] not in show_ip

def test_normalize_linefeeds():
    """Ensure no '\r' sequences."""
    show_ip = net_connect.send_command(commands["basic"])
    assert not '\r' in show_ip

def test_clear_buffer():
    """Test that clearing the buffer works."""
    net_connect.remote_conn.send(commands["version"])
    clear_buffer_check = net_connect.clear_buffer()
    clear_buffer_check = net_connect.clear_buffer()
    assert clear_buffer_check is None

