const sftpApi = {
  listDir: (path) => window.pywebview.api.sftp_list_dir(path),

  download: (remotePath, filename) => window.pywebview.api.sftp_download(remotePath, filename),

  upload: (remoteDir) => window.pywebview.api.sftp_upload(remoteDir),
};