# REFERENCE COMMANDS

## SSH

### Attach to srlinux CLI
docker exec -it clab-1srlinux_2clients-srlinux sr_cli

### Attach to clients
docker exec -it clab-1srlinux_2clients-client1 sh

## GNMIC

### cmds from clab_yang
**REF:** https://github.com/martimy/clab_yang
**Configure an Interface using CLI**
```
A:router1# set /interface ethernet-1/21 admin-state enable subinterface 0 admin-state enable ipv4 admin-state enable address 192.168.1.1/24
A:router1# diff flat
A:router1# commit now
A:router1# show interface ethernet-1/21.0
A:router1# quit
```
**Configure using gNMIc**

```
gnmic -a router1 capabilities
gnmic -a router1 capabilities | awk -F  ':' '/interface/ {print $3}'
gnmic -a router1 capabilities | awk -F  ':' '/network-instance/ {print $3}'
gnmic -a router1 capabilities | awk -F  ':' '/ospf/ {print $3}'
gnmic -a router1 get --path /interface[name=ethernet-1/21]/subinterface[index=0] -t config
gnmic -a router1 get --path /interface[name=ethernet-1/21]/subinterface[index=0] -t config --format flat

gnmic -a router2,router3 set \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0] \
--update-value '{"index": 0}'

gnmic -a router2 set \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0]/ipv4 \
--update-value '{"address": [{"ip-prefix": "192.168.2.1/24"}]}'

gnmic -a router3 set \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0]/ipv4 \
--update-value '{"address": [{"ip-prefix": "192.168.3.1/24"}]}'

gnmic -a router2,router3 set \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0]/admin-state \
--update-value enable \
--update-path /interface[name=ethernet-1/21]/subinterface[index=0]/ipv4/admin-state \
--update-value enable

gnmic -a router2,router3 get --path /interface[name=ethernet-1/21] -t config --format flat

```
**Create a network-instance**

```
gnmic -a router1 set \
--update-path /network-instance[name=default] \
--update-value '{"name": "default"}' \
--update-path /network-instance[name=default]/admin-state \
--update-value enable \
--update-path /network-instance[name=default] \
--update-value '{"interface": [{"name": "ethernet-1/21.0"}]}'

gnmic -a router2,router3 set \
--update-path /network-instance[name=default] \
--update-file config/instance_config.json

gnmic -a router1,router2,router3 get --path /network-instance[name=default] -t
config --format flat

gnmic -a router1 set --update-path / --update-file config/interfaces_config.yaml

gnmic -a router1 get --path /interface -t config --format flat

```
**Using request-file flag**

```
gnmic -a router1,router2,router3 set --request-file config/interfaces_request.yaml
gnmic -a router1,router2,router3 get --path /interface -t config --format flat
gnmic -a router1,router2,router3 set --request-file ospf_request.yaml
gnmic -a router1 get --path /network-instance/protocols/ospf/ -t config --format flat
gnmic -a router1 get --path /network-instance[name=default]/route-table

```


### config
gnmic -a clab-1srlinux_2clients-srlinux:57400 -u admin -p NokiaSrl1! --skip-verify capabilities

gnmic --config nodes_connections.yaml capabilities 

gnmic --config nodes_connections.yml set --update ./config-set.yaml ????

### generate

```
gnmic --encoding json_ietf \
          generate  \
          --config-only \
          --dir srlinux-yang-models \
          --file srlinux-yang-models/srl_nokia/models/interfaces/srl_nokia-interfaces.yang \
          --path interface/subinterface/ipv4
```

```
gnmic generate \
        --dir srlinux-yang-models/ \
        --file srlinux-yang-models/srl_nokia/models/interfaces/srl_nokia-interfaces.yang \
        set-request \
        --update interface/subinterface/ipv4
```

```
gnmic --encoding json_ietf \
          generate  \
          --config-only \
          --file srlinux-yang-models/srl_nokia/models \
          --dir srlinux-yang-models \
          --path network-instance
```

### get

- srl-if-stats:
gnmic --config config/gnmic/nodes_connections.yaml get --path /interface[name=ethernet-1/*]/oper-state
gnmic --config config/gnmic/nodes_connections.yaml get --path /interface[name=ethernet-1/*]/statistics
gnmic --config config/gnmic/nodes_connections.yaml get --path /interface[name=ethernet-1/*]/traffic-rate

- srl-bgp: (optional)
gnmic --config config/gnmic/nodes_connections.yaml get --path /network-instance[name=*]/protocols/bgp/statistics

- srl-system-performance
gnmic --config config/gnmic/nodes_connections.yaml get --path /platform/control[slot=*]/cpu[index=all]/total
gnmic --config config/gnmic/nodes_connections.yaml get --path /platform/control[slot=*]/memory

- srl-routes
gnmic --config config/gnmic/nodes_connections.yaml get --path /network-instance[name=*]/route-table/ipv4-unicast/statistics/
gnmic --config config/gnmic/nodes_connections.yaml get --path /network-instance[name=*]/route-table/ipv6-unicast/statistics/

- srl-bridge: (optional)
gnmic --config config/gnmic/nodes_connections.yaml get --path /network-instance[name=*]/bridge-table/statistics/

- srl-apps:
gnmic --config config/gnmic/nodes_connections.yaml get --path /system/app-management/application[name=*]

- srl-net-instance:
gnmic --config config/gnmic/nodes_connections.yaml get --path /network-instance[name=*]/oper-state

gnmic -a clab-web-srlinux1 -u admin -p NokiaSrl1! --skip-verify --encoding json_ietf get --path /bfd/network-instance[name=*]/peer[local-discriminator=*]/session-state

## LAB CONFIG

### config srlinux

gnmic --config config/gnmic/nodes_connections.yaml capabilities 

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/interfaces_config.yaml

gnmic --config config/gnmic/nodes_connections.yaml get --path /interface -t config --format flat
gnmic --config config/gnmic/nodes_connections.yaml get --path /oam/link-measurement/interface[name=*]/last-reported-dynamic-delay -t config --format flat

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/instance_config.yaml


gnmic --config config/gnmic/nodes_connections.yaml get --path /network-instance -t config



gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/interfaces_config_srlinux1.yaml

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/interfaces_config_srlinux2.yaml

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/interfaces_config_srlinux3.yaml

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/instance_config_srlinux1.yaml

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/instance_config_srlinux2.yaml

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/instance_config_srlinux3.yaml

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/instance_config_srlinux1rr.yaml

gnmic --config config/gnmic/nodes_connections.yaml set --update-path / --update-file config/gnmic/instance_config_srlinux2rr.yaml


ping 10.0.2.2 network-instance default

### iperf3

docker exec client2 pkill iperf3
iperf3 -s -p 5201 -D > iperf3_1.log

iperf3 -c 192.168.2.11 -t 10000 -i 10 -p 5201 -B 192.168.1.11 -P 8 -b 200K -M 1460

```
Breakdown of Options
-c 192.168.2.11
Specifies the server’s IP address to connect to as a client.

-t 10000
Test duration: run the test for 10,000 seconds (almost 2.8 hours).

-i 10
Output interval: display reporting results every 10 seconds.

-p 5201
Port: connect to server on port 5201 (default for iperf3, can be changed if server uses a different port).

-B 192.168.1.11
Bind: the client will use the local IP address 192.168.1.11 as its source interface.

-P 8
Parallel streams: run 8 parallel client streams/connections to maximize throughput and reveal network capacity.

-b 200K
Bandwidth (UDP mode only, otherwise ignored in TCP): attempt to send data at 200Kbps (kilobits per second) per stream.

-M 1460
Set the TCP (or UDP) Maximum Segment Size (MSS/MTU) to 1,460 bytes.
```
iperf3 -s -p 5201 -D > iperf3_1.log
iperf3 -c 10.0.2.2 -t 10000 -p 5201 -B 10.0.1.2 -b 2M -M 1460
iperf3 -c 10.0.2.2 -t 10000 -p 5201 -B 10.0.1.2 -b 2M -M 1460 &
iperf3 -c 20.0.2.2 -t 10000 -p 5202 -B 20.0.1.2 -b 2M -M 1460 &

iperf3 -s -p 5201 -D > iperf3_1.log
iperf3 -c 10.0.2.2 -t 10000 -p 5201 -B 10.0.1.2 -b 2M -M 1460 &
containerlab tools netem set -n clab-3srlinux_2clients-srlinux1 -i e1-2 --loss 99

### Link impairments

**REF:** https://containerlab.dev/cmd/tools/netem/set/

#### Displaying the netem details
containerlab tools netem show -n srl --format json

#### Setting delay and jitter:
containerlab tools netem set -n clab-web-srlinux1 -i e1-2 --delay 5ms --jitter 1ms

#### Setting packet loss
containerlab tools netem set -n clab-web-srlinux1 -i e1-2 --loss 99

#### Clear any existing impairments
containerlab tools netem set -n clab-web-srlinux1  -i e1-2

## Configure with existing yaml




## Misc

### Access GUIs

localhost:3000
localhost:9090

# REFERENCES:

https://github.com/srl-labs/nokia-basic-dci-lab/blob/main/configs/leaf1-dc1.cfg
https://github.com/srl-labs/nokia-basic-dci-lab/blob/main/dci.clab.yml
https://github.com/srl-labs/srl-bfd-lab/blob/main/configs/srl2.cfg
https://documentation.nokia.com/srlinux/22-3/SR_Linux_Book_Files/Configuration_Basics_Guide/configb-network_instances.html#configure_failure_detection_for_static_routes
https://medium.com/@netopschic/network-automation-series-7-configuring-static-routing-on-nokia-sr-linux-via-ansible-and-ef85edc52462
