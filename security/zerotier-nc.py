#! /usr/bin/env python3
##
# ZeroTier Network Controller
# By Amos <LFlare> Ng
##
from ipaddress import *
import argparse
import atexit
import json
import pickle
import platform
import requests
import sys
import collections

base_api = "http://127.0.0.1:9993"
ctrlr = None


def pprint(obj):
    print(json.dumps(obj, indent=2, separators=(',', ': ')))


def ddict():
    return collections.defaultdict(ddict)


def request(url, payload=None, method="get"):
    """Simple request wrapper

    Takes a couple of variables and wraps around the requests
    module

    Args:
        url: API URL
        method: Query method (default: {"get"})
        payload: JSON payload (default: {None})

    Returns:
        Dataset as result from query
        JSON Object
    """
    r = None
    if payload is not None:
        r = requests.post(
            base_api+url, headers=ctrlr["headers"], json=payload)
    elif method == "get":
        r = requests.get(
            base_api+url, headers=ctrlr["headers"])
    elif method == "delete":
        r = requests.delete(
            base_api+url, headers=ctrlr["headers"])
    return r.json()


def save_ctrlr():
    with open(get_filepath()+"/ctrlr.pickle", "wb") as file:
        pickle.dump(ctrlr, file)


def load_ctrlr():
    global ctrlr
    try:
        with open(get_filepath()+"/ctrlr.pickle", "rb") as file:
            ctrlr = pickle.load(file)
    except:
        ctrlr = ddict()


def get_filepath():
    """Get filepath according to OS"""
    if platform.system() == "Linux":
        return "/var/lib/zerotier-one"
    elif platform.system() == "Darwin":
        return "/Library/Application Support/ZeroTier/One"
    elif platform.system() == "FreeBSD" or platform.system() == "OpenBSD":
        return "/var/db/zerotier-one"
    elif platform.system() == "Windows":
        return "C:\ProgramData\ZeroTier\One"


def set_headers():
    """Sets authentication headers globally

    Automatically detect system and reads authtoken.secret
    to set authenticaiton headers used in request method
    globally.
    """
    with open(get_filepath()+"/authtoken.secret") as file:
        ctrlr["headers"] = {"X-ZT1-Auth": file.read()}


def set_id():
    ctrlr["ztid"] = request("/status").get("address")


def valid_nwid(nwid):
    return nwid is not None and (len(nwid) == 16 or len(nwid) == 6)


def valid_ztid(ztid):
    return ztid is not None and len(ztid) == 10


def alias(alias=None, nwid=None, ztid=None):
    if alias is not None:

        # Set alias
        if valid_nwid(nwid):

            # Set member alias
            if valid_ztid(ztid):
                ctrlr["network"][nwid]["member"][ztid]["alias"] = alias
                return ctrlr["network"][nwid]["member"]

            # Set network alias
            else:
                ctrlr["network"][nwid]["alias"] = alias
                request("/controller/network/"+nwid, {"name": alias})
                return ctrlr["network"]

        # Get from alias
        else:

            # Get member from alias
            if ":" in alias:
                nwalias, ztalias = alias.split(":")
                for x, y in ctrlr["network"].items():
                    if nwalias == y["alias"]:
                        for xx, yy in ctrlr["network"][x]["member"].items():
                            if ztalias == yy["alias"]:
                                return x, xx

            # Get network from alias
            else:
                for x, y in ctrlr["network"].items():
                    if y["alias"] == alias:
                        return x
    else:

        # Get alias
        if valid_nwid(nwid):

            # Get member alias
            if valid_ztid(ztid):
                for x, y in ctrlr["network"].items():
                    if nwid == x:
                        for xx, yy in ctrlr["network"][x]["member"].items():
                            if ztid == xx:
                                return y["alias"], yy["alias"]

            # Get network alias
            else:
                for x, y in ctrlr["network"].items():
                    if nwid == x:
                        return y["alias"]


def net_add(nwid):
    return request("/controller/network/"+nwid, {})


def net_del(nwid):
    if nwid in ctrlr["network"]:
        ctrlr["network"][nwid].clear()
        del ctrlr["network"][nwid]
    return request("/controller/network/"+nwid, method="delete")


def net_info(nwid):
    ctrlr["network"][nwid].update(request("/controller/network/"+nwid))
    return ctrlr["network"][nwid]


def net_ipadd(nwid, ip):
    ipaddrs = list(ip_network(ip).hosts())
    start, end = tuple([str(x) for x in ipaddrs[::len(ipaddrs)-1]])
    net = net_info(nwid)
    net["v4AssignMode"] = {"zt": "true"}
    net["routes"].append({"target": ip, "via": "null"})
    net["ipAssignmentPools"].append({"ipRangeStart": start, "ipRangeEnd": end})
    return request("/controller/network/"+nwid, net)


def net_ipdel(nwid, ip):
    ipaddrs = list(ip_network(ip).hosts())
    start, end = tuple([str(x) for x in ipaddrs[::len(ipaddrs)-1]])
    net = net_info(nwid)
    net["v4AssignMode"] = {"zt": "true"}
    net["routes"] = [
        x for x in net["routes"]
        if x["target"] != ip]
    net["ipAssignmentPools"] = [
        x for x in net["ipAssignmentPools"]
        if x["ipRangeStart"] != start or x["ipRangeEnd"] != end]
    return request("/controller/network/"+nwid, net)


def net_list():
    nwids = request("/controller/network")
    new_nwids = dict()
    for nwid in nwids:
        new_nwids[nwid] = alias(nwid=nwid)
    return new_nwids


def net_pooladd(nwid, ip):
    ipaddrs = list(ip_network(ip).hosts())
    start, end = tuple([str(x) for x in ipaddrs[::len(ipaddrs)-1]])
    net = net_info(nwid)
    net["v4AssignMode"] = {"zt": "true"}
    net["ipAssignmentPools"].append({"ipRangeStart": start, "ipRangeEnd": end})
    return request("/controller/network/"+nwid, net)


def net_pooldel(nwid, ip):
    ipaddrs = list(ip_network(ip).hosts())
    start, end = tuple([str(x) for x in ipaddrs[::len(ipaddrs)-1]])
    net = net_info(nwid)
    net["v4AssignMode"] = {"zt": "true"}
    net["ipAssignmentPools"] = [
        x for x in net["ipAssignmentPools"]
        if x["ipRangeStart"] != start or x["ipRangeEnd"] != end]
    return request("/controller/network/"+nwid, net)


def net_routeadd(nwid, ip):
    net = net_info(nwid)
    net["routes"].append({"target": ip[0], "via": ip[1]})
    return request("/controller/network/"+nwid, net)


def net_routedel(nwid, ip):
    net = net_info(nwid)
    net["routes"] = [
        x for x in net["routes"]
        if x["target"] != ip]
    return request("/controller/network/"+nwid, net)


def member_auth(nwid, ztid):
    net = net_info(nwid)
    member = net["member"][ztid]
    member["authorized"] = "true"
    return request("/controller/network/"+nwid+"/member/"+ztid, member)


def member_deauth(nwid, ztid):
    net = net_info(nwid)
    member = net["member"][ztid]
    member["authorized"] = "false"
    return request("/controller/network/"+nwid+"/member/"+ztid, member)

def member_activebridge(nwid, ztid):
    net = net_info(nwid)
    member = net["member"][ztid]
    member["activeBridge"] = "true"
    return request("/controller/network/"+nwid+"/member/"+ztid, member)

def member_inactivebridge(nwid, ztid):
    net = net_info(nwid)
    member = net["member"][ztid]
    member["activeBridge"] = "false"
    return request("/controller/network/"+nwid+"/member/"+ztid, member)


def member_delete(nwid, ztid):
    del ctrlr["network"][nwid]["member"][ztid]
    return request(
        "/controller/network/"+nwid+"/member/"+ztid,
        method="delete"
    )


def member_info(nwid, ztid):
    net = net_info(nwid)
    member = net["member"][ztid]
    member.update(request("/controller/network/"+nwid+"/member/"+ztid))
    return member


def member_ipset(nwid, ztid, ip):
    member = member_info(nwid, ztid)
    member["ipAssignments"] = [ip]
    member = request("/controller/network/"+nwid+"/member/"+ztid, member)
    return member


def member_ipadd(nwid, ztid, ip):
    member = member_info(nwid, ztid)
    member["ipAssignments"].append(ip)
    member = request("/controller/network/"+nwid+"/member/"+ztid, member)
    return member


def member_ipdel(nwid, ztid, ip):
    member = member_info(nwid, ztid)
    if ip in member["ipAssignments"]:
        member["ipAssignments"].remove(ip)
    member = request("/controller/network/"+nwid+"/member/"+ztid, member)
    return member


def member_list(nwid):
    ztids = request("/controller/network/"+nwid+"/member")
    new_ztids = dict()
    for ztid in ztids:
        new_ztids[ztid] = dict()
        new_ztids[ztid]["ipAssignments"] = ", ".join(
            member_info(nwid, ztid)["ipAssignments"])

        try:
            new_ztids[ztid]["alias"] = ":".join(alias(nwid=nwid, ztid=ztid))
        except TypeError:
            new_ztids[ztid]["alias"] = alias(nwid=nwid, ztid=ztid)
    return new_ztids


def main():
    # Load/Create controller and set atexit argument
    load_ctrlr()
    atexit.register(save_ctrlr)

    # Populate current fields
    set_headers()
    set_id()

    # Used to detect runtime variables and configurations
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group()

    # Management actions
    actions.add_argument("--alias", metavar="[Alias]")

    # Network actions
    actions.add_argument("--net-add", action="store_true")
    actions.add_argument("--net-del", action="store_true")
    actions.add_argument("--net-info", action="store_true")
    actions.add_argument("--net-ipadd", metavar="[IP Address]")
    actions.add_argument("--net-ipdel", metavar="[IP Address]")
    actions.add_argument("--net-list", action="store_true")
    actions.add_argument("--net-pooladd", metavar="[IP Address]")
    actions.add_argument("--net-pooldel", metavar="[IP Address]")
    actions.add_argument("--net-routeadd", nargs=2, metavar="[IP Address]")
    actions.add_argument("--net-routedel", metavar="[IP Address]")

    # Member actions
    actions.add_argument("--member-auth", action="store_true")
    actions.add_argument("--member-deauth", action="store_true")
    actions.add_argument("--member-activebridge", action="store_true")
    actions.add_argument("--member-inactivebridge", action="store_true")
    actions.add_argument("--member-delete", action="store_true")
    actions.add_argument("--member-info", action="store_true")
    actions.add_argument("--member-ipset", metavar="[IP Address]")
    actions.add_argument("--member-ipadd", metavar="[IP Address]")
    actions.add_argument("--member-ipdel", metavar="[IP Address]")
    actions.add_argument("--member-list", action="store_true")

    # Variables
    parser.add_argument("-n", metavar="[Network ID]", default="______")
    parser.add_argument("-z", metavar="[Member ID]")

    # Alias
    parser.add_argument("a", metavar="[Alias]", nargs="?")

    # Parse arguments
    args = parser.parse_args()

    # Automatically extend network ID
    if args.n and len(args.n) == 6:
        args.n = ctrlr["ztid"] + args.n

    # Check if alias given
    if args.a and ":" in args.a:
        args.n, args.z = alias(alias=args.a)
    elif args.a:
        args.n = alias(alias=args.a)

    # Execute actions
    if args.alias:
        out = alias(alias=args.alias, nwid=args.n, ztid=args.z)
    elif args.net_add:
        out = net_add(nwid=args.n)
    elif args.net_del:
        out = net_del(nwid=args.n)
    elif args.net_info:
        out = net_info(nwid=args.n)
    elif args.net_ipadd:
        out = net_ipadd(nwid=args.n, ip=args.net_ipadd)
    elif args.net_ipdel:
        out = net_ipdel(nwid=args.n, ip=args.net_ipdel)
    elif args.net_list:
        out = net_list()
    elif args.net_pooladd:
        out = net_pooladd(nwid=args.n, ip=args.net_pooladd)
    elif args.net_pooldel:
        out = net_pooldel(nwid=args.n, ip=args.net_pooldel)
    elif args.net_routeadd:
        out = net_routeadd(nwid=args.n, ip=args.net_routeadd)
    elif args.net_routedel:
        out = net_routedel(nwid=args.n, ip=args.net_routedel)
    elif args.member_auth:
        out = member_auth(nwid=args.n, ztid=args.z)
    elif args.member_deauth:
        out = member_deauth(nwid=args.n, ztid=args.z)
    elif args.member_activebridge:
        out = member_activebridge(nwid=args.n, ztid=args.z)
    elif args.member_inactivebridge:
        out = member_inactivebridge(nwid=args.n, ztid=args.z)
    elif args.member_delete:
        out = member_delete(nwid=args.n, ztid=args.z)
    elif args.member_info:
        out = member_info(nwid=args.n, ztid=args.z)
    elif args.member_ipset:
        out = member_ipset(nwid=args.n, ztid=args.z, ip=args.member_ipset)
    elif args.member_ipadd:
        out = member_ipadd(nwid=args.n, ztid=args.z, ip=args.member_ipadd)
    elif args.member_ipdel:
        out = member_ipdel(nwid=args.n, ztid=args.z, ip=args.member_ipdel)
    elif args.member_list:
        out = member_list(nwid=args.n)
    else:
        parser.print_help()
        sys.exit(1)

    # Print output
    pprint(out)

if __name__ == "__main__":
    main()
