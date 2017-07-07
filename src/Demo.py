import requests, threading, time

class Downloader():
    def __init__(self, url, nums, name):
        self.url = url
        self.nums = int(nums)
        self.name = name
        r_head = requests.head(self.url)
        self.size = int(r_head.headers['Content-Length'])
        print('File size: {} {}'.format(self.size, 'Bytes'))

        ## 分割成nums个块
    def get_segment(self):
        segments = []
        ## 每个块的大小
        length = int(self.size / self.nums)
        for i in range(self.nums):
            if i == self.nums - 1:
                segments.append((i * length, self.size))
            else:
                segments.append((i * length, (i + 1) * length - 1))
        return segments

    # 下载每一个线程
    def download(self, start, end):
        try:
            begin = time.time()
            headers = {'Range':'Bytes={} - {}'.format(start, end), 'Accept-Encoding':'*'}
            r_g = requests.get(self.url, headers=headers)
            self.file.seek(start)
            self.file.write(r_g.content)
            print('{} ended, speed is {:.1f} kb/s.'
                  .format(threading.current_thread().name,(end - start)/(time.time() - begin)/1024))
        except Exception as e:
            print(e)



    def run(self):
        with open(self.name, 'wb') as self.file:
            n = 0
            thread_list = []
            for seg in self.get_segment():
                start, end = seg
                print('thread {} start: {}, end: {}'.format(n, start, end))
                n += 1
                thread = threading.Thread(target = self.download, args = (start, end))
                thread.start()
                thread_list.append(thread)
            for i in thread_list:
                i.join()

if __name__ == '__main__':
    try:
        url ='http://dldir1.qq.com/qqfile/qq/QQ8.9.3/21169/QQ8.9.3.exe' 
        nums = 8
        name = 'yy.jpg'
        down = Downloader(url, nums, name)
        begin = time.time()
        down.run()
        print('Download {} successful, spend {:.1f}s'.format(name, time.time() - begin))
    except requests.exceptions.RequestException:
        print('Oops, this url is not legal, we can\'t handle it')
    except KeyError:
        print('Oops, this url is not legal, we can\'t handle it')
    except ValueError:
        print('Oops, this numbers is not digital.')


