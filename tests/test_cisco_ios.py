#!/usr/bin/env python2.7
"""This module runs tests against Cisco IOS devices.

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
from testutils import Utils
from os import path

def setup_module(module):
    """Setup variables for tests."""
    pwd = path.dirname(path.realpath(__file__))
    responses = Utils.parse_yaml(pwd + "/etc/responses.yml")
    module.EXPECTED_RESPONSES = responses["ios"]
    module.commands = Utils.parse_yaml(pwd + "/etc/commands.yml")
    module.commands = module.commands["ios"]
    dispatcher = Utils.parse_yaml(pwd + "/etc/dispatchers.yml")
    dispatcher = dispatcher["ios"]

    SSHClass = netmiko.ssh_dispatcher(dispatcher["device_type"])
    net_connect = SSHClass(**dispatcher)

def test_disable_paging():
    """Verify paging is disabled by looking for string after when paging would normally occur."""
    output = net_connect.send_command(commands["version"])
    assert "Configuration register is" in output

def test_ssh_connect():
    """Verify the connection was established successfully."""
    output = net_connect.send_command(commands["version"])
    assert "Cisco IOS Software" in output

def test_send_command():
    """Verify a command can be sent down the channel successfully."""
    output = net_connect.send_command(commands["basic"])
    assert EXPECTED_RESPONSES["interface_ip"] in output

def test_send_command_expect():
    """Verify a command can be sent down the channel successfully."""
    output = net_connect.send_command_expect(commands["basic"])
    assert EXPECTED_RESPONSES["interface_ip"] in output

def test_base_prompt():
    """Verify the router prompt is detected correctly."""
    base_prompt = net_connect.base_prompt
    assert base_prompt == EXPECTED_RESPONSES["base_prompt"]

def test_strip_prompt():
    """Ensure the router prompt is not in the command output"""
    output = net_connect.send_command(commands["version"])
    assert EXPECTED_RESPONSES["base_prompt"] not in output
    output = net_connect.send_command_expect(commands["version"])
    assert EXPECTED_RESPONSES["base_prompt"] not in output


def test_strip_command():
    """Ensure that the command that was executed does not show up in the command output."""
    output = net_connect.send_command(commands["version"])
    assert commands["basic"] not in output
    output = net_connect.send_command_expect(commands["version"])
    assert commands["basic"] not in output

def test_normalize_linefeeds():
    """Ensure no '\r\n' sequences"""
    output = net_connect.send_command(commands["version"])
    assert not '\r\n' in output
    output = net_connect.send_command_expect(commands["version"])
    assert not '\r\n' in output

def test_clear_buffer():
    """Test that clearing the buffer works."""
    net_connect.send_command(commands["version"])
    net_connect.clear_buffer()
    output = net_connect.clear_buffer()
    assert output is None

def test_enable_mode():
    """Verify we enter enable mode properly."""
    output = net_connect.enable()
    assert output == EXPECTED_RESPONSES["enable_prompt"]
    net_connect.exit_enable_mode()


def test_config_mode():
    """Verify we enter config mode properly."""
    net_connect.enable()
    output = net_connect.config()
    assert EXPECTED_RESPONSES["config_mode"] in output
    net_connect.exit_config_mode()
    net_connect.exit_enable_mode()

def test_command_set():
    """Verify we send multiple commands properly."""
    net_connect.enable()
    net_connect.config()
    net_connect.send_config_set(commands["config"])
    output = net_connect.send_command("show running-config | include logging buffer")
    assert "logging buffered 20010" in output
    net_connect.exit_config_mode()
    net_connect.exit_enable_mode()

def test_exit_config_mode():
    """Verify that we exit config mode properly."""
    net_connect.enable()
    net_connect.config()
    output = net_connect.exit_config_mode()
    assert not EXPECTED_RESPONSES['config_mode'] in exit_config_mode
    net_connect.exit_enable_mode()


def test_exit_enable_mode():
    """Verify we exit enable mode properly."""
    output = net_connect.enable()
    assert EXPECTED_RESPONSES["user_exec_prompt"] in output
    net_connect.exit_enable_mode()

def test_disconnect():
    """Verify we disconnect from devices cleanly."""
    output = net_connect.disconnect()
    assert output is None
