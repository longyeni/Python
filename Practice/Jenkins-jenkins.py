#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jenkins
import time
import jenkinsapi
import re
from http.client import HTTPConnection


def build_testjob(jenkins_server_url, user_id, api_token, job_name):
    server.build_job(job_name, {'test-parameter': user_id})
    starttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('Build start: %s' % starttime)
    #  等待构建完成
    jenkinsapi.api.block_until_complete(jenkins_server_url, [job_name], maxwait=120, interval=5, raise_on_timeout=True, username=user_id, password=api_token, ssl_verify=True)
    endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('Build complete: %s' % endtime)


def get_filesize(url):
    reg_site = re.compile(
        r"^(?:(?:http|https):\/\/)?([\w\-_]+(?:\.[\w\-_]+)+)", re.IGNORECASE)
    try:
        port = str(url).split(':')[2].split('/')[0]
    except Exception as e:
        port = ""
    hostname = reg_site.match(url).group(1)
    if len(port) > 1:
        hostname = hostname + ':' + port
    path = str(url).split(hostname)[1]
    try:
        conn = HTTPConnection(hostname)
        conn.request("GET", path)
    except Exception as e:
        print('connect error!')
    r = conn.getresponse()
    return r.getheader("content-length")


def print_buildinfo(jenkins_server_url, buildnumber, job_name):
    if not server.get_build_info(job_name, buildnumber)['building']:
        buildinfo = server.get_build_info(job_name, buildnumber)
        buildresult = buildinfo['result']
        print('Build result: %s' % buildresult)
        builduser = buildinfo['actions'][1]['causes'][0]['userId']
        print('Build user: %s' % builduser)
        builddate = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(buildinfo['timestamp']/1000))
        print('Build date: %s' % builddate)
        buildtime = buildinfo['estimatedDuration']
        print('Build time: %ss' % (buildtime/1000))
        if buildinfo['artifacts']:
            buildfile = buildinfo['artifacts']
            print('Build Files:')
            for filenames in buildfile:
                filename = filenames['fileName']
                url = str('%s/job/%s/%s/artifact/%s' % (
                    jenkins_server_url, job_name, buildnumber, filename))
                filesize = get_filesize(url)
                print('-- %s  %s' % (filename, filesize))
        else:
            print('No any artifact')


if __name__ == '__main__':
    jenkins_server_url = 'http://10.10.11.8:8080'
    user_id = input('Please input username:')
    api_token = input('Please input password:')
    job_name = 'Tester_4ALL'
    server = jenkins.Jenkins(
        jenkins_server_url, username=user_id, password=api_token)
    build_testjob(jenkins_server_url, user_id, api_token, job_name)
    buildnumber = server.get_job_info(job_name)['lastBuild']['number']
    print('Build number: %s' % buildnumber)
    print_buildinfo(jenkins_server_url, buildnumber, job_name)
