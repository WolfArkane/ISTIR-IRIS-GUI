const alertbox = (() => {
  let overlayEl = null;

  function ensureOverlay() {
    if (overlayEl) return overlayEl;

    overlayEl = document.createElement("div");
    overlayEl.className = "alert-overlay";
    overlayEl.innerHTML = `
      <div class="alert-box">
        <h3 class="alert-title"></h3>
        <p class="alert-message"></p>
        <button class="alert-btn"></button>
      </div>
    `;
    document.body.appendChild(overlayEl);

    overlayEl.addEventListener("click", (e) => {
      if (e.target === overlayEl) close();
    });

    return overlayEl;
  }

  function close() {
    if (!overlayEl) return;
    overlayEl.classList.remove("visible");
  }

  function render({ title = "", message = "", btnTitle = "Ok", border = false, themeColor = "#da1d1d" } = {}) {
    const overlay = ensureOverlay();
    const box = overlay.querySelector(".alert-box");
    const titleEl = overlay.querySelector(".alert-title");
    const messageEl = overlay.querySelector(".alert-message");
    const btnEl = overlay.querySelector(".alert-btn");

    titleEl.textContent = title;
    messageEl.textContent = message;
    btnEl.textContent = btnTitle;

    box.classList.toggle("bordered", !!border);
    overlay.style.setProperty("--alert-theme-color", themeColor);

    btnEl.onclick = close;

    overlay.classList.add("visible");
  }

  return { render };
})();