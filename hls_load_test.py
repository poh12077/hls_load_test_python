import http.client
import threading

#lock = threading.Lock()
thread_num=3

def request_ts(id):

    conn = http.client.HTTPConnection("192.168.0.124:1935")

    conn.request("GET", "/vod/mp4:sample.mp4/playlist.m3u8")

    res = conn.getresponse()

    m3u8 = res.read()
    m3u8 = m3u8.decode('utf-8')
    m3u8=m3u8.split('\n')[-2]


    url = "/vod/mp4:sample.mp4/" + m3u8

    conn.request('GET', url)
    res = conn.getresponse()

    m3u8 = res.read()
    m3u8 = m3u8.decode('utf-8')
    m3u8=m3u8.split('\n')


    i=0
    ts=[]
    while True:
        if m3u8[i][0] != '#':
            ts.append("/vod/mp4:sample.mp4/" + m3u8[i])
        if m3u8[i] == '#EXT-X-ENDLIST':
            break
        i+=1 


    n=0
    while n<100:
        for i in ts:
            conn.request('GET', i )
            res = conn.getresponse()
            res.read()
            print( str(id) +' ' + str(res.status) + ' ' + i)
        n+=1    



for i in range(0,thread_num):
    th = threading.Thread(target=request_ts, args=(i, ) )    
    th.start()

