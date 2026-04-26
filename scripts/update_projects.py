import os
import re
import httpx

username = 'mr-vishal-singh01'
token = os.environ.get('METRICS_TOKEN')

def get_latest_projects():
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token: headers['Authorization'] = f'bearer {token}'
    try:
        response = httpx.get(
            f'https://api.github.com/users/{username}/repos?sort=pushed&direction=desc',
            headers=headers
        )
        repos = response.json()
        if not isinstance(repos, list): return []
        return [r for repo in repos if (r := repo) and r['name'].lower() != username.lower() and not r['fork'] and not r['private']][:6]
    except: return []

def generate_minimal_list(projects):
    if not projects: return '<!-- No public projects found -->'
    html = '<table>\n'
    for i, p in enumerate(projects):
        if i % 2 == 0: html += '  <tr>\n'
        desc = p['description'] or 'Exploration in progress.'
        html += f'''    <td width="50%" valign="top">
      <b><a href="{p['html_url']}">{p['name']}</a></b><br/>
      <small>{desc}</small><br/>
      <code>{p['language'] or 'System'}</code> ⭐ <code>{p['stargazers_count']}</code>
    </td>
'''
        if i % 2 != 0 or i == len(projects) - 1: html += '  </tr>\n'
    return html + '</table>'

projects = get_latest_projects()
if projects:
    new_list = generate_minimal_list(projects)
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(r'<!-- PROJECTS_START -->.*<!-- PROJECTS_END -->', f'<!-- PROJECTS_START -->\n{new_list}\n<!-- PROJECTS_END -->', content, flags=re.DOTALL)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)