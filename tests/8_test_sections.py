import pytest
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging

#####
### 집중 확인 세션 구현 x
#####

@function_logging
async def test_sections_KR(settings, test_logger):
    pass

@function_logging
async def test_sections_EN(settings, test_logger):
    pass

@module_logging
@pytest.mark.asyncio
async def test_browser(settings, test_logger):
    """
    """
    current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
    if not settings.should_run_module(current_module):  # 설정에 따라 모듈 실행 여부 확인
        pytest.skip("Module disabled in configuration")

        # 한국어 배너 확인
        await test_sections_KR(settings, test_logger)
        # 영어 배너 확인
        await test_sections_EN(settings, test_logger)
        
    