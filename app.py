from PIL import Image
from tkinter import Tk, filedialog, Button, Label, Entry, Text

def encode_image(image_path, data):
  img = Image.open("/content/Screenshot 2024-04-24 234736.png").convert("RGB")
  width, height = img.size

  num_pixels = width * height
  required_pixels = len(data) * 3  
  if required_pixels > num_pixels:
    raise ValueError("Data too large to be encoded in the image")

  data_index = 0
  pixels = img.load()

  for y in range(height):
    for x in range(width):
      if data_index >= len(data):
        break

      r, g, b = pixels[x, y]

      data_byte = format(data[data_index], '08b')

      new_r = r & ~1 | int(data_byte[0])
      new_g = g & ~1 | int(data_byte[1])
      new_b = b & ~1 | int(data_byte[2])

      pixels[x, y] = (new_r, new_g, new_b)
      data_index += 1

  return img

def decode_image(image_path):
  img = Image.open(image_path).convert("RGB")
  width, height = img.size

  data = ""
  for y in range(height):
    for x in range(width):

      try:
        r, g, b = img.getpixel((x, y))
        data_bit = str((r & 1) + (g & 1) * 2 + (b & 1) * 4)
      except ValueError:
        continue 
      data += data_bit

  data_bytes = [data[i:i+8] for i in range(0, len(data), 8)]
  try:
    decoded_data = "".join([chr(int(byte, 2)) for byte in data_bytes])
  except ValueError:
    return ""  

  return decoded_data

def encode_button_click():
  image_path = filedialog.askopenfilename(title="Select Image")
  data_to_encode = entry_data.get("1.0", "end").rstrip()

  try:
    encoded_image = encode_image(image_path, data_to_encode.encode())
    encoded_image.save("stego_image.png")
    label_message.config(text="Data encoded successfully!")
  except ValueError as e:
    label_message.config(text=f"Error: {e}")

def decode_button_click():

  image_path = filedialog.askopenfilename(title="Select Image")
  try:
    decoded_data = decode_image(image_path).decode()
    text_decoded.delete("1.0", "end")
    text_decoded.insert("1.0", decoded_data)
    label_message.config(text="Data decoded successfully!")
  except Exception as e:
    label_message.config(text=f"Error: {e}")

root = Tk()
root.title("Image Steganography")


label_image = Label(root, text="Select Image:")
label_image.grid(row=0, column=0, padx=5, pady=5)

button_image = Button(root, text="Browse", command=encode_button_click)
button_image.grid(row=0, column=1, padx=5, pady=5)

label_data = Label(root, text="Enter Secret Message:")
label_data.grid(row=1, column=0, padx=5, pady=5)

entry_data = Text(root, width=40, height=5)
entry_data.grid(row=2, columnspan=2, padx=5, pady=5)

button_encode = Button(root, text="Encode", command=encode_button_click)
button_encode.grid(row=3, column=0, padx=5, pady=5)

button_decode = Button(root, text="Decode", command=decode_button_click)
button_decode.grid(row=3, column=1, padx=5, pady=5)

label_message = Label(root, text="")
label_message.grid(row=4, columnspan=2, padx=5, pady=5)

text_decoded = Text(root, width=40, height=5, state="disabled")
text_decoded.grid(row=5, columnspan=2, padx=5, pady=5)

root.mainloop()