import os

from netsim import __version__
from netsim.utils import log,strings
from box import Box

"""
The initial lab exercises do not use BGP configuration module on the
devices, because we want the user to start BGP configuration from scratch.

That approach does not work for FRR containers because you cannot restart FRR
after modifying /etc/frr/daemons -- restating FRR kills the top-level container
process. Cumulus Linux does not have the same problem as it runs a different
init process.

This plugin is a fix for the FRR container initialization: if the device is a FRR container, the
clab binds are replaced with a mapping of FRR daemons into a local file. The
modifier FRR daemons file starts BGP, OSPFv2 and OSPFv3 (so we have a generic
solution in case we need it somewhere else).

Finally, the plugin adds "we already started BGP daemon for you" message to the
topology message to tell the user what's going on.
"""
def post_node_transform(topology: Box) -> None:
  uses_clab = topology.get('provider', None) == 'clab'
  if not uses_clab:
    return

  for n in topology.nodes:
    rtr = topology.nodes[n]
    # do it only for frr which has no bgp module already activated
    if rtr.device == 'frr' and not 'bgp' in rtr:
      strings.print_colored_text('[FIX_FRR]  ','yellow','FIX_FRR ')
      print(f"updating daemons on node {n}")
      rtr.clab.pop('config_templates', None)
      rtr.clab.binds = []
      rtr.clab.binds.append('frr-daemons:/etc/frr/daemons')

  if 'message' not in topology:
    topology.message = ''

  topology.message += '''
We already started BGP daemon in the FRR containers. You can connect to
your device and start configuring BGP.
'''

  return


def init(topology: Box) -> None:
    # Define custom data for node, to be used to cleanup bgp config
    topology.defaults.attributes.node.ignore_bgp_configuration = None
    return

def post_transform(topology: Box) -> None:
  for n in topology.nodes:
    rtr = topology.nodes[n]
    # remove the BGP config if the attribute 'ignore_bgp_configuration' is set to true
    if rtr.device == 'frr' and 'bgp' in rtr and rtr.get('ignore_bgp_configuration', False):
      strings.print_colored_text('[FIX_FRR]  ','yellow','FIX_FRR ')
      print(f"removing non-essential BGP config on node {n}")
      bgp_to_keep = [ 'as', 'ipv4', 'ipv6', 'router_id' ]
      current_bgp_items = list(rtr['bgp'].keys())
      for bgp_item in current_bgp_items:
        if bgp_item not in bgp_to_keep:
          del rtr['bgp'][bgp_item]
