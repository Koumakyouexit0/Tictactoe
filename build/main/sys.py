import os
import subprocess
import platform
import psutil
import requests
import geocoder

def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        if response.status_code == 200:
            ip_info = response.json()
            return ip_info.get('origin')
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None

def get_cpu_info():
    try:
        return platform.processor()
    except Exception as e:
        print(f"Error getting CPU info: {e}")
        return "Unknown"

def get_ram_info():
    try:
        mem = psutil.virtual_memory()
        return f"{mem.total / (1024**3):.2f} GB"
    except Exception as e:
        print(f"Error getting RAM info: {e}")
        return "Unknown"

def get_disk_info():
    try:
        partitions = psutil.disk_partitions()
        disk_info = []
        for partition in partitions:
            if os.name == 'nt':  
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append(f"{partition.device} - {partition_usage.total / (1024**3):.2f} GB")
            else: 
                disk_info.append(f"{partition.device} - {psutil.disk_usage(partition.mountpoint).total / (1024**3):.2f} GB")
        return disk_info
    except Exception as e:
        print(f"Error getting disk info: {e}")
        return ["Unknown"]

def get_gpu_info():
    try:
        gpu_info = []
        if os.name == 'nt':  
            command = 'wmic path win32_videocontroller get caption'
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:
                gpu_info.append(line.strip())
        else: 
            gpu_info.append("Not implemented for Unix/Linux")
        return gpu_info
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return ["Unknown"]

def get_user_info():
    try:
        return os.getlogin() if os.name == 'nt' else os.getenv('USER')
    except Exception as e:
        print(f"Error getting user info: {e}")
        return "Unknown"

def get_computer_model():
    try:
        result = subprocess.Popen(['wmic', 'csproduct', 'get', 'name'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output, error = result.communicate()
        if result.returncode == 0:
            model = output.decode('utf-8').strip().split('\r\r\n')[1].strip()
            return model
        else:
            print(f"Error: {error.decode('utf-8')}")
            return "Unable to retrieve"
    except Exception as e:
        print(f"Error getting computer model: {e}")
        return "Unable to retrieve"

def get_ip_info(ip_address):
    try:
        g = geocoder.ip(ip_address)
        if g.ok:
            return g.json 
        else:
            return None
    except Exception as e:
        print(f"Error getting IP info: {e}")
        return None

def write_to_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing to file '{filename}': {e}")

def main():
    ip_address = get_public_ip()
    if ip_address:
        ip_info = get_ip_info(ip_address)
        if ip_info:
            cpu_info = get_cpu_info()
            ram_info = get_ram_info()
            disk_info = get_disk_info()
            gpu_info = get_gpu_info()
            user_info = get_user_info()
            computer_model = get_computer_model()

            content = f"Địa chỉ IP công khai: {ip_address}\n\n"
            content += f"Thông tin chi tiết từ địa chỉ IP:\n"
            content += f"IP Address: {ip_info['ip']}\n"
            content += f"Country: {ip_info.get('country', 'Unknown')}\n"
            content += f"Region: {ip_info.get('region', 'Unknown')}\n"
            content += f"City: {ip_info.get('city', 'Unknown')}\n"
            content += f"Latitude: {ip_info.get('lat', 'Unknown')}\n"
            content += f"Longitude: {ip_info.get('lng', 'Unknown')}\n"
            content += f"ISP: {ip_info.get('org', 'Unknown')}\n"
            content += f"ASN: {ip_info.get('asn', 'Unknown')}\n\n"

            content += f"Thông tin cấu hình máy tính:\n"
            content += f"CPU: {cpu_info}\n"
            content += f"RAM: {ram_info}\n"
            content += f"Ổ đĩa:\n"
            for disk in disk_info:
                content += f"- {disk}\n"
            content += f"GPU:\n"
            for gpu in gpu_info:
                content += f"- {gpu}\n"
            content += f"Tài khoản người dùng: {user_info}\n"
            content += f"Model máy tính: {computer_model}\n"

            filename = "build/main/info.txt"
            if not os.path.exists(filename):
                write_to_file(filename, content)
        exit()

if __name__ == "__main__":
    main()
