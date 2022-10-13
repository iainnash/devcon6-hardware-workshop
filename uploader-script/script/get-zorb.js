import { zorbImageDataURI } from "@zoralabs/zorb/dist/main.js";
import { getAddress } from "@ethersproject/address";
import fs from "fs";
import child_process from "child_process";
import prompt from 'prompt-sync';
import axios from 'axios'

var prompter = prompt({sigint: true})

const address = prompter("Your address?");
console.log(`Your address is ${address}`);

const svg = zorbImageDataURI(getAddress(address));

var svgStr = Buffer.from(svg.substring(svg.indexOf(",")), "base64").toString(
  "utf-8"
);

function convert(image, out) {
  child_process.execSync(`convert ${image}[0] -resize 240x240 -alpha off -colors 256 -compress none -type palette BMP3:${out}`)
}

fs.writeFileSync("zorb.svg", svgStr);
const out1 = child_process.execSync('rsvg-convert zorb.svg --width 240 --height 240 > zorb-normal.png')
child_process.execSync('convert zorb-normal.png -rotate 180 zorb.png')
console.log(out1.toString('utf-8'))
convert('zorb.png', 'zorb.bmp')

const result = await axios.get(`https://api.poap.tech/actions/scan/${address}`)
const poaps = result.data
for (let i = 0; i < Math.min(7, poaps.length); i++) {
  var url = poaps[i].event.image_url;
  child_process.execSync(`wget ${url} -O poap${i}.png`)

  convert(`poap${i}.png`, `poap${i}.bmp`)
}

// for (let i = 0; i < 7; i++) {
//   convert(`poap${i}.png`, `poap${i}.bmp`)
// }

child_process.execSync('bash ./setup.sh')
