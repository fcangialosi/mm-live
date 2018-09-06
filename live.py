import sys, os
import re
from collections import defaultdict
import time

ms_per_bin = int(sys.argv[1])

def ms_to_bin(ms):
    return ms / ms_per_bin

def bin_to_seconds(b):
    return "%.3f" % (b * ms_per_bin / 1000.0)

def bits_to_mbps(bits, duration=(ms_per_bin / 1000.0)):
    return bits / duration / 1000000.0

capacity = defaultdict(int)
arrivals = defaultdict(lambda : defaultdict(int))
departures = defaultdict(lambda : defaultdict(int))
delays = defaultdict(list)
all_delays = []
first_t, last_t, base_t = None, None, None
capacity_sum, arrival_sum, departure_sum = 0, defaultdict(int), defaultdict(int)
xmin,xmax = None,None

curr_tbin = 0

header = True
last = time.time()
for l in sys.stdin:
    if header:
        m = re.search(r"^# base timestamp: (\d+)", l)
        if m:
            base_t = int(m.groups()[0])
            continue
        elif l[0] == "#":
            continue
        else:
            header = False

    sp = l.strip().split(" ")
    t, etype, num_bytes = sp[0:3]

    t = int(t)
    t -= base_t
    if (xmin and t < xmin) or (xmax and t > xmax):
        continue

    tbin = ms_to_bin(t)

    if tbin > curr_tbin:
        t = bin_to_seconds(curr_tbin)
        dep_t = bits_to_mbps(departures[curr_tbin]['sum']) if curr_tbin in departures else 0
        del_t = max(delays[curr_tbin]) if curr_tbin in delays else 0

        #sys.stdout.write("{} {} {} {}\n".format(t,dep_t,del_t,time.time() - last))
        sys.stdout.write("{} {} {}\n".format(t,dep_t,del_t))
        sys.stdout.flush()
        last = time.time()

        curr_tbin = tbin

    if not last_t:
        first_t = t
        last_t = t
    last_t = max(t, last_t)

    num_bytes = int(num_bytes)
    num_bits = num_bytes * 8

    if etype == "+":
        flow = sp[3]
        #agg_name = find_agg_name(flow)
        #arrivals[tbin][flow] += num_bits
        arrivals[tbin]['sum'] += num_bits
        #arrival_sum[flow] += num_bits
        arrival_sum['sum'] += num_bits
        #if agg_name:
        #    arrivals[tbin][agg_name] += num_bits
        #    arrival_sum[agg_name] += num_bits
    elif etype == "-":
        flow = sp[3]
        #agg_name = find_agg_name(flow)
        #departures[tbin][flow] += num_bits
        departures[tbin]['sum'] += num_bits
        #departure_sum[flow] += num_bits
        departure_sum['sum'] += num_bits
        #if agg_name:
        #    departures[tbin][agg_name] += num_bits
        #    departure_sum[agg_name] += num_bits
        delay = int(sp[4])
        delays[tbin].append(delay)
        #all_delays.append(delay)
        
    elif etype == "#":
        pass
        #capacity[tbin] += num_bits
        #capacity_sum += num_bits
    else:
        sys.exit("unrecognized event type: %s" % etype)
###
