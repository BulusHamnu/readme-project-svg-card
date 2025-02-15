import svgwrite
import base64
import textwrap
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get("GITHUB_TOKEN")
user_name = "BulusHamnu"
api_endpoint = "https://api.github.com/users/" + f'{user_name}' + "/repos" #endpoint for all repos
url = "https://api.github.com/graphql" #ql endpoint for getting pinned repos
pinned = True #this flag is set true if i wanna query for pinned repos

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
    "Dockerfile": "#384D54"
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

def create_svg(file_name,desc,title,cover_img,lang,like_count) :
    width = 320
    height = 240

    # covert my image to based64 so it will be saved in the svg
    with open(cover_img, "rb") as image:
        image_file = image.read()
        encode_file_data = base64.b64encode(image_file)
        decoded_file_data = encode_file_data.decode('utf-8')
    image_data = f'data:image/png;base64,{decoded_file_data}'  # format data

    # create svg file
    svg = svgwrite.Drawing(file_name, size=(width, height), profile=("full"))
    svg.add(svg.rect(insert=((width - width) / 2, 0), size=(width, height), rx=5, ry=5, fill=(svgwrite.rgb(40, 44, 52))))
    # svg.add(svg.image(href=image_data, insert=((width - 250) / 2, 0), size=(250, 250))
    svg.add(svg.rect(insert=((width - 280) / 2, 15), size=(280, 35), rx=5, ry=5, fill=(svgwrite.rgb(0, 150, 136))))

    #if the title is too long
    if len(title) > 25 :
        title = title[0:25]
        title += "..."

    svg.add(svg.text(title, insert=(width / 2, 38), fill='rgb(230, 230, 230)', font_size="20px",text_anchor="middle"))
    paragraph = svg.text("", insert=(width / 2, 56), fill='rgb(230, 230, 230)', font_size="16px", text_anchor="middle")

    # to create multi-line and avoid overflow in svg so i broke the desc
    if desc :
        wrapped_text = textwrap.wrap(desc, width=40)
        for i in range(len(wrapped_text)):
            if i < 6:
                if i == 5:
                    wrapped_text[i] += "..."
                line = svg.tspan(wrapped_text[i], x=[ width / 2], dy=["1.2em"])
                paragraph.add(line)
                # width / 2
    else :
        desc = "No description for this project."
        line = svg.tspan(desc, x=[width / 2], dy=["1.2em"])
        paragraph.add(line)

    svg.add(paragraph)
    svg.add(svg.circle(center=(40, 207), r=8, fill=colors_code[lang]))
    svg.add(svg.text(lang, insert=(55, 211), fill='rgb(230, 230, 230)', font_size="15px"))

    #from web
    star_points = [
        (10 * 1.1 + 225, 4 * 1.1 + 196),  # Top
        (12 * 1.1 + 225, 8 * 1.1 + 196),
        (16 * 1.1 + 225, 8 * 1.1 + 196),
        (13 * 1.1 + 225, 11 * 1.1 + 196),
        (14 * 1.1 + 225, 15 * 1.1 + 196),
        (10 * 1.1 + 225, 13 * 1.1 + 196),
        (6 * 1.1 + 225, 15 * 1.1 + 196),
        (7 * 1.1 + 225, 11 * 1.1 + 196),
        (4 * 1.1 + 225, 8 * 1.1 + 196),
        (8 * 1.1 + 225, 8 * 1.1 + 196)
    ]
    svg.add(svg.polygon(points=star_points, fill="none", stroke="yellow", stroke_width=2))

    #reduce and change to k format
    if like_count >= 1000000:
        m = like_count / 1000000
        like_count = str(m).rstrip("0").rstrip(".") + "M"
    elif like_count >= 1000:
        k = like_count / 1000
        like_count = str(k).rstrip("0").rstrip(".") + "K"

    svg.add(svg.text(like_count, insert=(250, 212), fill='rgb(230, 230, 230)', font_size="15px"))

    svg.save()
    print("done creating the file")

def get_repos() :
    r = None
    if pinned :
        r = requests.post(url, json={"query": query, "variables": {"login": f'{user_name}'}}, headers=headers)
        print(f'response with {r.status_code}')
        print("______________")
        if r.status_code == 200 :
            data1 = r.json()
            data2 = data1["data"]["user"]["pinnedItems"]["nodes"]
            for i in range(len(data2)):
                name = data2[i].get("name")
                desc = data2[i].get("description")
                lang = data2[i].get("primaryLanguage")["name"]
                likes_count = data2[i].get("stargazerCount")
                repo_url = data2[i].get("url")
                create_svg(f"project_card{i}.svg",desc,name,"image.png",lang,likes_count)
        else :
            print("could not get data..")
    else :
        r = requests.get(api_endpoint)
        print(f'response with {r.status_code}')
        print("______________")
        if r.status_code == 200 :
            data = r.json()
            for i in range(len(data)):
                name = data[i].get("name")
                desc = data[i].get("description")
                lang = data[i].get("language")
                likes_count = data[i].get("stargazers_count")
                repo_url = data[i].get("url")

                create_svg(f"project_card{i}.svg", desc, name, "image.png", lang, likes_count)
        else :
            print("could not get data..")

get_repos()


