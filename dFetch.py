from playwright.sync import sync_playwright

def scrape_dynamic_page(url):
    with sync_playwright() as p:
        # 启动浏览器（headless=False 显示浏览器窗口，方便调试）
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 访问目标网页
        page.goto(url)
        
        # 等待页面加载完成（根据实际页面调整等待条件）
        # 例如等待某个特定元素出现
        page.wait_for_selector("body > div.content")  # 替换为实际内容的选择器
        
        # 获取渲染后的完整HTML
        full_html = page.content()
        
        # 也可以直接提取需要的内容
        # 例如提取所有段落文本
        paragraphs = page.query_selector_all("p")
        content = [p.text_content() for p in paragraphs]
        
        # 关闭浏览器
        browser.close()
        
        return full_html, content

# 使用示例
if __name__ == "__main__":
    target_url = "https://www.toutiao.com/"  # 替换为目标网址
    html, text_content = scrape_dynamic_page(target_url)
    
    print("渲染后的HTML长度:", len(html))
    print("提取的文本内容:", text_content[:3])  # 打印前3条内容
