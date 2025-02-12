import svgwrite
import base64
import textwrap
width = 320
height = 430
text = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Illo voluptatibus hic nemo rem nostrum error fuga, omnis eum? Libero soluta a ad aliquam voluptatem odit unde animi. Unde, autem vero? Lorem, ipsum dolor sit amet consectetur adipisicing elit. Illo voluptatibus hic nemo rem nostrum error fuga, omnis eum? Libero soluta a ad aliquam voluptatem odit unde animi. Unde, autem vero?"
wrapped_text = textwrap.wrap(text, width=40)

# covert my image to based64 so it will be saved in the svg
with open("image.png","rb") as image :
    image_file = image.read()
    encode_file_data = base64.b64encode(image_file)
    decoded_file_data = encode_file_data.decode('utf-8')
image_data = f'data:image/png;base64,{decoded_file_data}' #format data


# create svg file
svg = svgwrite.Drawing("card.svg",size=(width,height), profile=("full"))
svg.add(svg.rect(insert=((width- width) / 2,0),size=(width,height),rx=5,ry=5, fill=(svgwrite.rgb(40, 44, 52))))
svg.add(svg.image(href=image_data,insert=((width - 250) / 2,0),size=(250,250)))
svg.add(svg.rect(insert=((width- 280) / 2,231),size=(280,35),rx=5,ry=5, fill=(svgwrite.rgb(0, 150, 136))))
svg.add(svg.text("Project Name duh", insert=(width / 2, 255), fill='rgb(230, 230, 230)', font_size="20px", text_anchor="middle"))
paragraph = svg.text("", insert=(width / 2, 272), fill='rgb(230, 230, 230)', font_size="16px", text_anchor="middle")

#to create multi-line and avoid overflow in svg so i broke the desc
for i in range(len(wrapped_text)) :
    if i < 7 :
        if i == 6 :
            wrapped_text[i] += "..."
        print(wrapped_text[i])
        line = svg.tspan(wrapped_text[i], x=[width / 2] , dy=["1.2em"])
        paragraph.add(line)

svg.add(paragraph)
svg.save()

print("----------------------")
print("done creating the file")
