import yt_dlp
import ffmpeg
import sys
import os
import glob
import music_tag

forbiddenChars = ['/','<','>',':','\\','|','?','*']

def main():
    url = input("URL:")
    foldername = input("Album Name:")
    addNumbers = input("Add Numbers (y/n): ")

    dl_opts = {
    'format': 'bestaudio/best',
    }

    if (os.path.isdir(foldername)==False):
        os.mkdir(foldername)
    os.chdir(foldername)

    dl = yt_dlp.YoutubeDL(dl_opts)
    chapters = dl.extract_info(url, download=False)["chapters"]
    if chapters[0]["title"] == "<Untitled Chapter 1>":
        chapters.pop(0)
    print(chapters)
    zeroes = len(str(len(chapters)))

    dl.download(url)

    originalFile = glob.glob("*")[0]

    #split by chapters
    
    for i,chapter in enumerate(chapters):
        startTime = chapter["start_time"]
        endTime = chapter["end_time"]
        name = chapter["title"]
        for char in forbiddenChars:
            name = name.replace(char,'')
        name = name+".mp3"
        if addNumbers == 'y':
            name = str(i+1).zfill(zeroes)+" - "+name
        ffmpeg.run(ffmpeg.output(ffmpeg.input(originalFile).audio.filter('atrim',start=startTime,end=endTime),name))
        f = music_tag.load_file(name)
        f["title"] = chapter["title"]
        f["album"] = foldername
        if addNumbers == 'y':
            f["tracknumber"] = i+1
        f.save()

    os.remove(originalFile)
    
    


if __name__ == "__main__":
    main()