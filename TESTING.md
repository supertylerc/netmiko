# Testing

This document covers the test suite for Netmiko.

## Preparing to Run Tests

In order to run tests, you should create a copy of the following files:

* ./tests/etc/dispatchers.yml.example
* ./tests/etc/responses.yml.example

Remove the `.example` extension.  An example of how to do this on Mac OSX and
Linux is below.

```bash
for file in ./tests/etc/*.example; do
    cp "${file}" "`basename ${file} .example`"
done
```

These files (with `.example` removed) are ignored by git because they store
sensitive credentials and unique prompts.

Once you've copied the files, you should open `./tests/etc/dispatchers.yml`
and edit the username and password for each of the vendors you plan to work
with.  They are in vendor-specific dictionaries, but if you are using the same
credentials for all vendors, you can user your editors find-and-replace feature
to update the username and password for all vendors at one time.  To do this
in `vim`, type: `:%s/user[^n]/tyler"/g` and press enter.  Replace `tyler` with
your actual username.  For the password, it is similar:
`:%s/pass[^w]/harbl"/g`, where `harbl` is your password.

Next, you should change the `ip` varaible to the IP address that will be used
to connect to your device(s).

Next, you will need to edit `./tests/etc/responses.yml`.  This file is a little
bit more complex and requires that you make manual changes to the lines.  For
each vendor, you will need to modify the each of the keys to match your
environment.

* `base_prompt`: the prompt stripped of special characters (such as `>` and `#`)
* `router_prompt`: the prompt expected when not in config mode
* `router_conf_mode`: the prompt expected when in config mode
* `interface_ip`: an IP address that will be present in the equivalent of `show ip interface brief`
* `config_mode`: a key that may or may not be present that is an additional prompt for config mode

Regular expressions may eventually be used to nullify the requirement for
modifying this file.

Finally, you should ensure you have [`pytest`](http://pytest.org/latest/)
installed.  It can be installed with `sudo pip install pytest`.

## Running Tests

Netmiko uses [`pytest`](http://pytest.org/latest/).  You can run all of the
tests by typing `py.test`.  Unless you have access to every vendor that Netmiko
supports, though, you should expect some to fail.  Instead, you can run tests
for a specific vendor by typing `py.test -s -v TESTNAME.py`, where
`TESTNAME.py` is the name of the test file.  To run tests for Juniper Networks
devices, for example, you would just type `py.test -s -v test_juniper_srx.py`.

Before you submit a pull request for any change, no matter how insignificant,
please run the tests against the associated vendor(s).  If you're changing
a class from which other classes inherit, please test all of the child
classes.  If you are unable to test all child classes due to a lack of access,
please test against all that you are able.

## Writing Tests

If you are writing a new feature or significantly altering the behavior of an
existing feature, please write a test case for the change.

Tests are functions.  The name of each function should begin with `test_`.  The
rest of the name should be relatively descriptive.  A docstring should follow.
It should conform to [PEP257](https://www.python.org/dev/peps/pep-0257/).

All tests should be self-contained.  This means that if they require entering
configuration commands, you should start your test function with the
appropriate command to enter configuration mode and end your test function with
the appropriate command to exit configuration mode.

Each test is setup with the `net_connect` object.  This is an instance of the
vendor's class against which you are testing.  You should use this variable to
access the methods of your device.

The `setup_module()` function should do all of the preliminary work, and you
shouldn't have to modify it.  However, if you do, please ensure you are not
running anything after the point at which the device connection is established.
All tests should be self-contained at that point.

For an example of tests, refer to `./tests/test_juniper_srx.py`.
