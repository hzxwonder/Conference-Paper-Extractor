import json
import os

# 读取 JSON 文件并将其解析为 Python 对象
root = "Paper_set/"

for file in os.listdir(root):
    json_path = os.path.join(root, file)
    conference = file.split('-')[0].upper()
    year = file.split('-')[1].split('.')[0]

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output = f"../Conference-Paper/{conference}/{year}/"

    # 创建输出文件夹
    if not os.path.exists(output):
        os.makedirs(output)

    batch_size = 200
    paper_idx = 0

    for i in range(0, len(data), batch_size):
        data_batch = data[i:i+batch_size]
        # 为每篇论文创建 Markdown 格式的字符串并存储在列表中
        markdown_strings = []
        for j,paper in enumerate(data_batch):
            try:
                markdown_string = f"""## {[paper_idx]} {paper['Title'].replace('.', '') if ('.' in paper['Title'] and paper['Title'][-1]=='.')else paper['Title']}

        **Authors**: *{", ".join(paper['Authors'])}*

        **Conference**: *{paper['Conference']} {paper['Time']}*

        **URL**: [{paper['URL']}]({paper['URL']})

        **Abstract**:

        {paper['Abstract'].strip()}

        ----

        """
            except:
                import pdb; pdb.set_trace()
            markdown_strings.append(markdown_string)
            paper_idx += 1

        if i == 0:
            markdown_strings.append(f"\n\n[Go to the next page]({conference}-{year}-list{i//batch_size+2:02d}.md)")
            markdown_strings.append(f"\n\n[Go to the catalog section](README.md)")
        elif i+batch_size >= len(data):
            markdown_strings.append(f"\n\n[Go to the previous page]({conference}-{year}-list{i//batch_size:02d}.md)")
            markdown_strings.append(f"\n\n[Go to the catalog section](README.md)")
        else:
            markdown_strings.append(f"\n\n[Go to the previous page]({conference}-{year}-list{i//batch_size:02d}.md)")
            markdown_strings.append(f"\n\n[Go to the next page]({conference}-{year}-list{i//batch_size+2:02d}.md)")
            markdown_strings.append(f"\n\n[Go to the catalog section](README.md)")

        with open(os.path.join(output, f'{conference}-{year}-list{i//batch_size+1:02d}.md'), 'w', encoding='utf-8') as f:
            for markdown_string in markdown_strings:
                f.write(markdown_string)


    readme_string = f"# {conference} {year} Paper List\n\n"

    readme_string += f"> Below is an index of article pages, with up to {batch_size} articles per markdown.\n\n"

    for i in range(0, len(data), batch_size):
        readme_string += f"- [{conference}-{year}-list{i//batch_size+1:02d}.md]({conference}-{year}-list{i//batch_size+1:02d}.md)\n"

    with open(os.path.join(output, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_string)