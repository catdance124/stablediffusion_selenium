import sys, pathlib
from huggingface_stablediffusion import StableDiffusion


def generate(query):
    sd= StableDiffusion()
    try:
        imgs = sd.generate_images(query)
    finally:
        sd.quit()
    return imgs

if __name__ == "__main__":
    query = sys.argv[1]
    print(query)
    save_dir = pathlib.Path('./images')
    save_dir.mkdir(parents=True, exist_ok=True)
    imgs = generate(query)
    for i in range(len(imgs)):
        filename = f'image{i}.jpg'
        with open(save_dir / filename, 'wb') as f:
            f.write(imgs[i])