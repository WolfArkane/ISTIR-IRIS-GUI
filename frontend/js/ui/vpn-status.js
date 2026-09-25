const vpnStatus = document.getElementById("vpn-status");

// Appelée par Python via evaluate_js() depuis le watcher VPN
function updateVpnStatus(connected) {
  if (connected) {
    vpnStatus.textContent = "Connecté";
    vpnStatus.classList.remove("vpn-status--off");
    vpnStatus.classList.add("vpn-status--on");
  } else {
    vpnStatus.textContent = "Déconnecté";
    vpnStatus.classList.remove("vpn-status--on");
    vpnStatus.classList.add("vpn-status--off");
  }
}