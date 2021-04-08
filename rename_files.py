# importing os module
import os
  
# Function to rename multiple files
def main():

    directory_name = "recordings_mp4"
    for count, filename in enumerate(os.listdir(directory_name)):
        dst ="clip_" + str(count) + ".mp4"
        src = directory_name + '/' + filename
        dst = directory_name + '/' + dst
          
        # rename() function will
        # rename all the files
        os.rename(src, dst)
  
# Driver Code
if __name__ == '__main__':
      
    # Calling main() function
    main()