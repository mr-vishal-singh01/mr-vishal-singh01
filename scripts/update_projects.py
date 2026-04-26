import os
import re
import httpx
from datetime import datetime

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
        if not isinstance(repos, list):
            return []
        featured = []
        for repo in repos:
            if repo['name'].lower() != username.lower() and not repo['fork'] and not repo['private']:
                featured.append(repo)
                if len(featured) == 6: break
        return featured
    except Exception as e:
        print(f'Exception: {e}')
        return []

def generate_html_grid(projects):
    if not projects: return '<!-- No public projects found -->'
    
    html = '<div align="center">\n<table width="100%" style="border-collapse: collapse; border: none;">\n'
    for i, p in enumerate(projects):
        if i % 2 == 0: html += '  <tr style="border: none;">\n'
        
        desc = p['description'] if p['description'] else 'Forging the future of agentic systems...'
        if len(desc) > 85: desc = desc[:82] + '...'
        
        stars = p['stargazers_count']
        forks = p['forks_count']
        lang = p['language'] or 'Mixed'
        updated = datetime.strptime(p['pushed_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')
        
        html += f'''
    <td width="50%" align="left" style="padding: 15px; border: 1px solid #30363d; border-radius: 10px;">
      <a href="{p['html_url']}">
        <h3 align="center"> ⚡ {p['name']}</h3>
      </a>
      <p align="center" style="color: #8b949e; font-size: 14px;">{desc}</p>
      <div align="center">
        <img src="https://img.shields.io/badge/-{lang}-blue?style=flat-square"/>
        <img src="https://img.shields.io/badge/⭐-{stars}-yellow?style=flat-square"/>
        <img src="https://img.shields.io/badge/Last_Push-{updated.replace(' ', '_')}-gray?style=flat-square"/>
      </div>
    </td>
'''
        if i % 2 != 0 or i == len(projects) - 1: html += '  </tr>\n'
        
    html += '</table>\n</div>'
    return html

projects = get_latest_projects()
if projects:
    new_grid = generate_html_grid(projects)
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(
        r'<!-- PROJECTS_START -->.*<!-- PROJECTS_END -->',
        f'<!-- PROJECTS_START -->\n{new_grid}\n<!-- PROJECTS_END -->',
        content,
        flags=re.DOTALL
    )
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
else:
    print('No projects found.')