import paramiko

host = "192.168.45.128"
username = "root"
password = "pnet"
command = "uname -a && whoami && uptime"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("جاري الاتصال بالـ VMware VM...")
    ssh.connect(host, port=22, username=username, password=password, timeout=5)
    
    # تنفيذ أمر سحب بيانات النظام (Telemetry)
    stdin, stdout, stderr = ssh.exec_command(command)
    
    telemetry_output = stdout.read().decode('utf-8')
    print("\n=== Observed Lab Evidence (Telemetry) ===")
    print(telemetry_output)
    
    ssh.close()
    print("تم الاتصال وإغلاقه بنجاح!")
except Exception as e:
    print("فشل الاتصال:", e)