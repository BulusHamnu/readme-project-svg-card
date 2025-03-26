import svgwrite
import asyncio
import aiohttp
import base64
import textwrap
import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get("GITHUB_TOKEN")

# variable for testing functions and return
username = "BulusHamnu"
user_repo_name = "Demi-Tasks"
pinned_repo = True #this flag is set true if i wanna query for pinned repos
selected_theme = "dark"
imglink =  "https://bulusdev.vercel.app/Asserts/images/animequiz.png"

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
    "warm": {
        "background": "#f4e1d2",
        "header": "#d2691e",
        "text": "#5a3e2b"
    },
    "cool": {
        "background": "#d7f0f7",
        "header": "#239dad",
        "text": "#082f49"
    }
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

#query schema
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
""" 
headers = {"Authorization": f"Bearer {TOKEN}"}



#functions
def create_svg(file_name,desc,title,img_link,lang,like_count,themes) :
    width = 320
    height = 430

    head_rect_y = 225
    head_text_Y = 249
    desc_text_y = 265
    lang_sym_y = 390
    lang_text_y = 395
    star_y_coordinates = [ 386.4, 390.8, 390.8, 394.1, 398.5,396.3, 398.5, 394.1, 390.8, 390.8]
    star_count_y = 398.5

    if img_link == None :
        height = 210
        lang_text_y = 185
        head_rect_y = 15
        head_text_Y = 38
        desc_text_y = 56
        lang_sym_y = 180
        star_y_coordinates = [4 * 1.1 + 168, 8 * 1.1 + 168,8 * 1.1 + 168,11 * 1.1 + 168,15 * 1.1 + 168,13 * 1.1 + 168,15 * 1.1 + 168,11 * 1.1 + 168,8 * 1.1 + 168, 8 * 1.1 + 168 ]
        star_count_y = 184


    # create svg file
    svg = svgwrite.Drawing(file_name, size=(width, height), profile=("full"))
    svg.add(svg.rect(insert=((width - width) / 2, 0), size=(width, height), rx=5, ry=5, fill=(themes_colors[themes].get("background"))))

    #chek for the image parameter
    if img_link != None :
        # getting image from url
        img_file = requests.get(img_link)
        encode_file_data = base64.b64encode(img_file.content)
        decoded_file_data = encode_file_data.decode('utf-8')
        image_data = f'data:image/png/jpeg;base64,{decoded_file_data}'


        svg.add(svg.image(href=image_data, insert=(34.5, -7), size=(250, 250)))

    svg.add(svg.rect(insert=((width - 280) / 2, head_rect_y), size=(280, 35), rx=5, ry=5, fill=(themes_colors[themes].get("header"))))

    #if the title is too long
    if len(title) > 25 :
        title = title[0:25]
        title += ".."

    svg.add(svg.text(title, insert=(width / 2, head_text_Y), fill=themes_colors[themes].get("text"), font_size="20px",text_anchor="middle"))
    paragraph = svg.text("", insert=(width / 2, desc_text_y), fill=themes_colors[themes].get("text"), font_size="16px", text_anchor="middle")

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
    svg.add(svg.circle(center=(40, lang_sym_y), r=8, fill=colors_code[lang ]))
    svg.add(svg.text(lang, insert=(55, lang_text_y), fill=themes_colors[themes].get("text"), font_size="15px"))

    #from web
    star_points = [
        (10 * 1.1 + 225, star_y_coordinates[0]),  # Top
        (12 * 1.1 + 225, star_y_coordinates[1]),
        (16 * 1.1 + 225, star_y_coordinates[2]),
        (13 * 1.1 + 225, star_y_coordinates[3]),
        (14 * 1.1 + 225, star_y_coordinates[4]),
        (10 * 1.1 + 225, star_y_coordinates[5]),
        (6 * 1.1 + 225, star_y_coordinates[6]),
        (7 * 1.1 + 225, star_y_coordinates[7]),
        (4 * 1.1 + 225, star_y_coordinates[8]),
        (8 * 1.1 + 225, star_y_coordinates[9])
    ]
    svg.add(svg.polygon(points=star_points, fill="none", stroke="yellow", stroke_width=2))

    #reduce and change to k format
    if like_count >= 1000000:
        m = like_count / 1000000
        like_count = str(m).rstrip("0").rstrip(".") + "M"
    elif like_count >= 1000:
        k = like_count / 1000
        like_count = str(k).rstrip("0").rstrip(".") + "K"

    svg.add(svg.text(like_count, insert=(250, star_count_y), fill=themes_colors[themes].get("text"), font_size="15px"))

    # svg.save()
    return svg.tostring()

async def get_repo(user_name, repo_name, theme, img_link) :
    """
    This function take a name arg and get the specific users repo
    :return: api response from git
    """
    repo_url = "https://api.github.com/repos/" + user_name + "/" + repo_name
    async with aiohttp.ClientSession() as session :
        r = await session.get(repo_url, headers = headers)
        if r.status == 200 :
            data = await r.json()
            name = data.get("name")
            desc = data.get("description")
            lang = data.get("language")
            likes_count = data.get("stargazers_count")
            repo_url = data.get("url")
            svg_data = create_svg(f"{user_name}_{repo_name}.svg", desc, name, img_link, lang, likes_count, theme)

            
            return [svg_data , r.status]
        else:
            data = await r.json()
            return [{"error" : data} , r.status ]
            

async def get_repos(user_name,pinned,theme, img_link) :
    """
    This function all the users repo but first check for user pinned arg if yes it get all the pinned repos else it get all users repo
    :return: api reponse from git
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

                    svg_list = []
                    for i in range(len(data2)):
                        name = data2[i].get("name")
                        desc = data2[i].get("description")
                        lang = data2[i].get("primaryLanguage")["name"]
                        likes_count = data2[i].get("stargazerCount")
                        repo_url = data2[i].get("url")
                        svg_data = create_svg(f"{user_name}_project_card{i}.svg",desc,name,img_link,lang,likes_count,theme)

                        project_details = {
                            "svg" : svg_data,
                            "project_url" : repo_url
                        }
                        
                        svg_list.append(project_details)

                    return [{ "data" : svg_list }, r.status]
                else :
                    rep = { "status" : error[0].get("type"), "message" : error[0].get("message")}
                    return [{ "error" : rep } , r.status ]
            else :
                error = await r.json()
                return [{ "error" : error } , r.status ]
    else :
        async with aiohttp.ClientSession() as session :
            r = await session.get(endpoint, headers = headers)

            print("______________")
            if r.status == 200 :
                data = await r.json()

                svg_list = []
                for i in range(len(data)):
                    name = data[i].get("name")
                    desc = data[i].get("description")
                    lang = data[i].get("language")
                    likes_count = data[i].get("stargazers_count")
                    repo_url = data[i].get("url")

                    svg_data = create_svg(f"{user_name}_project_card{i}.svg", desc, name, img_link, lang, likes_count,theme)

                    project_details = {
                            "svg" : svg_data,
                            "project_url" : repo_url
                        }

                    svg_list.append(project_details)

                return [{ "data" : svg_list} , r.status ]
            else :
                error = await r.json()
                return [{ "error" : error } , r.status ]


async def get_selected_repos(user_name,repos) :
    endpoint = "https://api.github.com/users/" + f'{user_name}' + "/repos" #endpoint for all

    async with aiohttp.ClientSession() as session :
        r = await session.get(endpoint, headers = headers)

        print("______________")
        if r.status == 200 :
            data = await r.json()

            svg_list = []
            for i in range(len(data)):
                name = data[i].get("name")
                desc = data[i].get("description")
                lang = data[i].get("language")
                likes_count = data[i].get("stargazers_count")
                repo_url = data[i].get("url")


                for repo in repos :
                    if  repo.get("name") == name :
                        svg_data = create_svg(f"{user_name}_project_card{i}.svg", desc, name, 
                            repo.get("imageurl") if repo.get("imageurl") != "None" else None 
                            , lang, likes_count,repo.get("theme"))

                        project_details = {
                            "svg" : svg_data,
                            "project_url" : repo_url
                        }

                        svg_list.append(project_details)

            if not svg_list :
                return [{ "error" : f"No Repos with this names are found. {str([repo.get('name') for repo in repos])}"} , r.status ]

            return [{ "data" : svg_list} , r.status ]
        else :
            error = await r.json()
            return [{ "error" : error } , r.status ]


if __name__ == "__main__" :
    # svg = asyncio.run(get_repo(username, user_repo_name, selected_theme,imglink))
    svgs = asyncio.run(get_repos(username,pinned_repo,selected_theme, imglink))
    # svgs = asyncio.run(get_selected_repos(username,[{"name" : "this"}, { "name" : "that"}]))
    # print(json.dumps(svgs, indent=4))