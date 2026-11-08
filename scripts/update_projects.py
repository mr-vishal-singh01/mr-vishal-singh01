import os
import re
import httpx

username = "mr-vishal-singh01"
token = os.environ.get("METRICS_TOKEN")

def get_latest_projects():
    headers = {}
    if token:
        headers["Authorization"] = f"bearer {token}"
    response = httpx.get(
        f"https://api.github.com/users/{username}/repos?sort=created&direction=desc",
        headers=headers
    )
    repos = response.json()
    
    featured = []
    for repo in repos:
        if repo.get("name") != username and not repo.get("fork"):
            featured.append(repo)
            if len(featured) == 4:
                break
    return featured

def generate_html_table(projects):
    html = '<table>\n  <tr>\n'
    for i, p in enumerate(projects):
        if i > 0 and i % 2 == 0:
            html += "  </tr>\n  <tr>\n"
        desc = p.get("description") or "No description provided."
        name = p.get("name", "")
        url = p.get("html_url", f"https://github.com/{username}/{name}")
        html += f"""    <td width="50%" valign="top">
      <h3 align="center">🚀 {name}</h3>
      <p>{desc}</p>
      <div align="center">
        <a href="{url}"><img src="https://img.shields.io/badge/View_Source-Repository-388BFD?style=for-the-badge&logo=github&labelColor=21262D"/></a>
      </div>
    </td>
"""
    html += "  </tr>\n</table>"
    return html

if __name__ == "__main__":
    projects = get_latest_projects()
    if projects:
        new_table = generate_html_table(projects)
        readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = re.sub(
            r"<!-- PROJECTS_START -->.*<!-- PROJECTS_END -->",
            f"<!-- PROJECTS_START -->\n{new_table}\n<!-- PROJECTS_END -->",
            content,
            flags=re.DOTALL
        )

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
