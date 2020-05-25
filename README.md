Ansible Role: ipaddr\_hash
==========================

[![Build Status](https://travis-ci.org/znerol/ansible-role-ipaddr-hash.svg?branch=master)](https://travis-ci.org/znerol/ansible-role-ipaddr-hash)

Provides a Jinja2 filter plugin to compute an IP address given a prefix and a
seed, e.g., the `inventory_hostname`.

This plugin is useful for people seeking a predictable addressing scheme for
statically assigned IPv6 addresses based on hostnames.

The algorithm used to derive an ip is simple:

    ip = prefix + (sha256(seed) & hostmask)

Requirements
------------

None

Role Variables
--------------

None

Dependencies
------------

* Python module [netaddr](https://pypi.org/project/netaddr/) on controller.

Example Playbook
----------------

Usage of `ipaddr_hash` filter:

    - hosts: localhost
      tasks:
        - import_role:
            name: znerol.ipaddr_hash

        - debug:
            msg: "Generated IPv6 address for example.com with prefix '2001:db8::/64' is {{ '2001:db8::/64' | ipaddr_hash('example.com') }}"

This should generate the address: `2001:db8::13d2:1255:86ce:1947`.

See [test/test.yml](tests/test.yml) for sample input/output.

License
-------

GPLv3
