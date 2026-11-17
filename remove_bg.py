from PIL import Image

src = r'frontend\public\yeni_ana_logo.jpeg'
dst = r'frontend\public\yeni_ana_logo_transparent.png'

img = Image.open(src).convert('RGBA')
w, h = img.size
pixels = img.load()

print(f'Size: {w}x{h}')

# JPEG compression ile kenar pikselleri hafif gri olabiliyor
# Sadece çok yüksek eşikle (254+) kesin beyaz pikselleri sil
# Böylece logo detayları (gri tonları) korunur

# Önce flood fill ile köşelerden başla - sadece bağlantılı beyaz alanları sil
# Bu sayede logonun içindeki beyaz alanlar korunur

from collections import deque

THRESHOLD = 240  # 240+ olan pikseller "beyaz arka plan" sayılır

def is_bg(r, g, b):
    return r >= THRESHOLD and g >= THRESHOLD and b >= THRESHOLD

# 4 köşeden flood fill
visited = [[False]*h for _ in range(w)]
queue = deque()

corners = [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]
for cx, cy in corners:
    r, g, b, a = pixels[cx, cy]
    if is_bg(r, g, b) and not visited[cx][cy]:
        queue.append((cx, cy))
        visited[cx][cy] = True

changed = 0
while queue:
    x, y = queue.popleft()
    r, g, b, a = pixels[x, y]
    pixels[x, y] = (r, g, b, 0)
    changed += 1

    for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
            nr, ng, nb, na = pixels[nx, ny]
            if is_bg(nr, ng, nb):
                visited[nx][ny] = True
                queue.append((nx, ny))

print(f'Flood fill ile transparan yapılan piksel: {changed}')
img.save(dst, 'PNG')
print(f'Kaydedildi: {dst}')
