import svgwrite
import asyncio
import aiohttp
import base64
import textwrap
import json
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get("GITHUB_TOKEN")
username = "BulusHamnu"
user_repo_name = "Interative-responsive-Carousel-in-vanilla-js-html-and-css"
pinned_repo = True #this flag is set true if i wanna query for pinned repos
selected_theme = "light"

# theme color for svg
themes_colors = {
    "light" : {
        "background" : "#e5e5e5",
        "header" : "#17a2b8",
        "text" : "#333333"
    },
    "dark" : {
        "background" : "#282c34",
        "header" : "#008080",
        "text" : "#ffffff"
    },
}
#github color code for lang
colors_code = {
    "Python": "#3572A5",
    "JavaScript": "#F1E05A",
    "TypeScript": "#3178C6",
    "HTML": "#E34C26",
    "CSS": "#563D7C",
    "Java": "#B07219",
    "Kotlin": "#A97BFF",
    "C": "#555555",
    "C++": "#F34B7D",
    "C#": "#178600",
    "Go": "#00ADD8",
    "Rust": "#DEA584",
    "Swift": "#F05138",
    "PHP": "#4F5D95",
    "Ruby": "#701516",
    "Dart": "#00B4AB",
    "Shell": "#89E051",
    "Scala": "#DC322F",
    "Objective-C": "#438EFF",
    "Perl": "#0298C3",
    "Lua": "#000080",
    "Haskell": "#5E5086",
    "Elixir": "#6E4A7E",
    "Clojure": "#DB5855",
    "R": "#198CE7",
    "Matlab": "#E16737",
    "Vim Script": "#199F4B",
    "TeX": "#3D6117",
    "GraphQL": "#E10098",
    "Makefile": "#427819",
    "Dockerfile": "#384D54",
    "None": "#384D54"
}

query = """
query ($login : String!){
      user(login: $login) {
        pinnedItems(first: 6, types: [REPOSITORY]) {
          nodes {
            ... on Repository {
              name
              url
              description
              stargazerCount
              primaryLanguage {
                name
              }
            }
          }
        }
      }
}
""" #query schema
headers = {"Authorization": f"Bearer {TOKEN}"}


#functions
def create_svg(file_name,desc,title,cover_img,lang,like_count,themes) :
    width = 320
    height = 210

    # covert my image to based64 so it will be saved in the svg
    # with open(cover_img, "rb") as image:
    #     image_file = image.read()
    #     encode_file_data = base64.b64encode(image_file)
    #     decoded_file_data = encode_file_data.decode('utf-8')
    # image_data = f'data:image/png;base64,{decoded_file_data}'
    # format data

    # create svg file
    svg = svgwrite.Drawing(file_name, size=(width, height), profile=("full"))
    svg.add(svg.rect(insert=((width - width) / 2, 0), size=(width, height), rx=5, ry=5, fill=(themes_colors[themes].get("background"))))
    # svg.add(svg.image(href=image_data, insert=((width - 250) / 2, 0), size=(250, 250))
    svg.add(svg.rect(insert=((width - 280) / 2, 15), size=(280, 35), rx=5, ry=5, fill=(themes_colors[themes].get("header"))))

    #if the title is too long
    if len(title) > 25 :
        title = title[0:25]
        title += ".."

    svg.add(svg.text(title, insert=(width / 2, 38), fill=themes_colors[themes].get("text"), font_size="20px",text_anchor="middle"))
    paragraph = svg.text("", insert=(width / 2, 56), fill=themes_colors[themes].get("text"), font_size="16px", text_anchor="middle")

    # to create multi-line and avoid overflow in svg so i broke the desc
    if desc :
        wrapped_text = textwrap.wrap(desc, width=40)
        for i in range(len(wrapped_text)):
            if i < 5:
                if i == 4:
                    wrapped_text[i] += "..."
                line = svg.tspan(wrapped_text[i], x=[29], dy=["1.2em"], text_anchor="start")
                paragraph.add(line)
                # width / 2
    else :
        desc = "No description for this project."
        line = svg.tspan(desc, x=[width / 2], dy=["1.2em"])
        paragraph.add(line)

    svg.add(paragraph)
    lang = "None" if not lang else lang
    svg.add(svg.circle(center=(40, 180), r=8, fill=colors_code[lang ]))
    svg.add(svg.text(lang, insert=(55, 185), fill=themes_colors[themes].get("text"), font_size="15px"))

    #from web
    star_points = [
        (10 * 1.1 + 225, 4 * 1.1 + 168),  # Top
        (12 * 1.1 + 225, 8 * 1.1 + 168),
        (16 * 1.1 + 225, 8 * 1.1 + 168),
        (13 * 1.1 + 225, 11 * 1.1 + 168),
        (14 * 1.1 + 225, 15 * 1.1 + 168),
        (10 * 1.1 + 225, 13 * 1.1 + 168),
        (6 * 1.1 + 225, 15 * 1.1 + 168),
        (7 * 1.1 + 225, 11 * 1.1 + 168),
        (4 * 1.1 + 225, 8 * 1.1 + 168),
        (8 * 1.1 + 225, 8 * 1.1 + 168)
    ]
    svg.add(svg.polygon(points=star_points, fill="none", stroke="yellow", stroke_width=2))

    #reduce and change to k format
    if like_count >= 1000000:
        m = like_count / 1000000
        like_count = str(m).rstrip("0").rstrip(".") + "M"
    elif like_count >= 1000:
        k = like_count / 1000
        like_count = str(k).rstrip("0").rstrip(".") + "K"

    svg.add(svg.text(like_count, insert=(250, 184), fill=themes_colors[themes].get("text"), font_size="15px"))

    svg.save()

async def get_repo(user_name, repo_name, theme) :
    """
    This function take a name arg and get the specific users repo
    :return:
    """
    repo_url = "https://api.github.com/repos/" + username + "/" + user_repo_name
    async with aiohttp.ClientSession() as session :
        r = await session.get(repo_url)
        if r.status == 200 :
            data = await r.json()
            # print(json.dumps(data, indent= 4))
            name = data.get("name")
            desc = data.get("description")
            lang = data.get("language")
            likes_count = data.get("stargazers_count")
            repo_url = data.get("url")
            create_svg(f"{user_name}_{repo_name}.svg", desc, name, "image.png", lang, likes_count, theme)
            print("done creating the files")
        else:
            print("could not get data..")
            data = await r.json()
            print(json.dumps(data, indent=4))

async def get_repos(user_name,pinned,theme) :
    """
    This function all the users repo but first check for user pinned arg if yes it get all the pinned repos else it get all users repo
    :return:
    """
    endpoint = "https://api.github.com/users/" + f'{user_name}' + "/repos" #endpoint for all repos
    graph_endpoint = "https://api.github.com/graphql" #ql endpoint for getting pinned repos

    if pinned :
        async with aiohttp.ClientSession() as session:
            r = await session.post(graph_endpoint,json={"query": query, "variables": {"login": f'{user_name}'}}, headers=headers)

            print(f'response with {r.status}')
            print("______________")
            if r.status == 200 :
                data1 = await r.json()
                error = data1.get("errors")
                if not error :
                    data2 = data1["data"]["user"]["pinnedItems"]["nodes"]
                    for i in range(len(data2)):
                        name = data2[i].get("name")
                        desc = data2[i].get("description")
                        lang = data2[i].get("primaryLanguage")["name"]
                        likes_count = data2[i].get("stargazerCount")
                        repo_url = data2[i].get("url")
                        create_svg(f"{user_name}_project_card{i}.svg",desc,name,"image.png",lang,likes_count,theme)

                    print("done creating the files")
                else :
                    rep = { "status" : error[0].get("type"), "message" : error[0].get("message")}
                    print(json.dumps(rep, indent=4))
            else :
                error = await r.json()
                print(error)
    else :
        async with aiohttp.ClientSession() as session :
            r = await session.get(endpoint)

            print(f'response with {r.status}')
            print("______________")
            if r.status == 200 :
                data = await r.json()
                for i in range(len(data)):
                    name = data[i].get("name")
                    desc = data[i].get("description")
                    lang = data[i].get("language")
                    likes_count = data[i].get("stargazers_count")
                    repo_url = data[i].get("url")

                    create_svg(f"{user_name}_project_card{i}.svg", desc, name, "image.png", lang, likes_count,theme)

                print("done creating the files")
            else :
                error = await r.json()
                print(error)


if __name__ == "__main__" :
    asyncio.run(get_repo(username, user_repo_name, selected_theme))
    # asyncio.run(get_repos(username,pinned_repo,selected_theme))

