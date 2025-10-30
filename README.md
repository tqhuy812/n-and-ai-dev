# n-and-ai-dev

## Deploy the lab
Activate the MCP Servers in the Copilot setting

## Apply srlinux2 initial configuration using gnmic:

```
gnmic -a clab-3srlinux_2clients-srlinux2:57400 -u admin -p NokiaSrl1! --skip-verify --encoding json_ietf set --update-path / --update-file containerlab/config/gnmic/init_config_srlinux2.yaml
```

## Verify shortest path

From client1

```
ping 10.0.2.2
```

## Generate traffic

From client2 (iperf server)

```
iperf3 -s -p 5201 -D > iperf3_1.log
```

From client 1 (iperf client)

```
iperf3 -c 10.0.2.2 -t 10000 -p 5201 -B 10.0.1.2 -b 2M -M 1460 &
```

## Observe the traffic via Grafana UI

Click on the "globe" icon of port 3000 to view the dashboard

## Verify Bidirectional Forwarding Detection (BFD) protocol

Open CLI of two devices: srlinux1 and srlinux2

```
enter state
info bfd
```

## Verify the alarm at Prometheus

Click on the "globe" icon of port 9090 to view the dashboard 

## Simulate a link failure event

Execute the following cmd on a different terminal to simulate the packet loss event at the e1-2 interface of srlinux1 (towards srlinux2)

```
containerlab tools netem set -n clab-3srlinux_2clients-srlinux1 -i e1-2 --loss 99
```

## Prompt for reroute

```
Configure srlinux1 with /workspaces/n-and-ai-dev/config_intent_srlinux1-reroute
```

```
Configure srlinux2 with /workspaces/n-and-ai-dev/config_intent_srlinux2-reroute
```

## Contact:

Huy Q. Tran (huy.h.tranATnokia-bell-labsDOTcom)
