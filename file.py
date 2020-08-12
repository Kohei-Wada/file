import sys
import getopt
import re
import os
import time

from pikepdf        import Pdf
from urllib.request import urlopen, urlretrieve
from urllib.parse   import urljoin
from bs4            import BeautifulSoup




target_url    = ""
file_type     = ""
all_file_path = []
saved_files   = []
directory     = None
password      = None
remove        = False




def usage():
    print("[*] Download and save all files from target page to pwd")
    print("")
    print("[*] Usage file.py -u <url> -t <file type>")
    print("    -u --url                 -target url download from")
    print("    -t --type                -file type")
    print("    -d --directory           -directory path save to")
    print("    -p --password            -password")
    print("    -r --remove              -remove all specified filetype")
    print("")
    print("[*] Examples: ")
    print("    file.py -u https://www.google.com -t pdf")
    print("    file.py -u https://www.draong.net -t .word -d ~/Desktop/word/")
    print("    file.py -r -t pdf")

    sys.exit()




def get_all_full_filepath(target_url):

    html = urlopen(target_url)
    bs   = BeautifulSoup(html, "html.parser")

    filter = "(." + file_type + ")"

    #for url in bs.find_all("a", href=re.compile("(.pdf)$")):
    for url in bs.find_all("a", href= re.compile(filter)):
        file = url["href"]
        full_path = urljoin(target_url, file)
        all_file_path.append(full_path)




def save_file(url):

    list = url.split("/")
    file_name = list[len(list) - 1]

    if directory is not None:
        file_name = directory + file_name


    urlretrieve(url, file_name)
    saved_files.append(file_name)
    print(f"saved {file_name}")




def delete_all_files():

    print(f"delete all {file_type} files", end="")

    if directory is not None:
        os.chdir(directory)
        print(f"from {directory}", end="")

    print("...")


    list = os.listdir()

    for file in list:
        if(file.endswith("." + file_type)):
            os.remove(file)

    print("done")




def unlock_and_save(file_name):

    print(f"unlock and save {file_type}")
    try:
        pdf = Pdf.open(file_name, password=password)

    except:
        print(f"failed to unlock {file_name}")
        return

    pdf_unlock = Pdf.new()
    pdf_unlock.pages.extend(pdf.pages)
    pdf_unlock.save("unlocked_" + file_name)
    os.remove(file_name)




def run():

    if remove:
        delete_all_files()
        sys.exit()


    else:
        if not target_url:
            print("url?")
            usage()


        print(f"Download all {file_type} from {target_url}")

        get_all_full_filepath(target_url)

        for link in all_file_path:
            save_file(link)
            time.sleep(1)

        print(f"saved {len(saved_files)} {file_type}")


        if password is not None and file_type == "pdf":
            for pdf in saved_files:
                unlock_and_save(pdf)

        return


def main():

    global target_url
    global file_type
    global remove
    global directory
    global password


    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(
                sys.argv[1:],
                "hu:d:rp:t:",
                ["help", "url=", "directory=", "remove", "password=", "type="])

    except getopt.GetoptError as e:
        print(str(e))
        usage()


    for o, a in opts:

        if o in ("-h", "--help"):
            usage()

        elif o in ("-u", "--url"):
            target_url = a

        elif o in ("-t", "--type"):
            file_type = a

        elif o in ("-d", "--directory"):
            directory = a
            print(f"directory = {directory}")

        elif o in ("-r", "--remove"):
            remove = True

        elif o in ("-p", "--password"):
            password = a
            print(f"password = {password}")

        else:
            assert(False, "Unhandled Option")


    if not file_type:
        print("file type?")
        usage()

    run()



if __name__ == "__main__":
    main()
