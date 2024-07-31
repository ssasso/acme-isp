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
    # Define custom global item, to be used to cleanup routing config
    topology.defaults.attributes['global']['ignore_routing_configuration_on_nodes'] = {
      'type': 'list',
      '_subtype': 'str',
    }
    topology.defaults.attributes['global']['remove_routing_group_data'] = {
      'type': 'list',
      '_subtype': 'str',
    }
    return

def post_transform(topology: Box) -> None:
  # remove the BGP/OSPF config for specific nodes
  for ignore_rt_node in topology.get('ignore_routing_configuration_on_nodes', []):
    if ignore_rt_node in topology.nodes and topology.nodes[ignore_rt_node].device == 'frr':
      rtr = topology.nodes[ignore_rt_node]
      # BGP Stuff
      if 'bgp' in rtr:
        strings.print_colored_text('[FIX_FRR]  ','yellow','FIX_FRR ')
        print(f"removing non-essential ROUTING config on node {ignore_rt_node}")
        bgp_to_keep = [ 'as', 'ipv4', 'ipv6', 'router_id' ]
        bgp_to_force_append = {
          'neighbors': [],
          'advertise_loopback': False,
        }
        current_bgp_items = list(rtr['bgp'].keys())
        for bgp_item in current_bgp_items:
          if bgp_item not in bgp_to_keep:
            del rtr['bgp'][bgp_item]
        for a, av in bgp_to_force_append.items():
          rtr['bgp'][a] = av
        for i in rtr.interfaces:
          if 'bgp' in i:
            del i['bgp']
      # OSPF Stuff
      if 'ospf' in rtr:
        # delete ospf loopback data
        del rtr.loopback['ospf']
        # delete ospf data from interfaces
        for i in rtr.interfaces:
          if 'ospf' in i:
            del i['ospf']
      # Routing module stuff
      if 'routing' in rtr:
        rtr['routing'] = {
          '_rm_per_af': True,
        }

def pre_transform(topology: Box) -> None:
  # remove non-needed groups
  for g_to_del in topology.get('remove_routing_group_data', []):
    if g_to_del in topology.groups:
      strings.print_colored_text('[FIX_FRR]  ','yellow','FIX_FRR ')
      print(f"removing group data for {g_to_del}")
      # append members to 'topology.ignore_routing_configuration_on_nodes' (and make it unique)
      if 'ignore_routing_configuration_on_nodes' not in topology:
        topology['ignore_routing_configuration_on_nodes'] = []
      for m in topology.groups[g_to_del].get('members', []):
        topology['ignore_routing_configuration_on_nodes'].append(m)
      del topology.groups[g_to_del]
  # if present, make ignore_routing_configuration_on_nodes unique
  if 'ignore_routing_configuration_on_nodes' in topology:
    topology['ignore_routing_configuration_on_nodes'] = list(set(topology['ignore_routing_configuration_on_nodes']))
