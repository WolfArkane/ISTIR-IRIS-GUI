const salleSelect = document.getElementById("salle-select");
const posteSelect = document.getElementById("poste-select");
const connectButton = document.getElementById("connect-button");

let SALLES_DATA = { salles: [] };

window.addEventListener("pywebviewready", async () => {
  SALLES_DATA = await window.pywebview.api.get_salles();

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

connectButton.addEventListener("click", async () => {
  const salleId = salleSelect.value;
  const posteId = posteSelect.value;
  const username = document.getElementById("ssh-username").value;

  if (!username) {
    alertbox.render({
      title: 'Erreur',
      message: 'Il faut renseigner un utilisateur !',
      btnTitle: 'Ok',
      border: true,
      themeColor: '#da1d1d'
    });
    return;
  }

  const host = `${salleId}${posteId}`;

  console.log("Dimensions envoyées:", window.term.cols, window.term.rows);
  const result = await window.pywebview.api.ssh_connect(host, username, window.term.cols, window.term.rows);
  console.log(result)

  if (result.status === "ok") {
    connectButton.textContent = "Connecté";
    connectButton.disabled = true;

    //fitAddon.fit();
    //window.pywebview.api.ssh_resize(window.term.cols, window.term.rows);
  } else {
    //alert("Erreur de connexion : " + result.message);
    alertbox.render({
      title: 'Erreur de connexion',
      message: result.message,
      btnTitle: 'Ok',
      border: true,
      themeColor: '#da1d1d'
    });
    return;
  }
});