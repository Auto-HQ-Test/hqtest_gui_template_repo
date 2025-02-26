import pytest
import asyncio
import random
import re
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging

#####
### 구현 완료
#####

@function_logging
async def check_newsLetter_KR(settings, test_logger):

        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기

        url = "https://www.fasoo.com/?lang=kr"
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True
    
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    headless=settings.get_module_options(current_module)['headless'],    
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)

                 # 상단 배너에서 뉴스 & 이벤트 
                news_button = page.get_by_label("뉴스 & 이벤트").get_by_role("link", name="뉴스 & 이벤트")
                await expect(news_button).to_be_visible()
                await news_button.hover()
                await news_button.click()    

                # 뉴스레터로 접근
                letter_button = page.locator("#menu-1-0084bdb").get_by_role("link", name="뉴스레터")
                await expect(letter_button).to_be_visible()
                await letter_button.hover()
                await letter_button.click()   

                await page.wait_for_url("https://www.fasoo.com/newsletter")

                # 최상단 뉴스레터 열어보기
                # 매월 업데이트 필요
                # await page.get_by_role("heading", name="년 2월호 뉴스레터").click()ㄴㄴ

                # 모든 뉴스레터 heading 가져오기 (예: "2024년 2월호 뉴스레터")
                newsletter_headings = await page.locator('role=heading').all()

                if not newsletter_headings:
                    print("뉴스레터가 존재하지 않음!")
                    return False

                # 선택 방법 (랜덤 / 첫 번째 / 두 번째)
                choice_method = "random"  # "random" / "first" / "second"

                if choice_method == "random":
                    target_index = random.randint(0, len(newsletter_headings) - 1)
                elif choice_method == "first":
                    target_index = 0
                elif choice_method == "second" and len(newsletter_headings) > 1:
                    target_index = 1
                else:
                    target_index = 0  # 기본적으로 첫 번째 선택

                # 선택한 뉴스레터 클릭
                await newsletter_headings[target_index].click()

                await asyncio.sleep(5) # 너무 빨리 지나가서 한번 어떤 페이지가 열리는지 확인

                 # 최대 5초 동안 이미지가 나타나는지 체크
                for _ in range(10):  # 0.5초마다 체크, 최대 5초 대기
                    images = await page.get_by_role("img").all()
                    if images:  # 이미지가 존재하면
                        print(f"이미지 {len(images)}개 감지됨. 뉴스레터 문제 없음")
                        return True
                    await asyncio.sleep(0.5)  # 0.5초 대기 후 다시 확인

                print("이미지가 나타나지 않음. 문제 발생")
                return False  # 이미지 없음 -> 실패

    
@function_logging
async def check_newsLetter_EN(settings, test_logger):
        url = "https://en.fasoo.com/"
        head_option = True
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True

        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
    
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    headless=settings.get_module_options(current_module)['headless'],    
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)
                
                # 상단 배너에서 News & Events 클릭
                support = page.get_by_role("navigation").get_by_role("link", name="News & Events")
                await expect(support).to_be_visible()
                await support.click()
                await page.wait_for_url("https://en.fasoo.com/news-and-events/")

                # 모든 뉴스레터 이미지 찾기
                newsletter_images = await page.get_by_role("img").all()

                if not newsletter_images:
                    print("[EN]뉴스레터 이미지가 없음")
                    return False

                # 선택 방법 (랜덤 / 첫 번째 / 두 번째)
                choice_method = "random"  # "random" / "first" / "second"
                
                if choice_method == "random":
                    target_index = random.randint(0, len(newsletter_images) - 1)
                elif choice_method == "first":
                    target_index = 0
                elif choice_method == "second" and len(newsletter_images) > 1:
                    target_index = 1
                else:
                    target_index = 0  # 기본적으로 첫 번째 선택

                # 선택된 이미지 클릭
                await newsletter_images[target_index].click()
                print(f"{target_index+1}번째 뉴스레터 클릭")

                 # 변경될 URL 패턴 정의 (정규식 사용)
                target_url_pattern = re.compile(r"https://en\.fasoo\.com/newsletter/.*")

                # URL 변경 대기 (최대 10초)
                try:
                    await page.wait_for_url(target_url_pattern, timeout=10000)  # 10초 대기
                    print(f"새 URL: {page.url}")

                    # 새 페이지에서 heading 요소 확인
                    has_heading = await page.locator('role=heading').count() > 0
                    return has_heading
                except:
                    print("URL 변경이 감지되지 않음!")
                    return False


@module_logging
@pytest.mark.asyncio
async def test_main(settings, test_logger):
    """
    """
    current_module = Path(__file__).name # Get current module name
    # Check if module should run
    if not settings.should_run_module(current_module):
        pytest.skip("Module disabled in configuration")

    await check_newsLetter_KR(settings, test_logger)
    await check_newsLetter_EN(settings, test_logger)
