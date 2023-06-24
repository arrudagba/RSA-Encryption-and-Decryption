import tkinter as tk
import random


def primo(n):
  if n < 2:
    return False
  for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
      return False
  return True


def gcd(a, b):
  while b != 0:
    a, b = b, a % b
  return a


def mod_inv(a, m):
  for i in range(1, m):
    if (a * i) % m == 1:
      return i
  return None


def gerar_par():
  global p_entry, q_entry, chave_publica, chave_privada
  p = int(p_entry.get())  # first prime number
  q = int(q_entry.get())  # second prime number
  if not (primo(p) and primo(q)):
    raise ValueError("Both numbers must be prime.")
  elif p == q:
    raise ValueError("p and q cannot be equal.")
  n = p * q
  phi = (p - 1) * (q - 1)
  e = random.randrange(1, phi)
  g = gcd(e, phi)
  while g != 1:
    e = random.randrange(1, phi)
    g = gcd(e, phi)
  d = mod_inv(e, phi)
  chave_publica, chave_privada = ((e, n), (d, n))


def criptografar(pk, plaintext):
  key, n = pk
  cipher = [pow(ord(char), key, n) for char in plaintext]
  return cipher


def descriptografar(pk, ciphertext):
  key, n = pk
  plain = [chr(pow(char, key, n)) for char in ciphertext]
  return ''.join(plain)


def encriptar_mensagem():
  global chave_publica
  msg = msg_entry.get()
  msg_criptografada = criptografar(chave_publica, msg)
  cipher_text.insert(
    tk.END, "Encrypted message: " +
    ' '.join(map(lambda x: str(x), msg_criptografada)) + "\n")


def desencriptar_mensagem():
  global chave_privada
  msg = msg_entry.get()
  msg_criptografada = list(map(int, msg.split()))
  msg_descriptografada = descriptografar(chave_privada, msg_criptografada)
  plain_text.insert(
    tk.END, "Decrypted message: " + msg_descriptografada + "\n")


# function to clear the entry when clicking on it
def on_entry_click(event):
  if event.widget.get() == 'First prime number' or event.widget.get(
  ) == 'Second prime number':
    event.widget.delete(0, "end")
  return None


window = tk.Tk()
window.title("RSA Coverter")

p_entry = tk.Entry(window, width=50)
p_entry.insert(0, 'First prime number')
p_entry.bind('<FocusIn>', on_entry_click)
p_entry.pack()

q_entry = tk.Entry(window, width=50)
q_entry.insert(0, 'Second prime number')
q_entry.bind('<FocusIn>', on_entry_click)
q_entry.pack()

generate_button = tk.Button(window,
                            text="Generate key pairs",
                            command=gerar_par)
generate_button.pack()

msg_entry = tk.Entry(window, width=50)
msg_entry.pack()

encrypt_button = tk.Button(window,
                           text="Encrypt message",
                           command=encriptar_mensagem)
encrypt_button.pack()

decrypt_button = tk.Button(window,
                           text="Decrypt message",
                           command=desencriptar_mensagem)
decrypt_button.pack()

cipher_text = tk.Text(window, height=10, width=50)
cipher_text.pack()

plain_text = tk.Text(window, height=10, width=50)
plain_text.pack()

window.mainloop()
