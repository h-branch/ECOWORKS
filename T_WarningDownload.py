import requests


url='https://apihub.kma.go.kr/api/typ01/url/wrn_met_data.php?'

option={
    'reg': '0',
    'wrn': 'A',
    'tmfc1': '202401010000',
    'tmfc2': '202501010000',
    'disp': '0',
    'help': '1',
    'authKey': 'R3WTydcASuG1k8nXABrhgA'
}

response=requests.get(url, option)

f_path='D:/python/0.work/240715_WarningCheck/24_warning.txt'
with open(f_path, 'wb') as file:
    file.write(response.content)

print(f'데이터 저장 완료: {f_path}')
