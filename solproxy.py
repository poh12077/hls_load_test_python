import http.client
import threading

thread_num=1
#host = 'origin.media.com:8080'
#host = "10.0.4.101:8080"
host = '192.168.111.101:8080'

def request_ts(id):
    # session_id=0
    # session_max = 1000
    body = None
    headers = {"Host": "origin.media.com"}
    conn = http.client.HTTPConnection(host)
    conn.request("GET", "/B120156699_EPI0001_02_t33.mp4/playlist.m3u8",body, headers)
    res = conn.getresponse()

    m3u8 = res.read()
    m3u8 = m3u8.decode('utf-8')
    m3u8=m3u8.split('\n')[-2]


    url = "/B120156699_EPI0001_02_t33.mp4/" + m3u8

    conn.request('GET', url, body, headers)
    res = conn.getresponse()

    m3u8 = res.read()
    m3u8 = m3u8.decode('utf-8')
    m3u8=m3u8.split('\n')


    i=0
    ts=[]
    while True:
        if m3u8[i][0] != '#':
            ts.append("/B120156699_EPI0001_02_t33.mp4/" + m3u8[i])
        if m3u8[i] == '#EXT-X-ENDLIST':
            break
        i+=1 


    while True:
        for i in ts:
            #headers = {"user-agent": str(session_id)}
            conn.request('GET', i, body, headers )
            res = conn.getresponse()
            res.read()
            # session_id +=1
            # if session_id == session_max:
            #     session_id = 0
            print( str(id) +' ' + str(res.status) + ' ' + i)
            break
    

# for i in range(0,thread_num):
#     th = threading.Thread(target=request_ts, args=(i, ) )    
#     th.start()

while True:
    th = threading.Thread(target=request_ts, args=(0, ) )    
    th.start()
    th.join()