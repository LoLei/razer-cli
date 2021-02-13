import sys

import razer_cli
from razer_cli.razer_cli import util
from razer_cli.razer_cli.handler.handler import Handler


class VersionHandler(Handler):
    def handle(self):
        print("razer-cli:", self.version)
        print("   Installed in:",
              util.os.path.dirname(util.os.path.realpath(razer_cli.__file__)))
        print("python3-openrazer:", self.device_manager.version)
        print("openrazer-daemon:", self.device_manager.daemon_version)
        print("Python:",
              '.'.join([str(sys.version_info.major), str(sys.version_info.minor), str(sys.version_info.micro)]))
