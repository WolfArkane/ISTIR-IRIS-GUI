const sshApi = {
  connect: (host, username, password, cols, rows) =>
    window.pywebview.api.ssh_connect(host, username, password, cols, rows),

  sendInput: (data) => window.pywebview.api.ssh_send_input(data),

  resize: (cols, rows) => window.pywebview.api.ssh_resize(cols, rows),

  disconnect: () => window.pywebview.api.ssh_disconnect(),
};