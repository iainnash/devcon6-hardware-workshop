import child_process from "child_process";
import fs from 'fs/promises'
import {join} from 'path';

function convert(image, out) {
    console.log({image, out})
  child_process.execSync(
    `convert ${image}[0] -resize 240x240 -alpha off -colors 256 -compress none -type palette BMP3:${out}`
  );
}

async function doConvert() {
    const slides = await fs.readdir(join('.', 'slides'));
    for (const slide of slides) {
        if (!slide.startsWith('.')) {
            convert(`slides/${slide}`, `out/${slide}.bmp`)
        }
    }
}

doConvert();