import svgwrite
import base64
import textwrap

text = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Illo voluptatibus hic nemo rem nostrum error fuga, omnis eum? Libero soluta a ad aliquam voluptatem odit unde animi. Unde, autem vero? Lorem, ipsum dolor sit amet consectetur adipisicing elit. Illo voluptatibus hic nemo rem nostrum error fuga, omnis eum? Libero soluta a ad aliquam voluptatem odit unde animi. Unde, autem vero?"

def create_svg(file_name,desc,title,cover_img,color,lang,like_count) :
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
    wrapped_text = textwrap.wrap(desc, width=40)
    for i in range(len(wrapped_text)):
        if i < 6:
            if i == 5:
                wrapped_text[i] += "..."
            line = svg.tspan(wrapped_text[i], x=[width / 2], dy=["1.2em"])
            paragraph.add(line)

    svg.add(paragraph)
    svg.add(svg.circle(center=(40, 207), r=8, fill=color))
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
    svg.add(svg.text(like_count, insert=(250, 212), fill='rgb(230, 230, 230)', font_size="15px"))

    svg.save()
    print("done creating the file")


create_svg("project_card.svg",text,"Task Manager App Management system","image.png","red","javascipt","300k")
