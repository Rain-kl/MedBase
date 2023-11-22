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
        self.status_dict={
            200: '请求成功',
            201: '创建成功',
            202: '更新成功',
            204: '删除成功',
            400: '请求失败',
            401: '未授权',
            403: '禁止访问',
            404: '未找到',
            406: '请求格式错误',
            410: '请求资源不存在',
            422: '请求参数错误',
            500: '服务器错误',
            502: '网关错误',
            503: '服务不可用',
            504: '网关超时',
        }

    @Retry.async_retry(max_retries=3, _log='Get网络请求',success_log=False)
    async def _get_request(self, url: str, params=None):
        async with httpx.AsyncClient(proxies=self.proxies, verify=False) as client:
            response = await client.get(url, headers=self.headers, timeout=self.timeout, params=params)
            if response.status_code != 200:
                logger.error(f'请求失败: {response.status_code} {self.status_dict[response.status_code]}')
            return response

    @Retry.async_retry(max_retries=3, _log='Post网络请求',success_log=False)
    async def _post_request(self, url: str, data=None, _json=None):
        async with httpx.AsyncClient(proxies=self.proxies, verify=False) as client:
            response = await client.post(url, headers=self.headers, timeout=self.timeout, data=data, json=_json)
            if response.status_code != 200:
                logger.error(f'请求失败: {response.status_code} {self.status_dict[response.status_code]}')
            return response
