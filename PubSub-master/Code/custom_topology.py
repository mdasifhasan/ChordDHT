"""Custom topology example
Two directly connected switches plus a host for each switch:
   host --- switch --- switch --- host
Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    

    def __init__( self ):
        "Create custom topo."

        # Initializing topology
        Topo.__init__( self )

        # Adding hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
	leftHost2 = self.addHost( 'h3' )
        rightHost2 = self.addHost( 'h4' )
        leftSwitch = self.addSwitch( 's1' )
	leftSwitch2 = self.addSwitch( 's2' )
	leftSwitch3 = self.addSwitch( 's3' )
	leftSwitch4 = self.addSwitch( 's4' )
	leftSwitch5 = self.addSwitch( 's5' )
        

        # Adding links between hosts, switches etc
        self.addLink( leftHost2, leftSwitch2 )
	self.addLink( leftHost, leftSwitch )
	self.addLink( rightHost, leftSwitch3 )
	self.addLink( rightHost2, leftSwitch4 )
	self.addLink( leftSwitch2, leftSwitch5 )
	self.addLink( leftSwitch, leftSwitch5 )
	self.addLink( leftSwitch3, leftSwitch5 )
	self.addLink( leftSwitch4, leftSwitch5 )
        


topos = { 'mytopo': ( lambda: MyTopo() ) }
