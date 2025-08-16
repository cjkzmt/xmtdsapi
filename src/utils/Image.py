from PIL import   Image, ImageFont, ImageDraw
色值={
    '红': '#ff0000',
    "绿": '#00ff00',
    "蓝": '#0000ff',
    "黄": (254,223,1),
    "紫": '#ff00ff',
    "青": '#00ffff',
    "橙": '#ffa500',
    "粉": '#ff69b4',
    "灰": '#808080',
    "白": (255,255,255),
    "黑": (0,0,0)  
    } 
def get_str_info(t, z, F):
    f = ImageFont.truetype(F, z)
    b = f.getbbox(t)
    return b[2] - b[0],b[3] - b[1]
def 低图(img,k,tg,g,t):
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x1,y1,x2,y2 = 0, (tg-g)/2,k,(tg+g)/2
    draw.rectangle([x1,y1,x2,y2], fill=(0, 0, 0, int(255 *t)))  
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def 绘字(i, b):
    d = ImageDraw.Draw(i)  
    x, y, t, f, z, c = b
    F = ImageFont.truetype(f, z)
    if len(c) > 1:
        for dx, dy in [(-3, -3), (-3, 0), (-3, 3), (0, -3), (0, 3), (3, -3), (3, 0), (3, 3)]:
            d.text((x + dx, y + dy), t, font=F, fill=色值[c[-1]])
    d.text((x, y), t, font=F, fill=色值[c[0]])
    return i
def 方形(i,b):
    d = ImageDraw.Draw(i)  
    x1,y1,x2,y2,c,w=b
    d.rectangle([x1, y1,x2,y2], outline=色值[c], width=w)
    return i