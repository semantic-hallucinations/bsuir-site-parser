class ParsingLimiterConfig:
    SAVE_EXT = {
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".rtf",
        ".odt",
        ".dotx",
        ".djvu",
    }

    DROP_EXT = {
        ".html",
        ".jpg",
        ".jpeg",
        ".png",
        ".mp3",
        ".mp4",
        ".zip",
        ".rar",
        ".vsd",
        ".dwt",
        ".dotx",
        ".ttf",
        ".bin",
        ".htm",
        ".jsp",
        ".apk",
    }

    DROP_TOPICS = {"/impuls/", "/online/", "/virtualnaya-ekskursiya", "/news/"}
