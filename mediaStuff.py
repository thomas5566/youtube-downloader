import subprocess
import os


class Media():

    def __init__(self, filename):
        self.filename = filename

    # 檢查影片檔是否包含聲音
    def check_media(self):
        r = subprocess.Popen(["ffprobe.exe", self.filename],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                            # send data to stdin
                            # stdout and stderr read data
                            # .PIPE Special value that can be used as the stdin,
                            # stdout or stderr argument to Popen and indicates
                            # that a pipe to the standard stream should be opened.
                            # Most useful with Popen.communicate().
                            # .STDOUT Special value that can be used as the stderr argument to
                            # Popen and indicates that standard error should go
                            # into the same handle as standard output.
        out, err = r.communicate()
        # Popen.communicate()方法用於和子進程交互：發送數據到stdin，
        # 並從stdout和stderr讀數據，直到收到EOF。等待子進程結束。
        if (out.decode('utf-8').find('Audio') == -1):
            return -1 # 沒有聲音
        else:
            return 1