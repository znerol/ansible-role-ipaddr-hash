# (c) 2020, Lorenz Schori <lo@znerol.ch>
#
# ipaddr_hash filter derived from ansible slaac filter.
#
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import hashlib

try:
    import netaddr
except ImportError:
    # in this case, we'll make the filters return error messages (see bottom)
    netaddr = None

from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_bytes, to_text
from ansible.plugins.filter.ipaddr import ipaddr


def ipaddr_hash(value, seed):
    ''' takes a given IP prefix, and returns it combined with the sha256 sum
        of the seed to form a complete address. Works best with large prefixes
        (i.e., IPv6) due to the bigger address space. '''

    if netaddr is None:
        raise AnsibleFilterError(
                "The ipaddr_hash filter requires python's netaddr be "
                "installed on the ansible controller")

    try:
        vtype = ipaddr(value, 'type')
        if vtype == 'address':
            v = ipaddr(value, 'cidr')
        elif vtype == 'network':
            v = ipaddr(value, 'subnet')

        value = netaddr.IPNetwork(v)
    except Exception:
        raise AnsibleFilterError(
                "The ipaddr_hash filter requires a valid IPv6 prefix")

    if not seed:
        raise AnsibleFilterError(
                "The ipaddr_hash filter requires a non-empty seed, e.g., the "
                "inventory_hostname")

    dgst = hashlib.sha256(to_bytes(seed)).hexdigest()
    host = int(dgst, 16) & int(value.hostmask)
    net = int(value.ip) & int(value.netmask)
    ipver = ipaddr(value, 'version')
    return to_text(netaddr.IPAddress(net + host, ipver))


class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
            'ipaddr_hash': ipaddr_hash,
        }
