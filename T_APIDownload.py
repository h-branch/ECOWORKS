import requests
import datetime


Key='R3WTydcASuG1k8nXABrhgA'
hsr_url='https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-rdr_cmp1_api?'
asos_url='https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd.php?'
aws_grid_url='https://apihub.kma.go.kr/api/typ01/cgi-bin/aws/nph-aws_min_obj?'


def hsr_download():
# ※코드 수행 전 기간, 저장 간격 수정 필요※
    _start=datetime.datetime(2019,7,15,15) #기간 시작 시점
    _end=datetime.datetime(2019,7,15,16) #기간 종료 시점
    _int=datetime.timedelta(hours=1) #저장 간격

    while _start<=_end:
        _temp=_start.strftime('%Y%m%d%H') #*.strftime(): datetime → 문자열 출력

        _option={
            'tm': _temp,
            'cmp': 'PCPH',
            'qcd': 'KMA',
            'obs': 'ECHO',
            'acc': '180', #누적기간(분)
            'map': 'HB', #한반도(기본)
            'disp': 'B',
            'authKey': Key
        }

        _response=requests.get(hsr_url, _option)

        _f_path=f'D:/이현지/2. 진종훈 팀장님/#2. 내배수/240904 사례집 강우사상 수집/3hrPCPH_{_temp}.bin' #저장 경로
        with open(_f_path, 'wb') as _f:
            _f.write(_response.content) #*.content: binary type 데이터 수집(구동) / *.text: UTF-8 인코딩 문자열 수집(구동 X)
        
        print(f'데이터 저장 완료: {_f_path}')

        _start += _int


def asos_download():
# ※코드 수행 전 기간, 저장 간격 수정 필요※
    _start=datetime.datetime(2023,1,1) #기간 시작 시점
    _end=datetime.datetime(2023,12,31) #기간 종료 시점
    _int=datetime.timedelta(days=1) #저장 간격

    while _start<=_end:
        _temp=_start.strftime('%Y%m%d')

        _option={
            'tm': _temp,
            # 하기 옵션은 기상청 API허브 인자 참조
            'stn': '0', #전 지점
            'help': '0', #도움말 없음
            'authKey': Key
        }

        _response=requests.get(asos_url, _option)

        _f_path=f'C:/Users/lhj15/OneDrive/바탕 화면/study/240804 API data/Data/API{save}.txt'
        with open(_f_path,'wb') as _f:
            _f.write(_response.content)

        print(f'데이터 저장 완료: {_f_path}')

        _start += _int


def aws_grid_download():
# ※코드 수행 전 기간, 저장 간격 수정 필요※
    _start=datetime.datetime(2019,7,15,15,15) #기간 시작 시점
    _end=datetime.datetime(2019,7,15,16,15) #기간 종료 시점
    _int=datetime.timedelta(hours=1) #저장 간격

    while _start<=_end:
        _temp=_start.strftime('%Y%m%d%H%M')

        _option={
            'obs': 'rn_60m', #rn_60m, rn_03h, rn_06h
            'tm': _temp,
            'stn': '0',
            'obj': 'mq',
            'map': 'D3',
            'grid': '0.5',
            'gov': '',
            'authKey': Key
        }

        _response=requests.get(aws_grid_url, _option)

        _f_path=f'D:/이현지/2. 진종훈 팀장님/#2. 내배수/241008 피해지점 및 인근 관측소 매칭/241010 사례집 다운로드/1hrAwsGrid_{_temp}.txt'
        with open(_f_path, 'wb') as _f:
            _f.write(_response.content)

        print(f'데이터 저장 완료: {_f_path}')

        _start += _int
