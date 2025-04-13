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
    epilog='Usage (python):\npython sprite_cut.py --file home/img/player.png --out home/result/ -W 77 -H 69\n\nUsage (exe):\n./sprite_cut --file home/img/player.png --out home/result/ -W 77 -H 69\n\nWill cut the image 77px by 69px evenly into separate images and save the files in home/result/ directory.\n ',
    formatter_class=argparse.RawDescriptionHelpFormatter
)


def cut_w_wh(sheet, args):
    sheet_width, sheet_height = sheet.size
    cut_width = int(args.width)
    cut_height = int(args.height)
    # calculate how many images will be cut based on the cut width and height to the sheet size
    true_sheet_width = sheet_width - (sheet_width % cut_width)
    true_sheet_height = sheet_height - (sheet_height % cut_height)
    vertical_cut_count = int(true_sheet_height / cut_height) # sum of vertical cut (col)
    horizontal_cut_count = int(true_sheet_width / cut_width) # sum of horizontal cut (row)

    # Cut images
    for cut_hor in range(horizontal_cut_count):
        for cut_vert in range(vertical_cut_count):
            left_side = cut_width * cut_vert
            up_side = cut_height * cut_hor
            right_side = left_side + cut_width
            down_side = up_side + cut_height
            result = sheet.crop((left_side, up_side, right_side, down_side))
            if args.outname:
                result.save(f'{args.out}/{args.outname}_{cut_hor}_{cut_vert}.png')
            else:
                result.save(f'{args.out}/cut_{cut_hor}_{cut_vert}.png')


def cut_auto(sheet, args):
    sheet_width, sheet_height = sheet.size
    vertical_cut_count =  int(input("How many vertical cut? (col) >> "))
    horizontal_cut_count = int(input("How many horizontal cut? (row) >> "))
    # calculate how many images will be cut based on the cut count
    # to automatically determined the cut size
    cut_width = sheet_width / vertical_cut_count
    cut_height = sheet_height / horizontal_cut_count
    
    # Cut images
    for cut_hor in range(horizontal_cut_count):
        for cut_vert in range(vertical_cut_count):
            left_side = cut_width * cut_vert
            up_side = cut_height * cut_hor
            right_side = left_side + cut_width
            down_side = up_side + cut_height
            result = sheet.crop((left_side, up_side, right_side, down_side))
            if args.outname:
                result.save(f'{args.out}/{args.outname}_{cut_hor}_{cut_vert}.png')
            else:
                result.save(f'{args.out}/cut_{cut_hor}_{cut_vert}.png')
    



def main():
    parser.add_argument("-f", "--file", help='Image file, Ex: home/img/img.png', metavar='<IMG FILE>')
    parser.add_argument("-o", "--out", help='Output directory, Ex: home/result', metavar='<OUTPUT DIR>')
    parser.add_argument('--width', help='Width of image to cut in pixel(px), Ex: 77', metavar="<WIDTH>")
    parser.add_argument('--height', help='Height of image to cut in pixel(px), Ex: 69', metavar="<HEIGHT>")
    parser.add_argument('--outname', help='Output file name prefix, Default: cut_1.png, cut_2.png...', metavar='<PREFIX>')
    parser.add_argument('--auto', help='Automatically determined the cut size based on how many cut you want', action="store_true")

    args = parser.parse_args()

    if args.file:
        if args.out:
            # if out dir did not exist make one
            if not os.path.isdir(args.out):
                os.makedirs(args.out)

            sheet = Image.open(args.file)

            if args.width and args.height:
                cut_w_wh(sheet, args)
            elif args.auto:
                cut_auto(sheet, args)
            print(f"Finished cutting: {args.file}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print("Input must be a number: ", e)
        exit()
    except KeyboardInterrupt as e:
        print("Exit... ", e)
        exit()
    except Exception as e:
        print("Error: ", e)
        exit()