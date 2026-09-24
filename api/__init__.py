from .api import Api
from .vpnApi import VpnApi
from .sshAPI import SshApi
from .sftpApi import SftpApi

class CombinedAPI(Api, VpnApi, SshApi, SftpApi):
    pass