import http.client
import threading
import os

thread_num=2
#host = "10.0.4.101:8080"
host = "192.168.0.124:1935"
concurrent_user=2
base_url = "/vod/mp4:sample.mp4/"
#base_url = "/B120156699_EPI0001_02_t33.mp4/"


def request_ts(id):
    body = None
    headers = {"Host": "origin.media.com"}

    # conn = http.client.HTTPConnection(host)
    # conn.request("GET", base_url + "playlist.m3u8" , body, headers)
    # res = conn.getresponse()

    conn=[]
    res=[]
    for i in range(0, concurrent_user):
        conn.append( http.client.HTTPConnection(host) )
        conn[i].request("GET", base_url + "playlist.m3u8" , body, headers)
        res.append( conn[i].getresponse() )
        if i==0:
            m3u8 = res[i].read()
        else:
            res[i].read()

    m3u8 = m3u8.decode('utf-8')
    m3u8=m3u8.split('\n')[-2]

    url = base_url + m3u8

    conn[0].request('GET', url, body, headers)
    res[0] = conn[0].getresponse()

    m3u8 = res[0].read()
    m3u8 = m3u8.decode('utf-8')
    m3u8=m3u8.split('\n')

    i=0
    ts=[]
    while True:
        if m3u8[i][0] != '#':
            ts.append(base_url + m3u8[i])
        if m3u8[i] == '#EXT-X-ENDLIST':
            break
        i+=1 

    while True:
        for i in ts:
            for j in range(0, concurrent_user):
               # session_id = str(os.getpid()) + ' ' + str(j)
                session_id = str( threading.get_ident() ) + ' ' + str(j)
                headers = {"Host": "origin.media.com", "user-agent": session_id }
                conn[j].request('GET', i, body, headers )
                res[j] = conn[j].getresponse() 
                res[j].read()
                print( session_id +' ' + str(res[j].status) + ' ' + i)

for i in range(0,thread_num):
    th = threading.Thread(target=request_ts, args=(i, ) )    
    th.start()