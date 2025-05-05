from .parsing_limits_config import ParsingLimiterConfig as PLC


class ParsingLimiter:
    @classmethod
    def in_save_extensions(url: str) -> bool:
        return any(url.endswith(ext) for ext in PLC.SAVE_EXT)

    @classmethod
    def in_drop_extensions(url: str) -> bool:
        return any(url.endswith(ext) for ext in PLC.DROP_EXT)

    @classmethod
    def in_drop_topics(url: str) -> bool:
        return any(topic in url for topic in PLC.DROP_TOPICS)
