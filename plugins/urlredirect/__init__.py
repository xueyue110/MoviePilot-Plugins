import time

import requests

from app.plugins import _PluginBase
from typing import Any, List, Dict, Tuple
from app.log import logger
from app.schemas import NotificationType
from app import schemas


class UrlRedirect(_PluginBase):
    # 插件名称
    plugin_name = "UrlRedirect"
    # 插件描述
    plugin_desc = "访问指定url返回Header Location指定的地址。"
    # 插件图标
    plugin_icon = "https://raw.githubusercontent.com/thsrite/MoviePilot-Plugins/main/icons/synology.png"
    # 插件版本
    plugin_version = "1.0"
    # 插件作者
    plugin_author = "thsrite"
    # 作者主页
    author_url = "https://github.com/thsrite"
    # 插件配置项ID前缀
    plugin_config_prefix = "urlredirect_"
    # 加载顺序
    plugin_order = 30
    # 可使用的用户级别
    auth_level = 2

    # 任务执行间隔
    _enabled = False
    _notify = False
    _msgtype = None

    def init_plugin(self, config: dict = None):
        if config:
            self._enabled = config.get("enabled")
            self._notify = config.get("notify")
            self._msgtype = config.get("msgtype")

    def redirect(self, url: str, ua: str) -> schemas.Response:
        """
        发送通知
        """
        logger.info(f"收到请求 {url}")
        if self._enabled:
            headers = {
                "User-Agent": ua,
            }

            try:
                start_time = time.time()  # Record the start time
                response = requests.head(url, headers=headers, allow_redirects=True)
                end_time = time.time()  # Record the end time

                content_type = response.headers.get("Content-Type", "Unknown")
                duration = end_time - start_time  # Calculate the duration

                # Log the response status, Content-Type, and duration
                logger.info(
                    f"fetchStrmLastLink response.status: {response.status_code}, contentType: {content_type}, duration: {duration:.4f} seconds")

                logger.info(f"Last link: {response.url}")
                return schemas.Response(
                    success=True,
                    data={'url': response.url}
                )
            except requests.RequestException as e:
                logger.error(f"Request failed: {e}")

                return schemas.Response(
                    success=False,
                    message=str(e)
                )

    def get_state(self) -> bool:
        return self._enabled

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

    def get_api(self) -> List[Dict[str, Any]]:
        """
        获取插件API
        [{
            "path": "/xx",
            "endpoint": self.xxx,
            "methods": ["GET", "POST"],
            "summary": "API说明"
        }]
        """
        return [{
            "path": "/redirect",
            "endpoint": self.redirect,
            "methods": ["GET"],
            "summary": "UrlRedirect"
        }]

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """
        拼装插件配置页面，需要返回两块数据：1、页面配置；2、数据结构
        """
        # 编历 NotificationType 枚举，生成消息类型选项
        MsgTypeOptions = []
        for item in NotificationType:
            MsgTypeOptions.append({
                "title": item.value,
                "value": item.name
            })
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'notify',
                                            'label': '开启通知',
                                        }
                                    }
                                ]
                            },
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12
                                },
                                'content': [
                                    {
                                        'component': 'VSelect',
                                        'props': {
                                            'multiple': False,
                                            'chips': True,
                                            'model': 'msgtype',
                                            'label': '消息类型',
                                            'items': MsgTypeOptions
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                },
                                'content': [
                                    {
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'text': '群辉webhook配置http://ip:3001/api/v1/plugin/SynologyNotify/webhook?text=hello world。'
                                                    'text参数类型是消息内容。此插件安装完需要重启生效api。消息类型默认为手动处理通知。'
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                },
                                'content': [
                                    {
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'text': '如安装完插件后，群晖发送webhook提示404，重启MoviePilot即可。'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ], {
            "enabled": False,
            "notify": False,
            "msgtype": ""
        }

    def get_page(self) -> List[dict]:
        pass

    def stop_service(self):
        """
        退出插件
        """
        pass
