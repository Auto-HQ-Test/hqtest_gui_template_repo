import pytest
import asyncio
import pyautogui
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging
#from custom.select_n_random import select_n_random

#####
### 캡챠로 인해 사용자 개입 필요, 자동 다운로드드 구현 x
#####
# pip install pyautogui

async def solve_captcha_and_download(page):
    """CAPTCHA 체크 후 자동 다운로드"""
    captcha_checkbox = page.get_by_label("I'm not a robot")

    # CAPTCHA가 체크될 때까지 감시 (최대 30초)
    for _ in range(30):  # 1초씩 체크하며 30초 동안 대기
        if await captcha_checkbox.is_checked():
            print("CAPTCHA 해결됨! 다운로드 진행")
            break
        print("CAPTCHA 체크 대기 중...")
        await asyncio.sleep(1)  # 1초 대기 후 다시 확인
    else:
        print("CAPTCHA 해결이 감지되지 않음. 수동 해결 필요")
        return False  # CAPTCHA 해결 안되면 함수 종료

    # 다운로드 버튼 클릭
    await page.get_by_role("button", name="Submit to Download").click()
    print("📥 다운로드 버튼 클릭 완료")

    # PDF 다운로드 버튼이 있는지 확인하고 클릭
    await page.wait_for_timeout(3000)  # 다운로드 페이지 로딩 대기
    pdf_download_button = page.locator("text=다운로드")
    if await pdf_download_button.is_visible():
        await pdf_download_button.click()
        print("PDF 다운로드 완료")

    return True


@function_logging
async def download_brochure_KR(settings, test_logger):
    
            current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
            n = 5
            n_check_brochures = 10

            url = "https://www.fasoo.com/?lang=kr"
            browser_type = "chromium"
            width = 1920
            height = 1080
            accept_download = True


            async with async_playwright() as p:
                if browser_type == "chromium":
                    browser = await p.chromium.launch(headless=settings.get_module_options(current_module)['headless'])
                
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)

                # 자료실 버튼 찾기
                library_button = page.get_by_label("자료실").get_by_role("link", name="자료실")
                await expect(library_button).to_be_visible()
                await library_button.hover()
                await library_button.click()

                await page.wait_for_url("https://www.fasoo.com/document/case-study")
                await expect(page).to_have_url("https://www.fasoo.com/document/case-study")

                # Brochure 버튼 찾기
                brochure_button = page.get_by_role("link", name="Brochure")
                await expect(brochure_button).to_be_visible()
                await brochure_button.hover()
                await brochure_button.click()

                await page.wait_for_url("https://www.fasoo.com/document/brochure")
                #page.get_by_role("link", name="Brochure").click()
                #await expect(page.get_by_role("heading", name="케이스 스터디, 브로슈어, 백서, 산업 리포트")).to_be_visible()
                
                # Check brochure counts
                visible_brochures = await page.locator('[id^="post-"]').locator('role=link').all()
                n_brochures = len(visible_brochures) # The number of visible brochures. If not identical to the starting parameter, perform visual inspection. 
                for i in range(min(10,n_brochures)):
                    test_logger.console(str(visible_brochures[i]))
                if n_brochures != n_check_brochures:
                    test_logger.console(f"https://www.fasoo.com/document에서 열람 가능한 브로슈어의 수가 {n_brochures}입니다. 등록된 브로슈어의 수는 {n_check_brochures}입니다.")

                # Randomly sample n number of items
                random_indices = [i for i in [4, 5, 6] if i < n_brochures]

                for idx in random_indices:
                    brochure_selector = visible_brochures[idx]
                    await brochure_selector.click()
                    await page.wait_for_load_state("networkidle")

                    # CAPTCHA 확인 (자동화가 막힐 가능성 있음)
                    try:
                        captcha_checkbox = page.get_by_label("I'm not a robot")
                        await expect(captcha_checkbox).to_be_visible(timeout=5000)  # 3초 내로 CAPTCHA 확인
                        await captcha_checkbox.check()
                    except:
                        alert = pyautogui.alert('캡챠를 진행해주세요.', title='알림', button='확인', timeout = 10000)
                        print(alert)
                        await page.pause() 

                    """# 다운로드 처리
                    async with page.expect_download() as download_info:  # 다운로드 이벤트 감지
                        await page.get_by_role("button", name="Submit to Download").click()

                    download = await download_info.value  # 다운로드 완료 대기
                    download_path = await download.path()  # 다운로드 경로 가져오기

                    # 다운로드 완료 알림 (Alert 띄우기)
                    alert = pyautogui.alert('다운로드가 완료되었습니다', title='코딩유치원', button='확인', timeout = 3000)
                    print(alert)
                    
                    # PDF가 새 탭에서 열리는 경우 다운로드 버튼 클릭
                    await page.wait_for_timeout(2000)  # PDF 로딩 대기
                    pdf_download_button = page.locator("text=다운로드")
                    if await pdf_download_button.is_visible():
                        await pdf_download_button.click()
                        alert = pyautogui.alert('다운로드 버튼 클릭 완료', title='코딩유치원', button='확인', timeout = 3000)
                        print(alert)
                    """                 
                    await solve_captcha_and_download(page)
                            
                        # 원래 페이지로 복귀
                    await page.goto("https://www.fasoo.com/document")

                return True

    
@function_logging
async def download_brochure_EN(settings, test_logger):
        test_logger.console(f"2.브로셔 및 자료 다운로드(영문) - #NaN")
        pass

@module_logging
@pytest.mark.asyncio
async def test_download_brochure(settings, test_logger):
    """
    """
    current_module = Path(__file__).name # Get current module name
    # Check if module should run
    if not settings.should_run_module(current_module):
        pytest.skip("Module disabled in configuration")

    """n = 5
    n_check_brochures = 10"""
    await download_brochure_KR(settings, test_logger)
    await download_brochure_EN(settings, test_logger)
    #test_logger.console(f"2.브로셔 및 자료 다운로드 - 이상 없음")
    #test_logger.console(f"2. 브로셔 및 자료 다운로드 - 오류")
