import json
import httpx
import asyncio
import functools
from loguru import logger


class Retry:
    @staticmethod
    def async_retry(max_retries=3, _log='函数运行', success_log=True, is_assert=False):
        def decorator(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                for count in range(max_retries):
                    try:
                        result = await func(*args, **kwargs)
                        if success_log:
                            logger.success(f"{_log} 成功: {func.__name__} {json.dumps([str(i) for i in args])}")
                        return result
                    except Exception as e:
                        logger.error(f"{_log} __{func.__name__}__ 失败 {count}: {str(e)}")

                logger.critical(
                    f"{_log} __{func.__name__}__ 失败: 已重试{max_retries}次, 内容记录：{func.__name__} {json.dumps([str(i) for i in args])}")
                if is_assert:
                    assert False, f"{_log} __{func.__name__}__ 失败: 已重试{max_retries}次, 内容记录：{func.__name__} {json.dumps([str(i) for i in args])}"

            return async_wrapper

        return decorator

    @staticmethod
    def sync_retry(max_retries=3, _log='函数运行', success_log=False, is_assert=False):
        def decorator(func):
            @functools.wraps(func)
            def async_wrapper(*args, **kwargs):
                for count in range(max_retries):
                    try:
                        result = func(*args, **kwargs)
                        if success_log:
                            logger.success(f"{_log} 成功: {func.__name__} {json.dumps([str(i) for i in args])}")
                        return result
                    except Exception as e:
                        logger.error(f"{_log} __{func.__name__}__ 失败{count}: {str(e)}")

                logger.critical(
                    f"{_log} __{func.__name__}__ 失败: 已重试{max_retries}次, 内容记录：{func.__name__} {json.dumps([str(i) for i in args])}")
                if is_assert:
                    assert False, f"{_log} __{func.__name__}__ 失败: 已重试{max_retries}次, 内容记录：{func.__name__} {json.dumps([str(i) for i in args])}"

            return async_wrapper

        return decorator


class AsyncSpider:
    def __init__(self, proxies=None, timeout=10):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/102.0.0.0 Safari/537.36"
        }
        self.proxies = proxies
        self.timeout = timeout

    @Retry.async_retry(max_retries=3, _log='Get网络请求',success_log=False)
    async def _get_request(self, url: str, params=None):
        async with httpx.AsyncClient(proxies=self.proxies, verify=False) as client:
            response = await client.get(url, headers=self.headers, timeout=self.timeout, params=params)
            return response

    @Retry.async_retry(max_retries=3, _log='Post网络请求',success_log=False)
    async def _post_request(self, url: str, data=None, _json=None):
        async with httpx.AsyncClient(proxies=self.proxies, verify=False) as client:
            response = await client.post(url, headers=self.headers, timeout=self.timeout, data=data, json=_json)
            return response
