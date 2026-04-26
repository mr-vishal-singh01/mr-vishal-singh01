import os
import re
import httpx

username = 'mr-vishal-singh01'
token = os.environ.get('METRICS_TOKEN')

def get_latest_projects():
    headers = {}
    if token: headers['Authorization'] = f'bearer {token}'
    try:
        response = httpx.get(
            f'https://api.github.com/users/{username}/repos?sort=created&direction=desc',
            headers=headers
        )
        repos = response.json()
        if not isinstance(repos, list):
            print(f'Error fetching repos: {repos}')
            return []
        featured = []
        for repo in repos:
            if repo['name'] != username and not repo['fork']:
                featured.append(repo)
                if len(featured) == 4: break
        return featured
    except Exception as e:
        print(f'Exception: {e}')
        return []

def generate_html_table(projects):
    html = '<table bordercolor="#30363d">\n  <tr>\n'
    for i, p in enumerate(projects):
        if i > 0 and i % 2 == 0: html += '  </tr>\n  <tr>\n'
        desc = p['description'] if p['description'] else 'No description provided.'
        html += f'''
    <td width="50%" valign="top">
      <h3 align="center"> 🛠️ {p['name']}</h3>
      <p>{desc}</p>
      <div align="center">
        <a href="{p['html_url']}"><img src="https://img.shields.io/badge/View_Source-Repository-2ea44f?style=for-the-badge&logo=github"/></a>
      </div>
    </td>
'''
    html += '  </tr>\n</table>'
    return html

projects = get_latest_projects()
if projects:
    new_table = generate_html_table(projects)
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(
        r'<!-- PROJECTS_START -->.*<!-- PROJECTS_END -->',
        f'<!-- PROJECTS_START -->\n{new_table}\n<!-- PROJECTS_END -->',
        content,
        flags=re.DOTALL
    )
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
else:
    print('No projects found to update.')