import subprocess

from codinit.logger import colorize

# ======================================================================
# W&B utils
# ======================================================================

def sync_wandb(folder, timeout=None):
    folder = folder.strip('/files')
    print(colorize('\nSyncing %s to wandb' % folder), bold=True)
    run_bash_cmd('wandb sync %s' % folder, timeout)

def run_bash_cmd(cmd, timeout=None):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    try:
        output, error = process.communicate(timeout=timeout)
    except:
        pass
