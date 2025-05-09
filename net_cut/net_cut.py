#!/user/bin/env python

# Trap all the packets that go to forward chain and use netfilter
# iptables -I FORWARD -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES RECEIVED
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES YOU'RE SENDING OUT LOCALLY
# iptables -I INPUT -j NFQUEUE --queue-num 0 # CREATE THE NFQUEUE TO TRACK PACKAGES YOU'RE RECEIVING LOCALLY
# iptables --flush # FLUSH THE IPTABLE WHEN YOU'RE DONE
import netfilterqueue

def process_packet(packet):
    print(packet)
    # packet.drop() to intercept, packet.accept() to forward
    packet.accept()

queue = netfilterqueue.NetFilterQueue()
queue.bind(0, process_packet)
queue.run()