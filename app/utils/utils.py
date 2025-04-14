from datetime import timezone, datetime, timedelta


def beijing_time() -> datetime:
    """返回当前北京时间（UTC+8）"""
    return datetime.now(timezone.utc).astimezone(
        timezone(timedelta(hours=8))
    )


if __name__ == "__main__":
    print(beijing_time())
    print(datetime.now())

