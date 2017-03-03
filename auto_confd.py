#!/usr/bin/env python
# coding: utf-8
import os, sys, time, commands, logging


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    logging.basicConfig(filename="./auto_conf.log", level=logging.DEBUG)
    try:
        # 程序分成两个不同的进程 同时执行下面的代码
        # 在子进程内 fork方法会返回0
        # 在父进程内 fork方法会返回子进程的编号PID
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        # sys.stderr.write("1st fork failed: %d %s\n" % (e.errno, e.strerror))
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
        # sys.stderr.write("2nd fork failed: %d %s\n" % (e.errno, e.strerror))
        logging.debug("2nd fork failed: %d %s\n" % (e.errno, e.strerror))
        sys.exit(1)


def main():
    from time import sleep
    try:
        sys.stdout.write("[%s]:auto config start" % (time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))))
        commands.getstatusoutput("bash rebuild.sh")
        nginx_time = os.stat("nginx.json").st_mtime
        rinetd_time = os.stat("rinetd.json").st_mtime
        # sys.stdout.write("[%s]:rebuilding succeed!" % (time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))))
        logging.debug("[%s]:first building succeed!" % (time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))))
        while 1:
            sleep(30)
            if os.stat("nginx.json").st_mtime != nginx_time or os.stat("rinetd.json").st_mtime != rinetd_time:
                commands.getstatusoutput("bash rebuild.sh")
                nginx_time = os.stat("nginx.json").st_mtime
                rinetd_time = os.stat("rinetd.json").st_mtime
                logging.debug(
                    "[%s]:rebuilding succeed!" % (time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))))
                # sys.stdout.write(
                # "[%s]:rebuilding succeed!" % (time.strftime('%Y-%m-%d %H%M%S', time.localtime(time.time()))))

    except Exception, e:
        # sys.stderr.write("error while rebuilding\n")
        logging.debug("error while rebuilding\n")


if __name__ == '__main__':
    daemonize('/dev/null', '/home/strrl/output.log', '/home/strrl/error.log')
    main()
