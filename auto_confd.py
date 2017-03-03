#!/usr/bin/env python
# coding: utf-8
import os, sys, time, commands, logging


def daemonize():
    logging.basicConfig(filename="./auto_conf.log", level=logging.DEBUG)
    try:
        # 程序分成两个不同的进程 同时执行下面的代码
        # 在子进程内 fork方法会返回0
        # 在父进程内 fork方法会返回子进程的编号PID
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        logging.debug("1st fork failed: %d %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # os.chdir("/")
    os.umask(0)
    os.setsid()  # ??????
    # 第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            logging.debug("pid: %d" % pid)
            sys.exit()
    except OSError, e:
        logging.debug("2nd fork failed: %d %s\n" % (e.errno, e.strerror))
        sys.exit(1)


def main():
    from time import sleep
    try:
        sys.stdout.write("[%s]:auto config start" % (time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))))
        commands.getstatusoutput("sudo bash rebuild.sh")
        nginx_time = os.stat("nginx.json").st_mtime
        rinetd_time = os.stat("rinetd.json").st_mtime
        logging.debug("[%s]:first building succeed!" % (time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))))
        while 1:
            sleep(30)
            if os.stat("nginx.json").st_mtime != nginx_time or os.stat("rinetd.json").st_mtime != rinetd_time:
                commands.getstatusoutput("sudo bash rebuild.sh")
                nginx_time = os.stat("nginx.json").st_mtime
                rinetd_time = os.stat("rinetd.json").st_mtime
                logging.debug(
                    "[%s]:rebuilding succeed!" % (time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))))

    except Exception, e:
        logging.debug(str(e.message))
        logging.debug("error while rebuilding\n")


if __name__ == '__main__':
    daemonize()
    main()
