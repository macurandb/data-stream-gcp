import shutil
from tox import hookimpl

@hookimpl
def tox_runtest_post(venv):
    try:
        shutil.rmtree(venv.path)
    except Exception as e:
        print("An exception occurred while removing '{}':".format(venv.path))
        print(e)