import urllib3
import os
import re
import requests
import argparse
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def display_banner():
    banner = r"""
 _______  _______  _______  ______   _______           _        _        _______  _______  ______  
(  ___  )(  ____ \(  ____ \(  __  \ (  ___  )|\     /|( (    /|( \      (  ___  )(  ___  )(  __  \ 
| (   ) || (    \/| (    \/| (  \  )| (   ) || )   ( ||  \  ( || (      | (   ) || (   ) || (  \  )
| |   | || (_____ | (_____ | |   ) || |   | || | _ | ||   \ | || |      | |   | || (___) || |   ) |
| |   | |(_____  )(_____  )| |   | || |   | || |( )| || (\ \) || |      | |   | ||  ___  || |   | |
| |   | |      ) |      ) || |   ) || |   | || || || || | \   || |      | |   | || (   ) || |   ) |
| (___) |/\____) |/\____) || (__/  )| (___) || () () || )  \  || (____/\| (___) || )   ( || (__/  )
(_______)\_______)\_______)(______/ (_______)(_______)|/    )_)(_______/(_______)|/     \|(______/ 
                                                                                                   
	"""
    print(banner)
    print("-------------------------------------\n-----Created by ApexSecLabs/h3ky-----\n-------------------------------------\n\n")

def fetch_keys_with_regex(base_url):
    response = requests.get(base_url, verify=False)
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return []

    key_pattern = re.compile(r'<Key>(.*?)</Key>', re.DOTALL)
    keys = key_pattern.findall(response.text)
    
    return keys

def download_file(base_url, key, save_path='.'):
    url = base_url + key
    print(f"请求URL: {url}")
    
    response = requests.get(url, stream=True, verify=False)
    
    file_name = os.path.basename(key.strip('/'))
    if not file_name:  # 如果文件名为空，跳过该文件
        print(f"无效的文件路径: {key}, 跳过此文件")
        return
    
    filename = os.path.join(save_path, file_name)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
        print(f"文件 {filename} 下载完成")
    else:
        print(f"下载失败：{url}, 状态码：{response.status_code}. 响应内容: {response.text}")

def main():
    display_banner()
    parser = argparse.ArgumentParser(description='OSS文件下载工具')
    parser.add_argument('-u', '--url', required=True, help='目标网站的URL')
    args = parser.parse_args()
    
    base_url = args.url
    if not base_url.endswith('/'):
        base_url += '/'
    
    parsed_url = urlparse(base_url)
    domain_name = parsed_url.netloc
    if not domain_name:
        print("错误: 无法从URL中提取域名")
        return
    
    save_directory = f'./{domain_name}'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        print(f"创建文件夹: {save_directory}")
    
    keys = fetch_keys_with_regex(base_url)
    if not keys:
        print("未找到任何文件键值。")
        return
    
    for key in keys:
        if "导出文件" not in key:
            download_file(base_url, key, save_directory)

if __name__ == "__main__":
    main()
