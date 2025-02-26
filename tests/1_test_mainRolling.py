import pytest
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging

#####
### 구현 단계 x 
#####

@function_logging
async def check_mainPageBanner_KR(settings, test_logger):
        #test_logger.console(f"메인롤링[KR] - #NaN")
        return True

@function_logging
async def check_mainPageBanner_EN(settings, test_logger):
        #test_logger.console(f"메인롤링[EN] - #NaN")
        return True

@module_logging
@pytest.mark.asyncio
async def test_mainRolling(settings, test_logger):
    """
    """
    current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
    if not settings.should_run_module(current_module):  # 설정에 따라 모듈 실행 여부 확인
        pytest.skip("Module disabled in configuration")

        # 한국어 배너 확인
        await check_mainPageBanner_KR(settings, test_logger)
        
        # 영어 배너 확인
        await check_mainPageBanner_EN(settings, test_logger)
        
        # 전체 배너 확인이 이상이 없으면 로깅
        #test_logger.console(f"1. 메인롤링 - 이상 없음 #NaN")
    
