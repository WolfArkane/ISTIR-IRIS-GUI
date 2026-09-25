const salleSelect = document.getElementById("salle-select");
const posteSelect = document.getElementById("poste-select");
const connectButton = document.getElementById("connect-button");

let SALLES_DATA = { salles: [] };

window.addEventListener("pywebviewready", async () => {
  SALLES_DATA = await sallesApi.getSalles();

  SALLES_DATA.salles.forEach((salle) => {
    const option = document.createElement("option");
    option.value = salle.id;
    option.textContent = salle.label;
    salleSelect.appendChild(option);
  });
});

salleSelect.addEventListener("change", () => {
  const salleId = salleSelect.value;
  const salle = SALLES_DATA.salles.find((s) => s.id === salleId);

  posteSelect.innerHTML = '<option value="">-- Choisir un poste --</option>';
  posteSelect.disabled = !salleId;
  updateConnectButton();

  if (salle) {
    salle.postes.forEach((poste) => {
      const option = document.createElement("option");
      option.value = poste.id;
      option.textContent = poste.label;
      posteSelect.appendChild(option);
    });
  }
});

posteSelect.addEventListener("change", updateConnectButton);

function updateConnectButton() {
  const ready = salleSelect.value && posteSelect.value;
  connectButton.disabled = !ready;
  connectButton.classList.toggle("active", ready);
}

function updateConnectionTarget(salleLabel, posteLabel) {
  const target = document.getElementById("connection-target");
  const label = document.getElementById("connection-label");
  if (!target || !label) return;

  if (salleLabel && posteLabel) {
    label.textContent = `${salleLabel} / ${posteLabel}`;
    target.classList.add("connected");
  } else {
    label.textContent = "Non connecté";
    target.classList.remove("connected");
  }
}

// Appelée par Python via evaluate_js() si la session SSH se termine côté serveur
function onSshClosed() {
  appState.connected = false;
  connectButton.textContent = "Se connecter";
  connectButton.disabled = false;
  updateConnectionTarget(null, null);
}

connectButton.addEventListener("click", async () => {
  const salleId = salleSelect.value;
  const posteId = posteSelect.value;
  const username = document.getElementById("ssh-username").value;
  const password = document.getElementById("ssh-password").value;

  if (!username || !password) {
    alertbox.render({
      title: 'Erreur',
      message: 'Il faut renseigner un utilisateur et un mot de passe !',
      btnTitle: 'Ok',
      border: true,
      themeColor: '#da1d1d'
    });
    return;
  }

  const host = `${salleId}${posteId}`;

  const result = await sshApi.connect(host, username, password, window.term.cols, window.term.rows);

  document.getElementById("ssh-password").value = "";

  if (result.status === "ok") {
    appState.connected = true;
    connectButton.textContent = "Connecté";
    connectButton.disabled = true;

    const salleLabel = salleSelect.options[salleSelect.selectedIndex].textContent;
    const posteLabel = posteSelect.options[posteSelect.selectedIndex].textContent;
    updateConnectionTarget(salleLabel, posteLabel);
  } else {
    alertbox.render({
      title: 'Erreur de connexion',
      message: result.message,
      btnTitle: 'Ok',
      border: true,
      themeColor: '#da1d1d'
    });
  }
});