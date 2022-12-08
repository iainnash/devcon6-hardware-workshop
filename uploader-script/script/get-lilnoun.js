import { zorbImageDataURI } from "@zoralabs/zorb/dist/main.js";
import { getAddress } from "@ethersproject/address";
import fs from "fs";
import child_process from "child_process";
import prompt from "prompt-sync";
import axios from "axios";
import { ZDK } from "@zoralabs/zdk";

async function main() {
  const zdk = new ZDK();

  var prompter = prompt({ sigint: true });

  const address = prompter("Your address?");
  console.log(`Your address is ${address}`);

  const yourAddress = getAddress(address);

  const NOUNS_ADDRESS = "0x9c8ff314c9bc7f6e59a9d9225fb22946427edc03";
  const LIL_NOUNS_ADDRESS = "0x4b10701Bfd7BFEdc47d50562b76b436fbB5BdB3B";

  const tokens = await zdk.tokens({
    where: {
      collectionAddresses: [NOUNS_ADDRESS, LIL_NOUNS_ADDRESS],
      ownerAddresses: [yourAddress],
    },
  });

  const svg = zorbImageDataURI(yourAddress);

  var svgStr = Buffer.from(svg.substring(svg.indexOf(",")), "base64").toString(
    "utf-8"
  );

  function convert(image, out) {
    child_process.execSync(
      `convert ${image}[0] -resize 240x240 -alpha off -colors 256 -compress none -type palette BMP3:${out}`
    );
  }

  fs.writeFileSync("zorb.svg", svgStr);
  const out1 = child_process.execSync(
    "rsvg-convert zorb.svg --width 240 --height 240 > zorb-normal.png"
  );
  child_process.execSync("convert zorb-normal.png -rotate 180 zorb.png");
  console.log(out1.toString("utf-8"));
  convert("zorb.png", "zorb.bmp");

  child_process.execSync("rm -f ./noun*.png");

  tokens.tokens.nodes.slice(0, 7).map((token, i) => {
    const svgUrl = token.token.image.url;
    fs.writeFileSync(
      `noun${i}.svg`,
      Buffer.from(svgUrl.split(",")[1], "base64").toString("utf-8")
    );

    child_process.execSync(
      `rsvg-convert noun${i}.svg --width 240 --height 240 > noun${i}.png`
    );

    convert(`noun${i}.png`, `noun${i}.bmp`);
  });

  child_process.execSync("bash ./setup.sh noun");
}

main();
