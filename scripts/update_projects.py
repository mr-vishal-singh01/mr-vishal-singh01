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
            f'https://api.github.com/users/{username}/repos?sort=updated&direction=desc',
            headers=headers
        )
        repos = response.json()
        if not isinstance(repos, list):
            print(f'Error fetching repos: {repos}')
            return []
        featured = []
        for repo in repos:
            # Filter out profile repo and forks
            if repo['name'].lower() != username.lower() and not repo['fork'] and repo['name'] != 'mr-vishal-singh01':
                featured.append(repo)
                if len(featured) == 6: break # Show top 6
        return featured
    except Exception as e:
        print(f'Exception: {e}')
        return []

def generate_html_table(projects):
    if not projects: return '<!-- No recent public projects found -->'
    
    html = '<table width="100%" bordercolor="#30363d">\n  <tr>\n'
    for i, p in enumerate(projects):
        if i > 0 and i % 2 == 0: html += '  </tr>\n  <tr>\n'
        desc = p['description'] if p['description'] else 'Sovereign forge in progress...'
        stars = p['stargazers_count']
        lang = p['language'] or 'Mixed'
        
        html += f'''
    <td width="50%" valign="top">
      <h3 align="center"> 💠 {p['name']}</h3>
      <p align="center">{desc}</p>
      <p align="center">
        <img src="https://img.shields.io/badge/Language-{lang}-blue?style=flat-square"/>
        <img src="https://img.shields.io/badge/Stars-{stars}-yellow?style=flat-square&logo=github"/>
      </p>
      <div align="center">
        <a href="{p['html_url']}"><img src="https://img.shields.io/badge/Command-Access_Forge-success?style=for-the-badge&logo=gitbook&logoColor=white"/></a>
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
    
    # Updated regex to match the OMEGA section
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