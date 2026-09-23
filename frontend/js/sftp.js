let sftpReady = false;
let currentPath = ".";

function joinPath(base, name) {
  if (base === "/") return `/${name}`;
  return `${base}/${name}`;
}

function parentPath(path) {
  if (path === "/") return "/";
  const parts = path.split("/").filter(Boolean);
  parts.pop();
  return "/" + parts.join("/");
}

function onSftpReady(success, error) {
  sftpReady = success;
  const toggle = document.getElementById("sftp-toggle");
  toggle.disabled = !success;
  if (!success) console.error("SFTP indisponible:", error);
}

function onSftpDone(success, error) {
  if (success) refreshList();
  else console.error("Erreur SFTP:", error);
}

function onSftpProgress(sent, total) {
  // à brancher sur une progress bar si besoin plus tard
}

function renderSftpPanel() {
  const container = document.getElementById("sftp-container");
  container.innerHTML = `
    <div class="sftp-toolbar">
      <button id="sftp-up">⬆</button>
      <span id="sftp-path">${currentPath}</span>
      <button id="sftp-upload-btn">Upload</button>
    </div>
    <div id="sftp-list" class="sftp-list"></div>
  `;
  document.getElementById("sftp-up").addEventListener("click", () => navigate(parentPath(currentPath)));
  document.getElementById("sftp-upload-btn").addEventListener("click", () => {window.pywebview.api.sftp_upload(currentPath);});
}

async function navigate(path) {
  const result = await window.pywebview.api.sftp_list_dir(path);
  if (result.error) {
    console.error(result.error);
    return;
  }
  currentPath = result.path;
  document.getElementById("sftp-path").textContent = currentPath;
  renderList(result.entries);
}

function renderList(entries) {
  const list = document.getElementById("sftp-list");
  list.innerHTML = "";
  entries.forEach(e => {
    const row = document.createElement("div");
    row.className = "sftp-row";
    row.textContent = (e.is_dir ? "📁 " : "📄 ") + e.name;
    row.addEventListener("dblclick", () => {
      if (e.is_dir) navigate(joinPath(currentPath, e.name));
      else window.pywebview.api.sftp_download(joinPath(currentPath, e.name), e.name);
    });
    list.appendChild(row);
  });
}

function refreshList() {
  navigate(currentPath);
}

// --- init ---
document.getElementById("sftp-toggle").disabled = true;

document.getElementById("sftp-toggle").addEventListener("click", () => {
  const panel = document.getElementById("sftp-container");
  const willOpen = panel.classList.contains("collapsed"); // état avant toggle

  panel.classList.toggle("collapsed");

  if (willOpen && sftpReady && !panel.dataset.initialized) {
    panel.dataset.initialized = "true";
    renderSftpPanel();
    navigate(".");
  }
});
