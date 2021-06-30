from dropbox import Dropbox
import dropbox
from pathlib import Path
from keys import TOKEN

n_counter = '689'
dbx = dropbox.Dropbox(TOKEN)
file = f"{n_counter}.png"
file_from = f"/csm/images/{n_counter}.png"
file_to = f'files/{n_counter}.png'
print(file_from)

#####DOWNLOAD#######
dbx.files_download_to_file(file_to, file_from)