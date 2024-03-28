from datetime import datetime, timezone, timedelta
from typing import Union

import pytz


def get_utc_to_13d(date_time: datetime = None) -> int:
    """
    현재시간(또는 파라미터로 받은 특정시간)을 utc timestamp milli second(13자리) 단위로 리턴한다.
    :param date_time: 변환을 원하는 시간 datetime 객체(None 인 경우 현재 시간)
    :return: utc 13자리 int
    """
    if date_time is None:
        date_time = datetime.now(timezone.utc)
    if not isinstance(date_time, datetime):
        raise Exception('The parameter requires a datetime type.')
    return int(date_time.replace(tzinfo=timezone.utc).timestamp() * 1000)


def get_13d_to_utc(timestamp: int) -> datetime:
    """
    utc timestamp milli second(13자리) 값을 datetime 객체로 변환한다.
    :param timestamp:  utc timestamp milli second(13자리)
    :return: datetime 객체
    """
    if not isinstance(timestamp, int):
        raise Exception('The parameter requires a int type.')
    return datetime.fromtimestamp(timestamp / 1000, timezone.utc)


def get_utc_to_10d(date_time=None):
    """
    현재시간(또는 파라미터로 받은 특정시간)을 utc timestamp second(10자리) 단위로 리턴한다.
    :param date_time: 변환을 원하는 시간 datetime 객체(None 인 경우 현재 시간)
    :return: utc 10자리 int
    """
    if date_time is None:
        date_time = datetime.now(timezone.utc)

    if not isinstance(date_time, datetime):
        raise Exception('The parameter requires a datetime type.')
    return int(date_time.replace(tzinfo=timezone.utc).timestamp())


def get_10d_to_utc(timestamp: int) -> datetime:
    """
    utc timestamp second(10자리) 값을 datetime 객체로 변환한다.
    :param timestamp:  utc timestamp second(10자리)
    :return: datetime 객체
    """
    if not isinstance(timestamp, int):
        raise Exception('The parameter requires a int type.')
    return datetime.fromtimestamp(timestamp, timezone.utc)


def get_utc_after_secs(secs: int) -> datetime:
    """
    현재 시간에 seconds 를 더한 utc datetime 를 반환한다.
    :param secs:  초
    :return: datetime 객체
    """
    return datetime.now(timezone.utc) + timedelta(seconds=secs)


def get_utc_before_secs(secs: int) -> datetime:
    """
    현재 시간에 seconds 를 뺀 utc datetime 를 반환한다.
    :param secs:  초
    :return: datetime 객체
    """
    return datetime.now(timezone.utc) - timedelta(seconds=secs)


def get_utc_after_days(days: int) -> datetime:
    """
    현재 시간에 days 를 더한 utc datetime 를 반환한다.
    :param days:  일
    :return: datetime 객체
    """
    return datetime.now(timezone.utc) + timedelta(days=days)


def get_utc_before_days(days: int) -> datetime:
    """
    현재 시간에 days 를 뺀 utc datetime 를 반환한다.
    :param days:  일
    :return: datetime 객체
    """
    return datetime.now(timezone.utc) - timedelta(days=days)


def get_utc_to_10d_after_secs(secs: int) -> int:
    """
    현재 시간에 seconds 를 더한 utc timestamp 10자리(seconds) 반환한다.
    :param secs:  초
    :return: utc timestamp 10자리
    """
    utc_after_secs = get_utc_after_secs(secs)

    return get_utc_to_10d(utc_after_secs)


def get_utc_to_10d_before_secs(secs: int) -> int:
    """
    현재 시간에 seconds 를 뺀 utc timestamp 10자리(seconds) 반환한다.
    :param secs:  초
    :return: utc timestamp 10자리
    """
    utc_before_secs = get_utc_before_secs(secs)

    return get_utc_to_10d(utc_before_secs)


def get_utc_to_13d_after_days(days: int) -> int:
    """
    현재 시간에 days 를 더한 utc timestamp 13자리(milli seconds) 반환한다.
    :param days:  일
    :return: utc timestamp 13자리
    """
    utc_after_days = get_utc_after_days(days)

    return get_utc_to_13d(utc_after_days)


def get_utc_to_13d_before_days(days: int) -> int:
    """
    현재 시간에 days 를 뺀 utc timestamp 13자리(milli seconds) 반환한다.
    :param days:  일
    :return: utc timestamp 13자리
    """
    utc_before_days = get_utc_before_days(days)

    return get_utc_to_13d(utc_before_days)


def get_now(zone: str = None) -> datetime:
    """
    특정존의 현재 시간 datetime 객체를 반환한다.
    :param zone: zone 문자열 (기본값 UTC)
    :return: datetime 객체
    """
    if zone:
        now = datetime.now(pytz.timezone(zone))
    else:
        now = datetime.now(timezone.utc)
    return now


def get_local_now() -> datetime:
    """
    현재존의 현재 시간 datetime 객체를 반환한다.
    :return: datetime 객체
    """
    return datetime.now()


def get_now_str(zone: str = None, time_fmt: str = '%Y-%m-%d') -> str:
    """
    특정존의 현재 날짜의 문자열을 반환한다.
    :param zone: zone 문자열 (기본값 UTC)
    :param time_fmt: 날짜 포매팅 문자열(기본값 %Y-%m-%d)
    :return: 포맷팅된 날짜 문자열 객체
    """
    return get_now(zone).strftime(time_fmt)


def get_local_now_str(time_fmt: str = '%Y-%m-%d') -> str:
    """
    현재 존 현재 날짜의 문자열을 반환한다.
    :param time_fmt: 날짜 포매팅 문자열(기본값 %Y-%m-%d)
    :return: 포맷팅된 날짜 문자열 객체
    """
    return get_local_now().strftime(time_fmt)


def get_weekday_ko(weekday: int) -> str:
    """
    숫자를 요일 텍스트로 변환한다.
    :param weekday: 요일을 나타내는 숫자(1~7)
    :return: 요일 텍스트(월~일)
    """
    week_day_dict = {
        1: '월',
        2: '화',
        3: '수',
        4: '목',
        5: '금',
        6: '토',
        7: '일',
    }
    return week_day_dict[weekday]


def get_local_str_to_datetime(local_date: str, dt_fmt: str = '%Y-%m-%d') -> datetime:
    """
    로컬 존에 특정 포맷으로 표시된 날짜 문자열을 datetime 객체로 변환한다.
    :param local_date: 로컬존에서 표현된 날짜 문자열(기본값 %Y-%m-%d)
    :param dt_fmt : 날짜 포맷팅 문자열
    :return: 변환된 datetime
    """
    return datetime.strptime(local_date, dt_fmt)


def get_utc_str_to_datetime(local_date: str, dt_fmt: str = '%Y-%m-%d') -> datetime:
    """
    UTC 특정 포맷으로 표시된 날짜 문자열을 datetime 객체로 변환한다.
    :param local_date: UTC 에서 표현된 날짜 문자열(기본값 %Y-%m-%d)
    :param dt_fmt : 날짜 포맷팅 문자열
    :return: 변환된 datetime
    """
    return get_local_str_to_datetime(local_date, dt_fmt).astimezone(pytz.utc)


def transform_datetime(src: Union[str, datetime],
                       dst_type: Union[type(str), type(datetime)],
                       src_str_format: str = None, dst_str_format: str = None,
                       src_timezone: str = None, dst_timezone: str = None):
    """
    날짜를 표현하는 str 또는 datetime을 입력으로 받아서, 원하는 포맷과 타임존이 적용 된 str 또는 datetime을 반환한다.
    타임존 기본값은 UTC이다. 예제는 이 파일 하단에 표기함

    :param src: 입력 객체. str 또는 datetime
    :param src_str_format: 입력 str 표기 형식. src type이 str일 때만 사용 할 것.
    :param src_timezone: 입력 타임존(Asia/Seoul, US/Eastern, ...). src type이 str일 때만 사용 할 것.
    :param dst_type: 출력 객체 타입
    :param dst_str_format: 출력이 str일 때 포맷. 출력이 str 타입일 때만 사용 할 것.
    :param dst_timezone: 출력 타임존(Asia/Seoul, US/Eastern, ...). 파라메터 생략 시: src 타임존으로 적용
    """

    if dst_type not in [str, datetime]:
        raise Exception('dst_type must be one of [str, datetime]')

    if type(src) == str:
        dt_src = datetime.strptime(src, src_str_format)
        dt_src = pytz.timezone(src_timezone or 'UTC').localize(dt_src)
    elif type(src) == datetime:
        dt_src: datetime = src
        if not dt_src.tzinfo:
            dt_src = pytz.timezone(src_timezone or 'UTC').localize(src)
        elif src_timezone:
            raise Exception('src_timezone must be None if src is datetime')
    else:
        raise Exception('Type of src must be one of [str, datetime]')

    dt_dst = dt_src
    if dst_timezone:
        dt_dst = dt_src.astimezone(pytz.timezone(dst_timezone))

    if dst_type == str:
        if not dst_str_format:
            raise Exception('dst_str_format must be specified')
        return dt_dst.strftime(dst_str_format)
    elif dst_type == datetime:
        return dt_dst


if __name__ == '__main__':
    # utc now datetime
    print('현재 utc datetime', get_now())
    print('현재 utc YYYY-mm-dd', get_now_str())

    # asia/seoul now datetime
    print('현재 asia/seoul datetime', get_now('Asia/Seoul'))
    print('헌재 asia/seoul YYYY-mm-dd', get_now_str('Asia/Seoul'))

    # local now datetime
    print('현재 local datetime', get_local_now())
    print('현재 local YYYY-mm-dd', get_local_now_str())

    # utc now timestamp 13 예제
    utc13 = get_utc_to_13d()
    print('현재 utc timestamp(13)', utc13)
    print('현재 utc datetime', get_13d_to_utc(utc13))

    # utc now timestamp 10 예제
    utc10 = get_utc_to_10d()
    print('현재 utc timestamp(10)', utc10)
    print('현재 utc datetime', get_10d_to_utc(utc10))

    # 초, 일 전/후 datetime
    print('현재 utc 보다 10 초 후 datetime', get_utc_after_secs(10))
    print('현재 utc 보다 10 초 전 datetime', get_utc_before_secs(10))
    print('현재 utc 보다 1일 후 datetime', get_utc_after_days(1))
    print('현재 utc 보다 1일 전 datetime', get_utc_before_days(1))

    # 일 전/후 timestamp(13)
    print('현재 utc 보다 1일 후 timestamp(13)', get_utc_to_13d_after_days(1))
    print('현재 utc 보다 1일 전 timestamp(13)', get_utc_to_13d_before_days(1))

    # 초 전/후 timestamp(10)
    print('현재 utc 보다 10 초 후 timestamp(10)', get_utc_to_10d_after_secs(10))
    print('현재 utc 보다 10 초 전 timestamp(10)', get_utc_to_10d_before_secs(10))

    # 문자열 -> datetime 변환
    print('문자열 로컬 타임 변환', get_local_str_to_datetime('2021-10-01'))
    print('문자열 UTC 타임 변환', get_utc_str_to_datetime('2021-10-01'))

    # transform_datetime
    dt_utc = datetime(year=2022, month=8, day=30, hour=20, tzinfo=timezone.utc)
    print('utc->seoul str', transform_datetime(src=dt_utc, dst_type=str, dst_str_format='%Y%m%d',
                                               dst_timezone='Asia/Seoul'))  # 20220831

    print('utc->seoul datetime', transform_datetime(src=dt_utc, dst_type=datetime,
                                                    dst_timezone='Asia/Seoul'))  # 2022-08-31 05:00:00+09:00

    print('str->datetime', transform_datetime(src='20220830',
                                              src_str_format='%Y%m%d',
                                              dst_type=datetime))  # 2022-08-30 00:00:00+00:00

    print('seoul str -> utc str', transform_datetime(src='2022.08.30 13:30:59', src_timezone='Asia/Seoul',
                                                     src_str_format='%Y.%m.%d %H:%M:%S', dst_timezone='UTC',
                                                     dst_type=str,
                                                     dst_str_format='%Y.%m.%d %H:%M:%S'))  # 2022.08.30 04:30:59
