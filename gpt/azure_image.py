import base64
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = '',
  api_version = "2023-12-01-preview",
  azure_endpoint =  'https://linkv-aigc-gpt4turbo.openai.azure.com/'
)


# OpenAI API Key
api_key = "YOUR_OPENAI_API_KEY"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path ="/Users/toto/Desktop/0a7e935da9de58c150262e9ea6e1df60e4064d35.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)
prompt = """
Never forget your are a assistant help me parse descriptions and tags in images, your name is assistant
You need to interpret this picture from the following dimensions:

Gender: 1 girl, 1 boy, 1 male, male focus
Pose: close-up, portraits, upper body, half body, full body
Ethnicity: American girl, white girl, black girl, black woman, Asian girl, mulatto girl, American boy, white man, black man, Asian man, mulatto man, afro
Composition: center pose
Hairstyle: long hair, short hair, very short hair, curly hair, straight hair, ponytail, hair ornament
Hair Color: blonde hair, brown hair, black hair
Hair State: messy hair, soften and smooth hair
Hair Strand Detail: blurry hair, fine hair, detailed hair
Skin Texture: natural skin, mole, wrinkles, freckles
Skin Color: dark skin, dark-skinned
Makeup: make up, eyeshadow, eyeliner, eyelashes, lipstick
Eye Details: beautiful eyes, big eyes, medium eye, detailed eyes
Iris Color: brown eyes, blue eyes, grey eyes, black eyes
Gaze: looking at viewer, looking to the side, looking at another
Facial Hair: facial hair, beard, mustache
Facial Features: lips, parted lips, nose, closed mouth, open mouth, teeth
Expression: smiles, little smiles, light smiles, grin
Body Type: muscular, thin, skinny, slim body, fat
Chest: breast, big breast, small breast, medium breast, cleavage
Hand Position: hand up, arms up, hand on hip, arms behind back, hands in pockets, clenched hand
Clothing: t-shirt, shirt, coat, jackets, pants, jeans, denim, dress, long dress, tank top, glove, shoes
Background Description: simple background, blurry background, depth of field
Indoor/Outdoor: indoors, outdoors
Common Scenes: street, forest, tree, water
Clarity: 4k, 8k, high quality, masterpieces, blurry
Vintage Feel: film grain, retro artstyle, 1960s artstyle
Texture: photography, photographic, realistic

If the result of the action is "Unrecognized", Please do not return the corresponding tag

Among them... is an ellipsis, indicating that there are many such tags, ===The content inside is your answer,Please only return my answers in json format like this:

You need to return a 20-character caption and more than 20 tags

Some tags that are not listed above can also be returned in json tags if they have obvious characteristics.
Example1:
human: Please describe the image below
assistant:
{
   caption:"a beautiful woman is standing on the windowsill holding a cup and looking at the snow in the sky" 
   tag:"1 girl, American girl, center pose,long hair,blonde hair，..."
}

Example2:
human: Please describe the image below
assistant:
{
   caption:"A handsome boy wearing a school uniform is playing with paper airplanes" 
   tag:"1 boy, black boy, beautiful eyes,thin, hand on hip，..."
}

Let's Begin!


"""
response = client.chat.completions.create(
  model="gpt-4-vision",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": prompt},
        {
          "type": "image_url",
          "image_url": {
            "url":f"data:image/jpeg;base64,{base64_image}",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0].message.content)