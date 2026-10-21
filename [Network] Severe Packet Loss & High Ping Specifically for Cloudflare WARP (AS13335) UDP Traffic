
    Issue Summary:
    When connecting via Cloudflare WARP, the game experiences severe latency (600-999ms) and constant packet loss (>20%). However, rigorous UDP testing through the same WARP tunnel to other destinations shows near-perfect connectivity.

    Test Methodology & Evidence:
    To isolate the issue, I conducted a 11,000+ packet UDP trace using Trippy (ICMP/UDP) targeting 8.8.8.8 while connected to the exact same Cloudflare WARP node used for War Thunder.

*Trippy Results: 11,282 packets sent, only 40 failed. Packet Loss: 0.4% . Latency is stable.
*In-Game Results: Ping fluctuates between 600ms and 999ms. Packet Loss (PL) hits 20% to 37% consistently in matches.

    Technical Deduction:
    The discrepancy proves that local ISP and the WARP tunnel are functioning perfectly. The failure is occurring on the “Last Mile” between Cloudflare’s egress node and Gaijin’s game servers .

It is highly likely applying strict QoS throttling or dropping UDP packets originating from Cloudflare’s AS13335 range on the network path.

The command from terminal is :sudo trip -u 8.8.8.8

-u : udp
