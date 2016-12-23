# COLLAGE

Stitching Little Images Into Larger Images

**Instructions**:

* **Setting Executable Bit**: eg. `$chmod +x collage.py`
* **Browsing Usage**: eg. `./collage.py -h`
* **Converting Output Images to Video**: eg. `ffmpeg -r 25 -i output/frame-%05d.jpg -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4`

**Examples**:

Here are some examples:

![1 x 1](lena1.jpg)

Lena

![5 x 5](lena5.jpg)

Some More Lena

![25 x 25](lena25.jpg)

Even More Lena

![100 x 100](lena100.jpg)

A Lot of Lena

**Notes**:

* Requires python.
* Requires pyopencv.
* Requires ffmpeg.
