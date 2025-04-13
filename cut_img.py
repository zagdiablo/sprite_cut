import os, colorama, argparse
from PIL import Image


colorama.init()
print(f"""
{colorama.Fore.MAGENTA}
 ,---.                ,--.  ,--.              ,-----.          ,--.   
'   .-'  ,---. ,--.--.`--',-'  '-. ,---.     '  .--./,--.,--.,-'  '-. 
`.  `-. | .-. ||  .--',--.'-.  .-'| .-. :    |  |    |  ||  |'-.  .-' 
.-'    || '-' '|  |   |  |  |  |  \\   --.    '  '--'\\'  ''  '  |  |   
`-----' |  |-' `--'   `--'  `--'   `----'     `-----' `----'   `--'   
        `--'                                                          
                    Sprite cutter by ZagDiablo
{colorama.Style.RESET_ALL}
""")
parser = argparse.ArgumentParser(
    description="Cut a sheet of sprite into multiple images by width and height.",
    epilog='Usage (python):\npython cut_img.py --file home/img/player.png --out home/result/ -W 77 -H 69\n\nUsage (exe):\n./cut_img --file home/img/player.png --out home/result/ -W 77 -H 69\n\nWill cut the image 77px by 69px evenly into separate images and save the files in home/result/ directory.\n ',
    formatter_class=argparse.RawDescriptionHelpFormatter
)


def main():
    parser.add_argument("-f", "--file", help='Image file, Ex: home/img/img.png', metavar='<IMG FILE>')
    parser.add_argument("-o", "--out", help='Output directory, Ex: home/result', metavar='<OUTPUT DIR>')
    parser.add_argument('--width', help='Width of image to cut in pixel(px), Ex: 77', metavar="<WIDTH>")
    parser.add_argument('--height', help='Height of image to cut in pixel(px), Ex: 69', metavar="<HEIGHT>")
    parser.add_argument('--outname', help='Output file name prefix, Default: cut_1.png, cut_2.png...', metavar='<PREFIX>')

    args = parser.parse_args()

    if args.file:
        if args.out:
            # try:
            # if out dir did not exist make one
            if not os.path.isdir(args.out):
                os.makedirs(args.out)

            sprite_width = int(args.width)
            sprite_height = int(args.height)
            img = Image.open(args.file)
            img_width, img_height = img.size

            # calculate how many images will be cut
            true_img_width = img_width - (img_width % sprite_width) 
            true_img_height = img_height - (img_height % sprite_height)
            horizontal_cut_count = int(true_img_width / sprite_width)
            vertical_cut_count = int(true_img_height / sprite_height)

            if args.width and args.height:
                # Cut images
                for cut_vert in range(vertical_cut_count):
                    for cut_hor in range(horizontal_cut_count):
                        left_side = sprite_width * cut_hor
                        up_side = sprite_height * cut_vert
                        right_side = left_side + sprite_width
                        down_side = up_side + sprite_height
                        result = img.crop((left_side, up_side, right_side, down_side))
                        if args.outname:
                            result.save(f'{args.out}/{args.outname}_{cut_vert}_{cut_hor}.png')
                        else:
                            result.save(f'{args.out}/cut_{cut_vert}_{cut_hor}.png')
            print(f"Finished cutting: {args.file}")
            # except Exception as e:
            #     print("Encountered an error during runtime: ", e)


if __name__ == "__main__":
    main()