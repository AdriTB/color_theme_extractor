#Color theme extractor
#By AdriTB

#How it works?
#Example of use: $python color_theme.py 'path/to/image.png' 3 -> Returns three main colors of the image
#If not specifing number of colors takes five by default
#Suports .png and .jpeg

from turtle import clear
import pandas as pd
from PIL import Image
import pyTextColor
import sys
import plot3D
from sklearn import cluster

class ThemeExtractor:    

    def __init__(self, image):
        self.image = image
        self.main_colors = []

    @staticmethod
    #Format rgb to hex
    def rgb_to_hex(rgb_color):
        return format("#%.02x%02x%02x" % tuple([int(x) for x in rgb_color])).upper()
    
    # Remove alpha colors
    def __remove_alpha_colors(self,df):
        alpha_min_value = 255
        df['alpha'] = df['color'].apply(lambda x:x[3])
        df = df.drop(df[df['alpha'] < alpha_min_value].index)
        df['color'] = df['color'].apply(lambda x:x[:-1])
        df.pop('alpha')
        return df

    #Extract all colors and sort by frequency
    def __get_colors(self):
        heigth,width = self.image.size
        colors = self.image.getcolors(width * heigth)
        with_alpha = len(colors[0][1]) == 4
        df_colors = pd.DataFrame(colors,columns=['freq','color'])
        if with_alpha:
            df_colors = self.__remove_alpha_colors(df_colors)
        # Optimize for large lists of colors
        col_count = df_colors.count()[0]
        max_colors = col_count // 10 if col_count // 10 > 8 else col_count
        
        return df_colors.sort_values('freq',ascending=False).head(max_colors)

    #Main extract method
    def theme(self, max,show_graph=False,show_image=False)->list:
        #Get all colors and format it
        all_colors = self.__get_colors()
        print(all_colors.head(10))
        # Clustering colors as 3D points
        kmeans = cluster.KMeans(n_clusters=max)
        kmeans.fit(list(all_colors['color'].values))
        filtered_colors = kmeans.cluster_centers_
        self.main_colors = filtered_colors
        # Show image option
        if show_image: self.image.show()
        # Show plot 3D option
        if show_graph: plot3D.show_data(all_colors)
        return self.main_colors
    
    #Show main colors
    def show_theme(self):
        if(len(self.main_colors) > 0):
            print(f"Colors of theme: {len(self.main_colors)}\n")
            pytext = pyTextColor.pyTextColor()
            for color in self.main_colors:
                hex_color = ThemeExtractor.rgb_to_hex(color)
                text = pytext.format_text(text= hex_color, color="black", bgcolor= hex_color)
                print (text)
        else:
            print("No extracted colors")

def main():
    if (len(sys.argv[1:]) > 3 and len(sys.argv[1:]) < 1) :
        print("""Please, check your command line arguments. 
        -First argument:                Path of the image.
        -Second argument(Optional):     Number of colors you need (Default five)."""
        )    
    else:
        try:
            path = sys.argv[1]
            #Max colors specified (Default 5)
            max_colors = int(sys.argv[2]) if len(sys.argv) == 3 else 5
            if(max_colors <= 0 or max_colors > 8):
                raise ValueError
            image = Image.open(path)
            #TODO Check if image is in P mode (mapping a palette)
            #Method Image.getpalette()
            extractor = ThemeExtractor(image)
            print('...getting theme')
            extractor.theme(max_colors,show_image=True,show_graph=False)
            extractor.show_theme()
            image.close()
        except FileNotFoundError:
            print("File not found")
        except ValueError:
            print("Value of number of colors invalid")
            print("Enter a number between 1 and 8")

if __name__=='__main__':
    main()
    

    
