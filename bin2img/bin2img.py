'''
This code snap is for reading images e.g. jpg, png from binary data (.bin)
The project is encountered in distributed tensorflow training in MSRA
'''
import io
import numpy as np
import PIL

info_path = 'XXXXX'      # this is for providing [filename, begin, offset, label]
train_path = 'train.bin' # this is image file stored in binary format
f = open(info_path)
data = open(train_path, 'rb')
line = f.readline()
while line != '':
	begin = int(line.split()[1])  # this is begin position of file pointer
	length = int(line.split()[2]) # this is the length of data chunk
	data.seek(begin, 0)           # move file pointer to begin position
	img = data.read(length)       # read length bytes data now the img id of class bytes
	img = PIL.Image.open(io.BytesIO(img))    # using pil to decode bin to img now the img is of class PIL.Image
	img = np.asarray(img, dtype=np.uint8)    # using numpy to convert PIL.Image to ndarray
	print(img.shape)
	line = f.readline()