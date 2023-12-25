from openai import OpenAI

# Set your OpenAI API key

client = OpenAI(
  api_key='Your API Key',  # this is also the default, it can be omitted
)


response = client.images.generate(
  model="dall-e-3",
  prompt="Kids storybook cover: spidery first day of school",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print (image_url)

# Download the image
image_data = openai.File(image_url).get()

# Save the image to a file
with open('generated_image.png', 'wb') as f:
    f.write(image_data)

print('Image saved to generated_image.png')
