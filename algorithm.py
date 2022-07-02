from PIL import Image
import requests
import json


class FlagGenerator:
    def __init__(self, id, starsUrl, stripesUrl, changesLeft):
        self.id = id
        self.starsUrl = starsUrl
        self.stripesUrl = stripesUrl
        self.starsImage = Image.open(requests.get(
            starsUrl, stream=True).raw).resize((500, 300), Image.ANTIALIAS).convert("RGBA")
        self.stripesImage = Image.open(requests.get(
            stripesUrl, stream=True).raw).resize((1000, 600), Image.ANTIALIAS).convert("RGBA")
        self.changesLeft = changesLeft

    def compile(self):
        """
        This function compiles the image src urls into a singular flag image and saves it locally

        Takes: self
        Use: defines self.flag
        Returns: none
        """

        stripes = Image.new("RGBA", self.stripesImage.size)
        stripes = Image.alpha_composite(stripes, self.stripesImage)

        stars = Image.new("RGBA", self.stripesImage.size)
        stars.paste(self.starsImage, (0, 0))

        flag = Image.alpha_composite(stripes, stars)
        flag.save("flag.png")
        self.flag = flag

    def upload(self):
        """
        This function uploads the local image file to ipfs along with a corresponding metadata json file

        Takes: self
        Use: defines self.metadata
        Returns: jsonUrl
        """

        with open('flag.png', "rb") as a_file:
            file_dict = {"file_to_upload.txt": a_file}
            response1 = requests.post(
                'https://ipfs.infura.io:5001/api/v0/add', files=file_dict)
            hash = response1.text.split(",")[1].split(":")[1].replace('"', '')
            flagUrl = "https://infura-ipfs.io/ipfs/" + hash

            suffix = " (LIVE)" if self.changesLeft == 1 else " (WIP)"
            metadata = {
                "name": "Americans Flags NFT #" + str(self.id) + suffix,
                "description": "This live Americans Flags NFT is one of the many interpretations of 'America'." if self.changesLeft == 1 else "This work-in-progress Americans Flags NFT is one of the many interpretations of 'America'.",
                "image": flagUrl,
                "id": self.id,
                "edition": 2022,
                "attributes":
                [
                    {
                        "trait_type": "Stars Background Image Url",
                        "value": self.starsUrl
                    },
                    {
                        "trait_type": "Stripes Background Image Url",
                        "value": self.stripesUrl
                    }
                ]
            }

            json_object = json.dumps(metadata, indent=4)
            with open("metadata.json", "w") as outfile:
                outfile.write(json_object)

            with open('metadata.json', "rb") as outfileJSON:
                file_dict_json = {"file_to_upload.txt": outfileJSON}
                response2 = requests.post(
                    'https://ipfs.infura.io:5001/api/v0/add', files=file_dict_json)
                hash = response2.text.split(",")[1].split(":")[
                    1].replace('"', '')
                jsonUrl = "https://infura-ipfs.io/ipfs/" + hash

                print(jsonUrl)
                return jsonUrl


if __name__ == "__main__":
    starsLink = "https://thumbor.forbes.com/thumbor/fit-in/x/https://www.forbes.com/advisor/ca/wp-content/uploads/2022/05/ethereum-1.jpeg"
    stripesLink = "https://upload.wikimedia.org/wikipedia/en/2/27/Bliss_%28Windows_XP%29.png"
    generator = FlagGenerator(0, starsLink, stripesLink, 3)
    generator.compile()
    # print(generator.upload())
