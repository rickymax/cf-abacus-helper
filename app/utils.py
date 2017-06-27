import os
import json
import subprocess

def runcmd(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
           stderr=subprocess.PIPE, env=None, close_fds=True):
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=stdin,
                         stdout=stdout,
                         stderr=stderr,
                         env=env,
                         close_fds=close_fds)

    (out, err) = p.communicate()
    return (p.returncode, out, err)
