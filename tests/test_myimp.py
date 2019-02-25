import mymodulename

import contextlib
import os
import signal
import sys
import time

# time in seconds to wait for an async call to return the expected value
ASYNC_WAIT_MAX = 10
ASYNC_POLL_TIME = 0.1

def test_run():
    myimp = mymodulename.MyImp()
    assert myimp.run() is True

def test_run_stdout(capsys):
    myimp = mymodulename.MyImp()
    assert myimp.run() is True
    captured = capsys.readouterr() # captures output up until this point
    assert captured.out == 'running\n'
    #with capsys.disabled():
    #    print('Debug tests')

def nottest_run_always(capsys):
    myimp = mymodulename.MyImp()
    myimp.run_always()

@contextlib.contextmanager
def background_server(capfd):
    myimp = mymodulename.MyImp()
    # Launching the server
    pid_server = os.fork()
    if not pid_server:  # Child code
        myimp.run_always()  # Blocking call (until signal.SIGINT)

    try:
        yield
    finally:
        # Closing the server
        #os.kill(pid_server, signal.SIGINT)
        pass

def test_run_always_background(capfd):
    with background_server(capfd):
        waited = 0
        captured = ''
        while True:
            captured += capfd.readouterr().out
            if '...' in captured:
                assert True
                return
            
            if waited > ASYNC_WAIT_MAX:
                break

            waited += ASYNC_POLL_TIME
            time.sleep(ASYNC_POLL_TIME)
            
        assert False