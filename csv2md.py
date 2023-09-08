from bs4 import BeautifulSoup
import os

# 读取本地HTML文件
with open('/Users/xxx/Downloads/flomo@yourname-20230905/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 查找所有符合条件的div
memos = soup.find_all('div', {'class': 'memo'})

# 创建一个目录来保存Markdown文件
os.makedirs('markdown_files', exist_ok=True)

# 使用字典来存储每个日期的所有 memos
date_memo_dict = {}

for memo in memos:
    # 获取时间并格式化为日期
    time_div = memo.find('div', {'class': 'time'})
    date_str = time_div.text.split(' ')[0] if time_div else 'Unknown Date'

    # 获取内容
    content_div = memo.find('div', {'class': 'content'})
    content = content_div.text if content_div else ''

    # 获取文件
    files_div = memo.find('div', {'class': 'files'})
    files_content = ''
    if files_div:
        img_tags = files_div.find_all('img')
        for img in img_tags:
            src = img.get('src', '')
            files_content += f'![image.png](../assets/{src})\n'

    # 合并内容和文件
    full_content = content + '\n' + files_content

    # 将内容添加到字典中
    if date_str in date_memo_dict:
        date_memo_dict[date_str].append(full_content)
    else:
        date_memo_dict[date_str] = [full_content]

# 创建Markdown文件并写入内容
for date_str, memos in date_memo_dict.items():
    with open(f'markdown_files/{date_str}.md', 'w', encoding='utf-8') as f:
        f.write('\n---\n'.join(memos))

print("Markdown files have been created.")
