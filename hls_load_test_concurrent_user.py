import http.client
import threading

thread_num=1
#host = "10.0.4.101:8080"
host = "192.168.0.124:1935"
socket_num=5
base_url = "/vod/mp4:sample.mp4/"
#base_url = "/B120156699_EPI0001_02_t33.mp4/"

def request_ts(id):
    # session_id=0
    # session_max = 1000
    body = None
    headers = {"Host": "origin.media.com"}

    # conn = http.client.HTTPConnection(host)
    # conn.request("GET", base_url + "playlist.m3u8" , body, headers)
    # res = conn.getresponse()

    conn_list=[]
    res_list=[]
    for i in range(0,socket_num):
        conn_list.append(http.client.HTTPConnection(host))
        conn_list[i].request("GET", base_url + "playlist.m3u8" , body, headers)
        res_list.append( conn_list[i].getresponse() )
        m3u8 = res_list[i].read()


    #m3u8 = res_list[0].read()
    m3u8 = m3u8.decode('utf-8')
    m3u8=m3u8.split('\n')[-2]

    url = base_url + m3u8

    conn_list[0].request('GET', url, body, headers)
    res_list[0] = conn_list[0].getresponse()

    m3u8 = res_list[0].read()
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
            #headers = {"user-agent": str(session_id)}
            # conn.request('GET', i, body, headers )
            # res = conn.getresponse()
            # res.read()

            for j in range(0,socket_num):
                conn_list[j].request('GET', i, body, headers )
                res_list[j] = conn_list[j].getresponse() 
                res_list[j].read()
                print( str(id) +' ' + str(res_list[j].status) + ' ' + i)
            # session_id +=1
            # if session_id == session_max:
            #     session_id = 0
            
            #print( str(id) +' ' + str(res.status) + ' ' + i)



for i in range(0,thread_num):
    th = threading.Thread(target=request_ts, args=(i, ) )    
    th.start()