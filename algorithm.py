from PIL import Image
import requests
import json
import datetime

projectId = "2KHm9KJmiddsClBskS6cDdNwJII"
projectSecret = "439643f1fdd076da3fe2fa36a33bdfb7"


class FlagGenerator:
    def __init__(self, id, starsUrl, stripesUrl, starsTitle, stripesTitle, starsSummary, stripesSummary, description, lastChanged, changesLeft):
        self.id = id
        self.starsUrl = starsUrl
        self.stripesUrl = stripesUrl
        self.starsTitle = starsTitle
        self.stripesTitle = stripesTitle
        self.starsSummary = starsSummary
        self.stripesSummary = stripesSummary
        self.description = description
        self.starsImage = Image.open(requests.get(
            starsUrl, stream=True).raw).resize((430, 297), Image.ANTIALIAS).convert("RGBA")
        self.stripesImage = Image.open(requests.get(
            stripesUrl, stream=True).raw).resize((920, 552), Image.ANTIALIAS).convert("RGBA")
        self.lastChanged = lastChanged
        self.changesLeft = changesLeft

    def compile(self):
        """
        This function compiles the image src urls into a singular flag image and saves it locally

        Takes: self
        Use: defines self.flag
        Returns: none
        """
        canvas = Image.new("RGBA", (478, 345))
        canvas.paste(self.starsImage, (25, 25))
        stars = Image.alpha_composite(canvas, Image.open("stars.png").resize(
            (478, 345), Image.ANTIALIAS).convert("RGBA"))
        stripes = Image.new("RGBA", (1000, 630))
        stripes.paste(self.stripesImage, (49, 47))
        flag = Image.alpha_composite(stripes, Image.open("stripes.png").resize(
            (1000, 630), Image.ANTIALIAS).convert("RGBA"))
        flag.paste(stars, (0, 0))
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
                'https://ipfs.infura.io:5001/api/v0/add', files=file_dict, auth=(projectId, projectSecret))
            hash = response1.text.split(",")[1].split(":")[1].replace('"', '')
            flagUrl = "https://infura-ipfs.io/ipfs/" + hash
            suffix = " (LIVE)" if self.changesLeft == 1 else " (WIP)"
            metadata = {
                "name": "Americans Flags NFT #" + str(self.id) + suffix,
                "description": self.description,
                "image": flagUrl,
                "id": self.id,
                "edition": datetime.date.today().year,
                "attributes":
                [
                    {
                        "trait_type": "Flag Status",
                        "value": "Live" if self.changesLeft == 1 else "Work-In-Progress"
                    },
                    {
                        "trait_type": "Stars Background Image Url",
                        "value": self.starsUrl
                    },
                    {
                        "trait_type": "Stars Background Image Title",
                        "value": self.starsTitle
                    },
                    {
                        "trait_type": "Stars Background Image Summary",
                        "value": self.starsSummary
                    },
                    {
                        "trait_type": "Stripes Background Image Url",
                        "value": self.stripesUrl
                    },
                    {
                        "trait_type": "Stripes Background Image Title",
                        "value": self.stripesTitle
                    },
                    {
                        "trait_type": "Stripes Background Image Summary",
                        "value": self.stripesSummary
                    },
                    {
                        "trait_type": "Left Changed",
                        "value": self.lastChanged
                    },
                    {
                        "trait_type": "Changes Left",
                        "value": self.changesLeft
                    }
                ]
            }
            json_object = json.dumps(metadata, indent=4)
            with open("metadata.json", "w") as outfile:
                outfile.write(json_object)
            with open('metadata.json', "rb") as outfileJSON:
                file_dict_json = {"file_to_upload.txt": outfileJSON}
                response2 = requests.post(
                'https://ipfs.infura.io:5001/api/v0/add', files=file_dict_json, auth=(projectId, projectSecret))
                hash = response2.text.split(",")[1].split(":")[
                    1].replace('"', '')
                jsonUrl = "https://infura-ipfs.io/ipfs/" + hash
                return jsonUrl


if __name__ == "__main__":
    starsLink = "https://thumbor.forbes.com/thumbor/fit-in/x/https://www.forbes.com/advisor/ca/wp-content/uploads/2022/05/ethereum-1.jpeg"
    stripesLink = "https://upload.wikimedia.org/wikipedia/en/2/27/Bliss_%28Windows_XP%29.png"
    starsName = "Ether to the moon!"
    stripesName = "PC on top"
    starsDesc = "Cool Ethereum logo"
    stripesDesc = "Windows XP pasture"
    description = "Hello world!"
    generator = FlagGenerator(0, starsLink, stripesLink, starsName,
                              stripesName, starsDesc, stripesDesc, description, 3)
    generator.compile()
    print(generator.upload())
