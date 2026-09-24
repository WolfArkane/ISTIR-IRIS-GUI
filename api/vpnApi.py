import os, json, subprocess, threading, platform, sys, webview, time, stat
import paramiko

if sys.platform == "win32":
    from winpty import PtyProcess
else:
    from ptyprocess import PtyProcess

import psutil, ipaddress
ISTIC_SUBNET = ipaddress.ip_network("148.60.9.0/24")

def is_vpn_connected():
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family.name == "AF_INET":
                print(f"DEBUG: interface={iface}, ip={addr.address}")
                try:
                    ip = ipaddress.ip_address(addr.address)
                    if ip in ISTIC_SUBNET:
                        return True
                except ValueError:
                    continue
    return False


#-----------------------------------------#
# CLASSE API VPN                          #
#-----------------------------------------#

class VpnApi:

    def start_vpn_watcher(self):
        def watch():
            last_state = None
            while True:
                connected = is_vpn_connected()
                if connected != last_state:
                    self._window.evaluate_js(f"updateVpnStatus({str(connected).lower()})")
                    last_state = connected
                time.sleep(5)
        threading.Thread(target=watch, daemon=True).start()