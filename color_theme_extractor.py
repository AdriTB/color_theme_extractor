#Color theme extractor
#By AdriTB

#How it works?
#Example of use: $python color_theme.py 'path/to/image.png' 3 -> Returns three main colors of the image
#If not specifing number of colors takes five by default
#Suports .png and .jpeg

from cmath import sqrt
from PIL import Image
import pyTextColor
import sys

class ThemeExtractor:    
    
    main_colors = []

    def __init__(self, image):
        self.image = image  

    #Format rgb to hex
    def __rgb_to_hex(self, rgb_color):
        return format("#%02x%02x%02x" % rgb_color).upper()

    #Format all colors without alpha channel
    def __rgb_format(self, colors):
        rgb_colors = []
        with_alpha = False
        if(len(colors[0][1]) > 3):
            with_alpha = True
        
        for result in colors:
            if(with_alpha):
                colorRGB = result[1][:-1]            
                alpha = result[1][-1]
                if(alpha > 0):
                    rgb_colors.append(colorRGB)
            else:
                colorRGB = result[1]
                rgb_colors.append(colorRGB)
            
        return rgb_colors

    #Extract all colors with all information
    def __extract_all_colors(self):
        width, heigth = self.image.size
        colors = self.image.getcolors(width * heigth)
        print(f"Format of color: {colors}")
        #print(f"Find {len(colors)} colors in that image")
        colors.sort()
        colors.reverse()
        max_colors = len(colors)//1000
        if(max_colors < 256):
            max_colors = len(colors)
        colors = colors[:max_colors] #Select only main colors
        #print(f"Colors detected: {len(colors)}")
        return colors

    #Compare two colors in a 3D space taking rgb values like cordinates
    def __compare_colors_channel(self, color, f_color, accurancy):
        margin = 220
        margin = margin - (accurancy * margin * 0.1)
        #Distance between this two points
        d = sqrt(pow(color[0]-f_color[0],2) + pow(color[1]-f_color[1],2) + pow(color[2]-f_color[2],2))  
        return d.real < margin

    #Main extract function
    def extract_main_colors(self, max):
        #Get all colors and format it
        all_colors = self.__extract_all_colors()
        all_colors = self.__rgb_format(all_colors)
        #Add to f_colors the most present color
        filtered_colors = []
        filtered_colors.append(all_colors[0])
        #Take colors one by one in order 
        accurancy = 0
        while(len(filtered_colors) != max):
            accurancy += 1
            for color in all_colors:
                if(not filtered_colors.__contains__(color)):
                    for f_color in filtered_colors:
                        if(self.__compare_colors_channel(color, f_color, accurancy)):
                            break
                    else:
                        filtered_colors.append(color)
                        accurancy = 0
                        break
            #No more relevant colors
            if(accurancy > max * 3):
                print("No more relevant colors in the image")
                break
            
        self.main_colors = tuple(filtered_colors)
    
    #Show main colors
    def show_colors(self):
        if(self.main_colors != []):
            #print(f"Colors of theme: {len(self.main_colors)}\n")
            pytext = pyTextColor.pyTextColor()
            for color in self.main_colors:
                hex_color = self.__rgb_to_hex(color)
                text = pytext.format_text(text= hex_color, color="black", bgcolor= hex_color)
                print (text)
        else:
            print("No extracted colors")


if (len(sys.argv[1:]) > 3 and len(sys.argv[1:]) < 1) :
    print("""Please, check your command line arguments. 
    -First argument:                Path of the image.
    -Second argument(Optional):     Number of colors you need (Default five)."""
    )    
else:
    try:
        path = sys.argv[1]
        max_colors = 5
        if(len(sys.argv) == 3):
            max_colors = int(sys.argv[2])
        if(max_colors <= 0 or max_colors > 8):
            raise ValueError
        image = Image.open(path)
        #image.show()
        extractor = ThemeExtractor(image)
        #TODO Check if image is in P mode (mapping a palette)
        #Method Image.getpalette()
        extractor.extract_main_colors(max_colors)
        extractor.show_colors()
    except FileNotFoundError:
        print("File not found")
    except ValueError:
        print("Value of number of colors invalid")
        print("Enter a number between 1 and 8")

    

    
