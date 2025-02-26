import pytest
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging

#####
### 구현 완료
### 전송(submit) 버튼은 주석처리로 비활성화 상태
#####

@function_logging
async def wrapsody_contactUs_KR_Main(settings, test_logger):
    
        url = "https://www.fasoo.com/?lang=kr"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
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

                # 상단 배너에서 제품 > Warpsody로 문의 페이지 접근
                link = page.get_by_label("제품").get_by_role("link", name="제품")
                await link.hover()
                support = page.get_by_role("link", name="생성형 AI 학습 콘텐츠 관리 | Wrapsody")
                await expect(support).to_be_visible()
                await support.click()
                await page.wait_for_url("https://www.fasoo.com/products/wrapsody")

                # 영업담당자 만나러가기 찾아서 클릭
                # Playwright ARIA 스냅샷을 사용하여 요소를 확인한 후 클릭
                await expect(page.locator("body")).to_match_aria_snapshot(
                    "- heading \"Wrapsody\" [level=2]\n"
                    "- heading \"Wrapsody 영업 담당자\" [level=2]\n"
                    "- heading \"만나러 가기\" [level=2]"
                )
                meeting_button = page.locator('text=만나러 가기')
                await expect(meeting_button).to_be_visible()  # 요소가 보일 때까지 대기
                async with page.expect_popup() as page11_info:  # 새 창 팝업 대기
                    await meeting_button.click()
                
                page11 = await page11_info.value

                # 팝업 페이지에서 필요한 작업을 진행
                await page11.wait_for_load_state("load")
                await page11.wait_for_url("https://www.fasoo.com/contact-us/solutions-a?type=wrapsody")
            
               
                # 양식 작성하기
                await page11.get_by_placeholder("성명*").click()
                await page11.get_by_placeholder("성명*").fill("hqtest1")
                await page11.get_by_placeholder("성명*").press("Tab")
                await page11.get_by_placeholder("회사*").fill("hqtest2")
                await page11.get_by_placeholder("회사*").press("Tab")
                await page11.get_by_placeholder("부서*").fill("hqtest3")
                await page11.get_by_placeholder("부서*").press("Tab")
                await page11.get_by_placeholder("직급*").fill("hqtest4")
                await page11.get_by_placeholder("직급*").press("Tab")
                await page11.get_by_placeholder("연락처*").fill("01011111111")
                await page11.get_by_placeholder("연락처*").press("Tab")
                await page11.get_by_placeholder("이메일*").fill("hqtest@fasoo.com")
                await page11.get_by_placeholder("이메일*").press("Tab")
                await page11.get_by_placeholder("문의 내용* (유저 수, 미팅 일정 등을 구체적으로 남겨 주시면 더욱 신속하게 상담이 진행됩니다.)").fill("hqtest5")
                await page11.get_by_label("온/오프라인 행사").check()
                await page11.get_by_label("개인정보 수집 및 이용에 대해서 동의합니다").check()
                #await page11.once("dialog", lambda dialog: dialog.dismiss())

                ###await page11.get_by_role("button", name="상담 신청하기").click()
            
                return True
   

@function_logging
async def wrapsody_contactUs_EN_Main(settings, test_logger):
    
        url = "https://en.fasoo.com/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
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

                # 'Products' 링크에 hover
                link = page.get_by_role("banner").get_by_role("link", name="Products")
                await link.hover()  
                
                # 'AI-Ready Data' 탭이 나타날 때까지 기다림
                ai_ready_data_tab = page.get_by_role("tab", name="AI-Ready Data")
                await expect(ai_ready_data_tab).to_be_visible()  

                # 'AI-Ready Data' 탭 클릭
                await ai_ready_data_tab.click()
                # await page.wait_for_url("https://en.fasoo.com/products/ai-ready-data/")  # 페이지가 해당 URL로 변경될 때까지 기다림

                # 'Wrapsody' 링크에 hover
                wrapsody_link = page.get_by_role("link", name="Wrapsody Enterprise Content")
                await wrapsody_link.hover()
                
                # 'Wrapsody' 링크 클릭
                await wrapsody_link.click()
                await page.wait_for_url("https://en.fasoo.com/products/wrapsody/")

                # contact us 버튼 클릭 후 팝업 대기
                async with page.expect_popup() as page12_info:  # 팝업을 기다리고 -> page12_info에 저장
                    await page.locator("section").filter(has_text="Wrapsody is available in the").get_by_role("link").click()

                # 팝업 페이지를 page12로 받아옴
                page12 = await page12_info.value

                # 팝업 페이지에서 필요한 작업을 진행
                await page12.wait_for_load_state("load")  # 팝업 페이지가 로드될 때까지 대기
                await page12.wait_for_url("https://en.fasoo.com/contact-us/product?type=wrapsody")  # URL이 일치할 때까지 대기
                

                # 양식 작성하기
                await page12.get_by_placeholder("Name*").click()
                await page12.get_by_placeholder("Name*").fill("hqtest1")
                await page12.get_by_placeholder("Name*").press("Tab")
                await page12.get_by_placeholder("Company*").fill("hqtest2")
                await page12.get_by_placeholder("Company*").press("Tab")
                await page12.get_by_placeholder("Department*").fill("hqtest3")
                await page12.get_by_placeholder("Department*").press("Tab")
                await page12.get_by_placeholder("Job Title*").fill("hqtest4")
                await page12.get_by_placeholder("Job Title*").press("Tab")
                await page12.get_by_placeholder("Phone*").fill("01011111111")
                await page12.get_by_placeholder("Phone*").press("Tab")
                await page12.get_by_placeholder("Work Email*").fill("hqtest5@fasoo.com")
                await page12.get_by_placeholder("Work Email*").press("Tab")
                await page12.get_by_placeholder("Inquiry Details*  (For a").fill("hello")
                await page12.get_by_label("Search Engine (Google, Bing,").check()
                await page12.get_by_label("I agree to the collection and").check()

                # 상담 신청하기 버튼 클릭
                ###await page12.get_by_role("button", name="Book Now").click()

                return True
   

@function_logging
async def wrapsodyECO_contactUs_KR_Main(settings, test_logger):
    
        url = "https://www.fasoo.com/?lang=kr"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
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
                # 상단 배너에서 제품 > Warpsody로 문의 페이지 접근
                link = page.get_by_label("제품").get_by_role("link", name="제품")
                await link.hover()
                support = page.get_by_role("link", name="Wrapsody eCo", exact=True)
                await expect(support).to_be_visible()
                await support.click()
                await page.wait_for_url("https://www.fasoo.com/products/wrapsody-eco")
                
                # 영업담당자 만나러가기 찾아서 클릭
                # Playwright ARIA 스냅샷을 사용하여 요소를 확인한 후 클릭
                await expect(page.locator("body")).to_match_aria_snapshot(
                    "- heading \"Wrapsody\" [level=2]\n"
                    "- heading \"Wrapsody eCo 영업 담당자\" [level=2]\n"
                    "- heading \"만나러 가기\" [level=2]"
                )
                meeting_button = page.locator('text=만나러 가기')
                await expect(meeting_button).to_be_visible()  # 요소가 보일 때까지 대기
                async with page.expect_popup() as page11_info:  # 새 창 팝업 대기
                    await meeting_button.click()
                page11 = await page11_info.value
                # 팝업 페이지에서 필요한 작업을 진행
                await page11.wait_for_load_state("load")
                await page11.wait_for_url("https://www.fasoo.com/contact-us/solutions-c?type=wrapsody-eco")
                
                # 양식 작성하기
                await page11.get_by_label("성명").click()
                await page11.get_by_label("성명").fill("hqtest1")
                await page11.get_by_label("성명").press("Tab")
                await page11.get_by_label("회사").fill("hqtest2")
                await page11.get_by_label("회사").press("Tab")
                await page11.get_by_label("부서").fill("hqtest3")
                await page11.get_by_label("부서").press("Tab")
                await page11.get_by_label("직급").fill("hqtest4")
                await page11.get_by_label("직급").press("Tab")
                await page11.get_by_label("연락처").fill("01011111111")
                await page11.get_by_label("연락처").press("Tab")
                await page11.get_by_label("이메일").fill("hqtest@fasoo.com")
                await page11.get_by_label("이메일").press("Tab")
                await page11.get_by_label("온/오프라인 행사").check()
                await page11.get_by_placeholder("유저 수, 미팅 일정 등을 구체적으로 남겨 주시면 더욱 신속하게 상담이 진행됩니다").fill("hqtest")
                #await page11.once("dialog", lambda dialog: dialog.dismiss())
                await page11.get_by_label("개인정보 수집 및 이용에 대해서 동의합니다").check()
                ###await page11.get_by_role("button", name="상담 신청하기").click()

                return True

 

@function_logging
async def wrapsodyECO_contactUs_EN_Main(settings, test_logger):
    
        url = "https://en.fasoo.com/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
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
                await page.wait_for_load_state("networkidle") 
                # 'Products' 링크에 hover
                await expect(page.get_by_role("banner").get_by_role("link", name="Products")).to_be_visible()
                await page.get_by_role("banner").get_by_role("link", name="Products").hover()
                # 'Secure Collaboration' 탭이 나타날 때까지 기다린 후 호버링
                await expect(page.get_by_role("tab", name="Secure Collaboration")).to_be_visible()
                await page.get_by_role("tab", name="Secure Collaboration").hover()
                await expect(page.get_by_role("link", name="Wrapsody eCo Secure")).to_be_visible()
                await page.get_by_role("link", name="Wrapsody eCo Secure").click()
                await page.wait_for_url("https://en.fasoo.com/products/wrapsody-eco/")
                await page.wait_for_load_state("networkidle") 
                await expect(page.get_by_role("heading", name="Why Wrapsody eCo?")).to_be_visible()
                await expect(page.get_by_role("heading", name="Meet with a Wrapsody eCo")).to_be_visible()
                async with page.expect_popup() as page1_info:
                    await page.get_by_role("heading", name="Meet with a Wrapsody eCo").click()
                page1 = await page1_info.value
                # 양식 작성하기
                await page1.get_by_placeholder("Name*").click()
                await page1.get_by_placeholder("Name*").fill("hqtest")
                await page1.get_by_placeholder("Name*").press("Tab")
                await page1.get_by_placeholder("Company*").fill("hqtest")
                await page1.get_by_placeholder("Company*").press("Tab")
                await page1.get_by_placeholder("Department*").fill("hqtest")
                await page1.get_by_placeholder("Department*").press("Tab")
                await page1.get_by_placeholder("Job Title*").fill("hqtest")
                await page1.get_by_placeholder("Job Title*").press("Tab")
                await page1.get_by_placeholder("Phone*").fill("01022222222")
                await page1.get_by_placeholder("Work Email*").click()
                await page1.get_by_placeholder("Work Email*").fill("hqtest@fasoo.com")
                await page1.get_by_placeholder("Work Email*").press("Tab")
                await page1.get_by_placeholder("Inquiry Details*  (For a").fill("hqtest")
                await page1.get_by_label("Search Engine (Google, Bing,").check()
                await page1.get_by_label("I agree to the collection and").check()
                ###await page1.get_by_role("button", name="Book Now").click()
                # await expect(page1.get_by_text("Your submission was")).to_be_visible()
                # test_logger.info("[메인] Wrapsody eCo 문의하기[EN] - 이상 없음")
                await browser.close()
                return True
   
  
@function_logging
async def wrapsodySE_contactUs_KR_Main(settings, test_logger):
    
        url = "https://www.fasoo.com/?lang=kr"
        browser_config = {
            "type": "chromium",
            "headless": True,
            "viewport": {"width": 1920, "height": 1080},
            "accept_downloads": True,
            "timeout": 20000
        }

        async with async_playwright() as p:
            # Browser setup
            browser = await p.chromium.launch(headless=browser_config["headless"])
            context = await browser.new_context(
                viewport=browser_config["viewport"],
                accept_downloads=browser_config["accept_downloads"]
            )
            context.set_default_timeout(browser_config["timeout"])
            page = await context.new_page()

            # Navigate to main page
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            # Click Wrapsody Drive link
            drive_link = page.get_by_role("link", name="문서 관리 x 보안 강화 | Wrapsody Drive")
            await expect(drive_link).to_be_visible()
            await drive_link.click()

            # Handle popup for contact form
            async with page.expect_popup() as page1_info:
                await page.get_by_role("heading", name="Wrapsody SE 영업 담당자").click()
            contact_page = page1_info.value
            await contact_page.wait_for_load_state("networkidle")

            # Form field data
            form_data = {
                "성명*": "hqtest",
                "회사*": "hqtest",
                "부서*": "hqtest",
                "직급*": "hqtest",
                "연락처*": "01090283044",
                "이메일*": "hqtest@fasoo.com",
                "문의 내용* (유저 수, 미팅 일정 등을 구체적으로 남겨 주시면 더욱 신속하게 상담이 진행됩니다.)": "hqtest"
            }

            # Fill form fields
            for placeholder, value in form_data.items():
                field = contact_page.get_by_placeholder(placeholder)
                await expect(field).to_be_visible()
                await field.click()
                await field.fill(value)

            # Check required checkboxes
            checkboxes = [
                "온/오프라인 행사",
                "개인정보 수집 및 이용에 대해서 동의합니다"
            ]
            for checkbox in checkboxes:
                await contact_page.get_by_label(checkbox).check()
            # Submit button is commented out for testing
            # submit_button = contact_page.get_by_role("button", name="상담 신청하기")
            # await expect(submit_button).to_be_visible()
            # await submit_button.click()
            # Close browser
            await browser.close()
            return True


@function_logging
async def wrapsodyDrive_contactUs_KR_Main(settings, test_logger):
    
        url = "https://www.fasoo.com/?lang=kr"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
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
                await page.wait_for_load_state("networkidle")

                link = page.get_by_label("제품").get_by_role("link", name="제품")
                await link.hover()
                support = page.get_by_role("link", name="차세대 문서중앙화 | Wrapsody Drive")
                await expect(support).to_be_visible()
                await support.click()
                await page.wait_for_url("https://www.fasoo.com/products/wrapsody-drive")
                async with page.expect_popup() as page1_info:
                    await page.get_by_role("heading", name="Wrapsody Drive 영업 담당자").click()
                page1 = await page1_info.value
                await page1.get_by_placeholder("성명*").click()
                await page1.get_by_placeholder("성명*").fill("hqtest")
                await page1.get_by_placeholder("회사*").click()
                await page1.get_by_placeholder("회사*").fill("hqtest")
                await page1.get_by_placeholder("부서*").click()
                await page1.get_by_placeholder("부서*").fill("hqtest")
                await page1.get_by_placeholder("직급*").click()
                await page1.get_by_placeholder("직급*").fill("hqtest")
                await page1.get_by_placeholder("연락처*").click()
                await page1.get_by_placeholder("연락처*").fill("01090283044")
                await page1.get_by_placeholder("연락처*").press("Tab")
                await page1.get_by_placeholder("이메일*").fill("hqtest")
                await page1.get_by_placeholder("이메일*").click()
                await page1.get_by_placeholder("이메일*").fill("hqtest@fasoo.com")
                await page1.get_by_placeholder("문의 내용* (유저 수, 미팅 일정 등을 구체적으로 남겨 주시면 더욱 신속하게 상담이 진행됩니다.)").click()
                await page1.get_by_placeholder("문의 내용* (유저 수, 미팅 일정 등을 구체적으로 남겨 주시면 더욱 신속하게 상담이 진행됩니다.)").fill("hqtest")
                await page1.get_by_label("온/오프라인 행사").check()
                await page1.get_by_label("개인정보 수집 및 이용에 대해서 동의합니다").check()
                ### page1.get_by_role("button", name="상담 신청하기").click()
        
                

@function_logging
async def wrapsodyDrive_contactUs_EN_Main(settings, test_logger):
    
        url = "https://en.fasoo.com/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
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
                await page.wait_for_load_state("networkidle")

                # Get the navigation bar 
                nav_menu = page.get_by_role("navigation")
                products_link = nav_menu.get_by_role("link", name="Products")

                # Verify Products link is visible
                await expect(products_link).to_be_visible()
                await products_link.hover()

                # Go to wrapsody link
                wrapsody_link = page.get_by_role("link", name="Wrapsody Drive Virtual")
                await expect(wrapsody_link).to_be_visible()
                await wrapsody_link.click()
                await page.wait_for_url("https://en.fasoo.com/products/wrapsody-drive/")
                
                async with page.expect_popup() as page1_info:
                    await page.get_by_role("heading", name="Meet with a Wrapsody Sales").click()
                page1 = await page1_info.value
                await page1.get_by_placeholder("Name*").click()
                await page1.get_by_placeholder("Name*").fill("hqtest")
                await page1.get_by_placeholder("Name*").press("Tab")
                await page1.get_by_placeholder("Company*").fill("hqtest")
                await page1.get_by_placeholder("Company*").press("Tab")
                await page1.get_by_placeholder("Department*").fill("hqtest")
                await page1.get_by_placeholder("Department*").press("Tab")
                await page1.get_by_placeholder("Job Title*").fill("hqtest")
                await page1.get_by_placeholder("Job Title*").press("Tab")
                await page1.get_by_placeholder("Phone*").fill("01022222222")
                await page1.get_by_placeholder("Work Email*").click()
                await page1.get_by_placeholder("Work Email*").fill("hqtest@fasoo.com")
                await page1.get_by_placeholder("Work Email*").press("Tab")
                await page1.get_by_placeholder("Inquiry Details*  (For a").fill("hqtest")
                await page1.get_by_label("Search Engine (Google, Bing,").check()
                await page1.get_by_label("I agree to the collection and").check()
                ### await page1.get_by_role("button", name="Book Now").click()
                # await expect(page1.get_by_text("Your submission was")).to_be_visible()
                return True

@function_logging
async def AIRPrivacy_contactUs_KR_Main(settings, test_logger):
    
        url = "https://www.fasoo.com/?lang=kr"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
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
                await page.wait_for_load_state("networkidle")

                # Get the navigation bar 
                nav_menu = page.get_by_role("navigation")
                products_link = nav_menu.get_by_role("link", name="제품")
                # Verify Products link is visible
                await expect(products_link).to_be_visible()
                await products_link.hover()
                
                await page.get_by_role("link", name="AI 기반 개인정보보호 및 검출 | AI-R").click()
                await page.wait_for_url("https://www.fasoo.com/products/fasoo-ai-r-privacy")
                await page.wait_for_load_state("networkidle")

                # Go to contact us link
                async with page.expect_popup() as page1_info:
                    await page.get_by_role("heading", name="AI-R Privacy 영업 담당자").click()
                page1 = await page1_info.value
                await page1.get_by_placeholder("성명*").click()
                await page1.get_by_placeholder("성명*").fill("hqtest")
                await page1.get_by_placeholder("회사*").click()
                await page1.get_by_placeholder("회사*").fill("hqtest")
                await page1.get_by_placeholder("부서*").click()
                await page1.get_by_placeholder("부서*").fill("hqtest")
                await page1.get_by_placeholder("직급*").click()
                await page1.get_by_placeholder("직급*").fill("hqtest")
                await page1.get_by_placeholder("연락처*").click()
                await page1.get_by_placeholder("연락처*").fill("01090283044")
                await page1.get_by_placeholder("이메일*").click()
                await page1.get_by_placeholder("이메일*").fill("hqtest@fasoo.com")
                await page1.get_by_placeholder("문의 내용* (유저 수, 미팅 일정 등을 구체적으로 남겨 주시면 더욱 신속하게 상담이 진행됩니다.)").click()
                await page1.get_by_label("온/오프라인 행사").check()
                await page1.get_by_label("개인정보 수집 및 이용에 대해서 동의합니다").check()
                ### await page1.get_by_role("button", name="상담 신청하기").click()
                return True
            
    
"""@function_logging
async def AIRPrivacy_contactUs_EN_Main(settings, test_logger):
    
        url = "https://en.fasoo.com/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
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
                await page.wait_for_load_state("networkidle")

                # Get the navigation bar 
                nav_menu = page.get_by_role("navigation")
                products_link = nav_menu.get_by_role("link", name="Products")

                # Verify Products link is visible
                await expect(products_link).to_be_visible()
                await products_link.hover()

                # Go to wrapsody link
                link = page.get_by_role("link", name="")
                await expect(link).to_be_visible()
                await link.click()
                await page.wait_for_url("")

                await page.get_by_placeholder("Name*").click()
                await page.get_by_placeholder("Name*").fill("hqtest")
                await page.get_by_placeholder("Name*").press("Tab")
                await page.get_by_placeholder("Company*").fill("hqtest")
                await page.get_by_placeholder("Company*").press("Tab")
                await page.get_by_placeholder("Department*").fill("hqtest")
                await page.get_by_placeholder("Department*").press("Tab")
                await page.get_by_placeholder("Job Title*").fill("hqtest")
                await page.get_by_placeholder("Job Title*").press("Tab")
                await page.get_by_placeholder("Phone*").fill("0000000000")
                await page.get_by_placeholder("Phone*").press("Tab")
                await page.get_by_placeholder("Work Email*").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("Work Email*").press("Tab")
                await page.get_by_placeholder("Inquiry Details*  (For a").fill("hqtest")
                await page.get_by_text("Search Engine (Google, Bing,").click()
                await page.locator("span").filter(has_text="I'd like Fasoo to use my").click()
                await page.once("dialog", lambda dialog: dialog.dismiss())"""
                # await page.get_by_role("button", name="Book Now").click()

@module_logging
@pytest.mark.asyncio
async def test_newLandingPage(settings, test_logger):
    """Test both components"""

    await wrapsody_contactUs_KR_Main(settings, test_logger)
    await wrapsody_contactUs_EN_Main(settings, test_logger)

    await wrapsodyECO_contactUs_KR_Main(settings, test_logger)
    await wrapsodyECO_contactUs_EN_Main(settings, test_logger)

    await wrapsodySE_contactUs_KR_Main(settings, test_logger)
        
    await wrapsodyDrive_contactUs_KR_Main(settings, test_logger)
    await wrapsodyDrive_contactUs_EN_Main(settings, test_logger)
        
    await AIRPrivacy_contactUs_KR_Main(settings, test_logger)
